import weaviate

client = weaviate.connect_to_local()

client.collections.delete("Books")

print("Коллекция успешно удалена!!")

client.close()