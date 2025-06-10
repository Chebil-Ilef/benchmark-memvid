import os
import time
import json
import re
import pdfplumber
import numpy as np
from pathlib import Path
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import faiss

INPUT_DATA_DIR = Path("./documents/reports")
OUTPUT_FAISS_DIR = Path("./data_faiss/reports")
MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 512
OVERLAP = 50
MAX_CHUNKS = 1000

def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages).strip()
    except Exception as e:
        print(f"Error reading {pdf_path.name}: {e}")
        return ""


def chunk_text(text, size=512, overlap=50):
    chunks = []
    for i in range(0, len(text), size - overlap):
        chunk = text[i:i + size].strip()
        if chunk:
            chunks.append(chunk)
        if len(chunks) >= MAX_CHUNKS:
            break
    return chunks

def get_file_size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)

def main():
    print("Starting FAISS baseline pipeline...")

    OUTPUT_FAISS_DIR.mkdir(parents=True, exist_ok=True)
    model = SentenceTransformer(MODEL_NAME)

    all_chunks = []
    metadata = []
    chunk_counter = 0

    start_ingest = time.time()

    for pdf_path in tqdm(list(INPUT_DATA_DIR.glob("*.pdf")), desc="Processing PDFs"):
        text = extract_text_from_pdf(pdf_path)
        if not text:
            continue

        chunks = chunk_text(text, size=CHUNK_SIZE, overlap=OVERLAP)
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            metadata.append({
                "text": chunk,
                "source": pdf_path.name,
                "chunk_id": i
            })
        chunk_counter += len(chunks)
        # if chunk_counter >= MAX_CHUNKS:
        #     print(f"Reached {MAX_CHUNKS} chunks. Stopping early.")
        #     break

    end_ingest = time.time()
    print(f"Total chunks added: {len(all_chunks)}")

    print("Generating embeddings...")
    start_embed = time.time()
    embeddings = model.encode(all_chunks, show_progress_bar=True, convert_to_numpy=True)
    end_embed = time.time()

    print("Saving FAISS index...")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    index_path = OUTPUT_FAISS_DIR / "faiss_index.index"
    faiss.write_index(index, str(index_path))

    metadata_path = OUTPUT_FAISS_DIR / "metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print("\nFAISS baseline complete.\n")

    print(f"Ingestion time       : {end_ingest - start_ingest:.2f} sec")
    print(f"Embedding + Indexing : {end_embed - start_embed:.2f} sec")
    print("Output file sizes:")
    print(f"  FAISS index        : {get_file_size_mb(index_path):.2f} MB")
    print(f"  Metadata (JSON)    : {get_file_size_mb(metadata_path):.2f} MB")
    print(f"  Total              : {get_file_size_mb(index_path) + get_file_size_mb(metadata_path):.2f} MB")

    print("\nChunks per PDF:")
    from collections import Counter

    pdf_chunk_counts = Counter(entry["source"] for entry in metadata)
    print("\nChunks per PDF:")
    for fname, count in pdf_chunk_counts.items():
        print(f"  {fname}: {count} chunks")

    print("\nTotal time: {:.2f} sec".format((end_embed - start_embed) + (end_ingest - start_ingest)))

if __name__ == "__main__":
    main()
