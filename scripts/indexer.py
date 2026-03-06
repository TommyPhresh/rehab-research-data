import os, json, pickle, hashlib, faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

BASE_DIR = "D:/Personal/rehab-research-data"
DATA_DIR = os.path.join(BASE_DIR, "data")
INDEX_DIR = os.path.join(BASE_DIR, "index")
MODEL_PATH = os.path.join(BASE_DIR, "models")

MANIFEST_PATH = os.path.join(INDEX_DIR, "sources.json")
INDEX_PATH = os.path.join(INDEX_DIR, "embeddings.index")
MAPPING_PATH = os.path.join(INDEX_DIR, "mapping.pkl")

os.makedirs(INDEX_DIR, exist_ok=True)
df = pd.read_parquet(os.path.join(DATA_DIR, "data.parquet"))

'''
Lightweight model load for limited machine architectures
'''
def load_model():
    word_embedding_model = models.Transformer(MODEL_NAME, max_seq_length=256)
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
    return SentenceTransformers(modules=[word_embedding_model, pooling_model])

'''
Creates embeddings for legacy dataset to establish baseline
'''
def create_initial_index(df, batch_size=64):
    df = df.fillna('')
    df['search_blob'] = df['name'] + ' ' + df['org'] + ' ' + df['desc']
    model = load_model()

    print('Generating embeddings')
    embeddings = model.encode(
        df['search_blob'].to_list(),
        batch_size=batch_size,
        show_progress_bar=True
    )

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)
    mapping = df.drop(columns=['search_blob']).to_dict('records')

    with open(MAPPING_PATH, 'wb') as file:
        pickle.dump(mapping, file)
    with open(MANIFEST_PATH, 'w') as file:
        json.dump({'total_rows': len(df), 'status': 'ready'}, file)
    print('Success')
