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
            SELECT name, org, "desc", deadline, link, isGrant, id
            FROM funding
            WHERE id IN ({id_list_strings})
            """
        rows = self.conn.execute(query).fetchall()
        final_results = []
        for row in rows:
            row_list = list(row)
            row_id = row_list[6]
            score = results.get(row_id, 0.0)
            final_row = [
                row_list[0], # name
                row_list[1], # org
                row_list[2], # desc
                row_list[3], # deadline
                row_list[4], # link
                row_list[5], # isGrant
                score
            ]
            final_results.append(final_row)
        return sorted(final_results, key=lambda x: x[6], reverse=True)