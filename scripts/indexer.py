import os, json, pickle, hashlib, faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
from constants import MODEL_NAME, DATA_DIR, INDEX_PATH, MAPPING_PATH, MANIFEST_PATH

'''
Lightweight model load for limited machine architectures
'''
def load_model():
    word_embedding_model = models.Transformer(MODEL_NAME, max_seq_length=256)
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
    return SentenceTransformers(modules=[word_embedding_model, pooling_model])

'''
Initial index for 10/2025 baseline dataset
'''
def create_initial_index(batch_size=64):
    df = pd.read_parquet(os.path.join(DATA_DIR, "data.parquet")
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
