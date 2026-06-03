from pathlib import Path

import os
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
RAG_DATA_DIR = DATA_DIR / "rag"

DATABASE_DIR = BASE_DIR / "database"
SQLITE_DB_PATH = DATABASE_DIR / "champions_league.db"

RAG_CORPUS_PATH = RAG_DATA_DIR / "ucl_rag_corpus.json"

RAG_INDEX_DIR = BASE_DIR / "rag_index"
FAISS_INDEX_PATH = RAG_INDEX_DIR / "index.faiss"
DOCUMENTS_PATH = RAG_INDEX_DIR / "documents.pkl"
METADATA_PATH = RAG_INDEX_DIR / "metadata.pkl"
USE_LLM = os.getenv("USE_LLM", "false").lower() == "true"
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "Qwen/Qwen2.5-3B-Instruct")