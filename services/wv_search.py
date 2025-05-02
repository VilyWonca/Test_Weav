import weaviate

class WeaviateSearcher:
    def __init__(self):
        self.client = weaviate.connect_to_local()
    
    def search(self, query: str, top_k: int, name_collection: str) -> list[dict]:
        collection = self.client.collections.get(name_collection)
        response = collection.query.near_text(
            query = query,
            limit = top_k
            )
        result = []

        for o in response.objects:
            text = o.properties["text"]
            author = o.properties["author"]
            name_book = o.properties["name_book"]
            page = o.properties["page"]
            
            result.append({
                "text": text,
                "author": author,
                "name_book": name_book,
                "page": page,
            })

        return result
    
    def close (self):
        self.client.close()
        print("Соединение с Weaviate успешно прервано")