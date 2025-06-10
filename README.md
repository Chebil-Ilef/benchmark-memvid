# Memvid Benchmark Suite

This repository benchmarks the [Memvid](https://github.com/Olow304/memvid) video-based AI memory system for document ingestion and semantic retrieval.

It includes ingestion and retrieval scripts, test queries, and evaluation results compared with FAISS.

---

## Structure

```

.
├── data\_memvid/           # Output files from Memvid (video, index)
├── data\_faiss/            # Output files from FAISS (index, metadata)
├── documents/             # PDF source documents (short/long/energy)
├── test\_queries/          # Query sets for each document collection
├── ingest\_memvid.py       # Memvid ingestion script
├── retriever\_memvid.py    # Memvid retrieval benchmark script
├── faiss\_benchmark.py     # FAISS ingestion + retrieval script
├── benchmark.md           # Detailed benchmark results and analysis
├── requirements.txt       # Python dependencies
└── README.md              # You're here :)

````

---

## Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
````

---

## Usage

### 1. Ingest Documents (Memvid)

```bash
python ingest_memvid.py
```

* Reads from `./documents/`
* Outputs to `./data_memvid/`
* Supports chunk size and overlap customization in code

### 2. Run Retrieval Benchmark (Memvid)

```bash
python retriever_memvid.py
```

* Queries come from files in `./test_queries/`
* Runs multiple repetitions for timing analysis
* Logs retrieved chunks per query

### 3. Benchmark FAISS (Baseline)

```bash
python faiss_benchmark.py
```

* Uses same document and query sets
* Produces FAISS index and metadata
* Logs ingestion, embedding time, and sizes

---

## Benchmark Results

See [`benchmark.md`](./benchmark.md) for full performance breakdown:

* Ingestion time
* Storage footprint
* Retrieval speed
* Quality issues and manual score analysis

---

## Notes 

as for June 2025 :

* Memvid does **not** expose similarity scores → reranking and debugging are limited.
* Retrieval quality suffers from hard chunk breaks → many chunks are cut mid-sentence or word.
* Video encoding is **very slow** for long documents.
* Old documentation , not maintained