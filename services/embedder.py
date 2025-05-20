import os

os.environ["NO_PROXY"] = "localhost,127.0.0.1"

from openai import OpenAI

class Embedder:
    def __init__(self,  model_name: str, batch_size: int = 100):
        self.model_name = model_name
        self.client = OpenAI()
        self.batch_size = batch_size
    
    def embed_text(self, chunks: list[str]) -> list[list[float]]:
        embeddings = []
        total = len(chunks)
        
        for start in range(0, total, self.batch_size):
            end = min(start + self.batch_size, total)

            batch = chunks[start:end]

            response = self.client.embeddings.create(
                    model=self.model_name,
                    input=batch,
                    encoding_format="float"
                    )

            for i, item in enumerate(response.data, start=start + 1):
                embeddings.append(item.embedding)
                print("Добили чанк под номером:", i)
        return embeddings
    
