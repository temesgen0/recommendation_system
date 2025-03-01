import faiss
import numpy as np

class FAISSDB:
    def __init__(self, dimension: int = 384):  # 384 is the dimension of the multilingual model
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity search
        self.product_ids = []

    def upsert_embedding(self, product_id: int, embedding: list):
        embedding = np.array(embedding, dtype="float32").reshape(1, -1)
        self.index.add(embedding)
        self.product_ids.append(product_id)

    def query_similar(self, embedding: list, top_k: int = 5):
        embedding = np.array(embedding, dtype="float32").reshape(1, -1)
        distances, indices = self.index.search(embedding, top_k)
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx != -1:  # FAISS returns -1 for invalid indices
                results.append({"product_id": self.product_ids[idx], "score": float(distance)})
        return results