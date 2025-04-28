from services.embedder import Embedder
from services.pdf_parser import PDFParser
from services.weaviate_uploader import WeaviateUploader

def main():
    parser = PDFParser(file_name= "books/Базы данных. Практикум ... С.В. Калиниченко.pdf")
    embedder = Embedder(model_name= "nomic-embed-text:latest")
    uploader = WeaviateUploader(collection_name= "Books")

    chunks = parser.parse_and_chunk(max_length=500, overlap=50)

    embeddings = embedder.embed_text(chunks)

    uploader.create_collection()

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings), start=1):
            uploader.upload_chunk(
                name_book="Базы данных. Практикум",
                author="С.В. Калиниченко",
                text=chunk,
                page=i,
                embedding=embedding
            )

    print("Все данные загружены")
    uploader.close()

if __name__ == "__main__":
    main()
    



