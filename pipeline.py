import hashlib, pandas as pd, faiss, duckdb
from sentence_transformers import SentenceTransformer

import scrapers

def get_new_data():
    df_fpmr = scrapers.fpmr.scrape_fpmr()
    df_neilsen = pd.DataFrame(scrapers.neilsen.scrape_neilsen())
    df_pcori = pd.DataFrame(scrapers.pcori.scrape_pcori())
    df_nidilrr = pd.DataFrame(scrapers.nidilrr.scrape_nidilrr())
    df_pva = scrapers.pva.scrape_pva()
    df_acrm = pd.DataFrame(scrapers.acrm.scrape_acrm())
    
    df_final = pd.concat([df_fpmr, df_neilsen, df_pcori,
                          df_nidilrr, df_pva, df_acrm])
    df_final = df_final.drop_duplicates(subset=['id']).reset_index(drop=True)
    df_final = df_final.sort_values('id').reset_index(drop=True)
    df_final.to_parquet("data/new_data.parquet")
    return df_final

def update_master_records(new_data):
    try:
        old_df = pd.read_parquet("data/data.parquet")
    except FileNotFoundError:
        old_df = pd.DataFrame()

    new_df = pd.DataFrame(new_data)
    combined_df = pd.concat([old_df, new_df])
    combined_df = df_combined.drop_duplicates(subset=['id'], keep='last')
    combined_df.to_parquet("data/data.parquet")
    return combined_df

def build_files(df):
    df['search_blob'] = df['name'] + '' + df['org'] + '' + df['desc']
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(df['search_blob'].to_list(), batch_size=64)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    faiss.write_index(index, "index/embeddings.index")
    conn = duckdb.connect("data/rehab-research-v2.db")
    conn.execute("CREATE TABLE funding AS SELECT * FROM df")
    conn.close()