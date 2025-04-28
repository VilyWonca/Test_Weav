import os

os.environ["NO_PROXY"] = "localhost,127.0.0.1"

import ollama

class Embedder:
    def __init__(self,  model_name: str):
        self.model_name = model_name
    
    def embed_text(self, chunks: list[str]) -> list[list[float]]:
        embeddings = []
        for chunk in chunks:
            response = ollama.embed(model=self.model_name, input=chunk)
            embeddings.append(response['embeddings'][0])
        return embeddings
    
