import os

os.environ["NO_PROXY"] = "localhost,127.0.0.1"

from openai import OpenAI
client = OpenAI()

class Embedder:
    def __init__(self,  model_name: str):
        self.model_name = model_name
    
    def embed_text(self, chunks: list[str]) -> list[list[float]]:
        embeddings = []
        for chunk in chunks:
            response = client.embeddings.create(
                model=self.model_name,
                input=chunk,
                encoding_format="float"
                )
            embeddings.append(response['embeddings'][0])
        return embeddings
    
