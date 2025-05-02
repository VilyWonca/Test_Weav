import weaviate

class WeaviateSearcher:
    def __init__(self):
        self.client = weaviate.connect_to_local()
    
    def search(self, query: str, top_k: int, name_collection: str) -> list[str]:
        collection = self.client.collections.get(name_collection)
        response = collection.query.near_text(
            query = query,
            limit = top_k
            )

        result = [o.properties["text"] for o in response.objects]
        return result
    
    def close (self):
        self.client.close()
        print("Соединение с Weaviate успешно прервано")