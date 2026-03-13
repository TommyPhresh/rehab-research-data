import duckdb, faiss, numpy as np
from sentence_transformers import SentenceTransformer

class SearchEngine:
    def __init__(self, db_path, index_path, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = faiss.read_index(index_path)
        self.db_path = db_path
        self.conn = duckdb.connect(self.db_path, read_only=True)

    def search(self, query_text, top_k=5000, threshold=0.5):
        query_vector = self.model.encode([query_text])
        faiss.normalize_L2(query_vector)
        scores, indices = self.index.search(query_vector.astype('float32'), top_k)
        results = {
            int(idx): float(score)
            for idx, score in zip(indices[0], scores[0])
            if score >= threshold
        }
        if not results: return []

        target_ids = list(results.keys())
        id_list_strings = ",".join(map(str, target_ids))
        query = f"""
            SELECT name, org, desc, due_date, id, link, isGrant
            FROM funding
            WHERE id IN ({id_list_strings})
            """
        rows = self.conn.execute(query).fetch_all()
        final_results = []
        for row in rows:
            row_list = list(row)
            row_id = row_list[4]
            row_list[4] = results.get(row_id, 0.0)
            final_results.append(row_list)
        return final_results.sort(key=lambda x: x[4], reverse=True)
