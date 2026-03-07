import os, pickle, faiss, numpy as np
from sentence_transformers import SentenceTransformer, models

from constants import MODEL_PATH, INDEX_PATH, MAPPING_PATH

'''
Loads model from disk for downstream calculations
'''
def load_resources():
    word_embedding_model = models.Transformer(MODEL_PATH, max_seq_length=256)
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
    model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
    index = faiss.read_index(INDEX_PATH)
    with open(MAPPING_PATH, 'rb') as file:
        mapping = pickle.load(file)
    return model, index, mapping

'''
Vectorize search query and perform simple similarity search
'''
def search(query, model, index, mapping, top_k=25):
    query_vector = model.encode([query])
    faiss.normalize_L2(query_vector)
    distances, indices = index.search(query_vector.astype('float32'), top_k)
    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1:
            item = mapping[idx].copy()
            item['score'] = float(distances[0][i])
            results.append(item)
    return results

if __name__ == "main":
    model, index, mapping = load_resources()
    while True:
        user_query = input("\nEnter search term (or q to quit): ")
        if user_quer.lower() == "q":
            break
        results = search(user_query, model, index, mapping)
        for i, result in enumerate(results, 1):
            name = result.get('name', 'N/A')
            org = result.get('org', 'N/A')
            score = round(result['score'] * 100, 2)
            print(f"{i}. [{score}% Match] {name} ({org})")