from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")

def create_embedding(content):
    return model.encode(content).tolist()


