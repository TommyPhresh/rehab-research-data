import os

MODEL_NAME = "all-MiniLM-L6-v2"

BASE_DIR = "D:/Personal/rehab-research-data"
DATA_DIR = os.path.join(BASE_DIR, "data")
INDEX_DIR = os.path.join(BASE_DIR, "index")
MODEL_PATH = os.path.join(BASE_DIR, "models")

MANIFEST_PATH = os.path.join(INDEX_DIR, "sources.json")
INDEX_PATH = os.path.join(INDEX_DIR, "embeddings.index")
MAPPING_PATH = os.path.join(INDEX_DIR, "mapping.pkl")

os.makedirs(INDEX_DIR, exist_ok=True)
