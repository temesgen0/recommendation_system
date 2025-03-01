from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        # Use a multi-language model
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    def generate_embedding(self, text: str):
        return self.model.encode(text)