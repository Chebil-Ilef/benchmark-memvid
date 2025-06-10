import os
import time
from pathlib import Path
from memvid import MemvidEncoder
from tqdm import tqdm
import pdfplumber

INPUT_DATA_DIR = Path("./documents/reports")
OUTPUT_MEMVID_DIR = Path("./data_memvid/reports")
CHUNK_SIZE = 512
OVERLAP = 50
MAX_CHUNKS_TO_PROCESS = 1000


import logging

logging.basicConfig(filename="ingestion.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("pdfminer").setLevel(logging.ERROR)


def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return "\n".join(
                page.extract_text() or "" for page in pdf.pages
            ).strip()
    except Exception as e:
        print(f"Error reading PDF {pdf_path.name}: {e}")
        return ""

def get_file_size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)

def main():
    print("Starting Memvid ingestion...")
    OUTPUT_MEMVID_DIR.mkdir(parents=True, exist_ok=True)
    encoder = MemvidEncoder()

    print(f"Chunk size: {CHUNK_SIZE}, Overlap: {OVERLAP}")
    pdf_files = list(INPUT_DATA_DIR.glob("**/*.pdf"))
    if not pdf_files:
        print("No PDFs found. Exiting.")
        return

    print(f"Found {len(pdf_files)} PDF files to process.")

    total_chunks = 0
    per_file_chunk_counts = {}

    start_ingest = time.time()

    for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
        text = extract_text_from_pdf(pdf_file)
        pre_chunk_count = len(encoder.chunks)
        if text:
            encoder.add_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP)
            post_chunk_count = len(encoder.chunks)
            new_chunks = post_chunk_count - pre_chunk_count
            per_file_chunk_counts[pdf_file.name] = new_chunks
            total_chunks += new_chunks
        else:
            print(f"Skipped empty: {pdf_file.name}")

        # if total_chunks >= MAX_CHUNKS_TO_PROCESS:
        #     print(f"Reached {MAX_CHUNKS_TO_PROCESS} chunks. Stopping early.")
        #     break

    end_ingest = time.time()

    if not encoder.chunks:
        print("No chunks created. Aborting.")
        return

    print(f"Total chunks added: {total_chunks}")
    print(f"Ingestion time: {end_ingest - start_ingest:.2f} seconds")

    print("Building video memory and index...")
    video_path = OUTPUT_MEMVID_DIR / "memvid_memory.mp4"
    index_path = OUTPUT_MEMVID_DIR / "memvid_index.json"

    start_build = time.time()
    encoder.build_video(str(video_path), str(index_path))
    end_build = time.time()

    print(f"Video build time: {end_build - start_build:.2f} seconds")
    print("Output file sizes:")
    print(f"  Video file  : {get_file_size_mb(video_path):.2f} MB")
    print(f"  Index (JSON): {get_file_size_mb(index_path):.2f} MB")
    print(f"  Total       : {get_file_size_mb(video_path) + get_file_size_mb(index_path):.2f} MB")

    print("\nChunks per PDF:")
    for fname, count in per_file_chunk_counts.items():
        print(f"  {fname}: {count} chunks")

    print("\nIngestion complete.")

if __name__ == "__main__":
    main()
