import weaviate
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["NO_PROXY"] = "localhost,127.0.0.1"

client = weaviate.connect_to_local()

client.collections.delete("Books")

print("Коллекция успешно удалена!!")

client.close()