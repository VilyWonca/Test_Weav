from services.wv_search import WeaviateSearcher

parser = WeaviateSearcher()

print(parser.search("Что такое драйвер?", 2, "Books"))