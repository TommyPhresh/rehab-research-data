from sentence_transformers import SentenceTransformer, models
import os

MODEL_PATH = "D:\\Personal\\rehab-research-data\\models"

def verify_model():
    print("Checking for model in", MODEL_PATH)
    required_files = ["config.json", "pytorch_model.bin", "modules.json"]
    missing = [file for file in required_files if not os.path.exists(os.path.join(MODEL_PATH, file))]
    if missing:
        print("Missing files:", missing)
        return

    try:
        print("Time to load model")
        word_embedding_model = models.Transformer(MODEL_PATH, max_seq_length=256)
        pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
        model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
        print("Model loaded successfully")
        test_vec = model.encode(["test"])
        print("Test vector shape", test_vec.shape)
    except Exception as e:
        print("Error", e)

if __name__ == "main":
    verify_model()
