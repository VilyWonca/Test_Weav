import weaviate
from weaviate.classes.config import Configure, Property, DataType


class WeaviateUploader:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.client = weaviate.connect_to_local()

    def create_collection(self,):

       collections = self.client.collections.list_all(simple=False)

       if self.collection_name in collections.keys():
            print(f"Collection '{self.collection_name}' already exists.")
            return
       
       self.client.collections.create(
            name= self.collection_name,
            properties=[
                Property(name="name_book", data_type=DataType.TEXT),
                Property(name="text", data_type=DataType.TEXT),
                Property(name="author", data_type=DataType.TEXT),
                Property(name="page", data_type=DataType.INT)
            ],
            vectorizer_config=Configure.Vectorizer.text2vec_openai(
                model="text-embedding-3-small"
            ),
            generative_config=Configure.Generative.openai(
                model="gpt-3.5-turbo"
            )                                      
        )

    def upload_chunk(self, name_book: str, author: str, text: str, page: int, embedding: list[float]):

        collection = self.client.collections.get(self.collection_name)

        uuid = collection.data.insert({
            "name_book": name_book,
            "author": author,
            "text": text,
            "page": page,
        },
        vector=embedding
        )

        print(f"Вставили этот чанк: {uuid}") 

    def close(self):
        self.client.close()
        print('Соединение с Weaviate остановлено.')


