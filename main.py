from services.embedder import Embedder
from services.pdf_parser import PDFParser
from services.wv_uploader import WeaviateUploader
import os

def main():
    parser = PDFParser(folder_path= "books/")
    embedder = Embedder(model_name= "text-embedding-3-small")
    uploader = WeaviateUploader(collection_name= "Books")

    list_pdf = parser.get_pdf_files()
    
    for file_path in list_pdf:
        chunks_dict = parser.parse_and_chunk(file_path, max_tokens=500)
        name_file = os.path.basename(file_path)

        name_book = str(name_file.split("...")[0].strip())
        name_author = str(name_file.split("...")[1].replace(".pdf ", "").strip())

        list_chunks = []

        for chunk in chunks_dict:
            list_chunks.append(chunk["text"])

        embeddings = embedder.embed_text(list_chunks)
        uploader.create_collection()
        for i, (page, chunk, embedding) in enumerate(zip(chunks_dict, list_chunks, embeddings)):
            uploader.upload_chunk(
                name_book= name_book,
                author= name_author,
                text=chunk,
                page=page["page_num"],
                embedding=embedding
            )
        print(f"Загрузка текста из книги: {name_file} окончена. Переходим к следующей.")

    
    print(f"Загрузка текста из ПОСЛЕДНЕЙ книги окончена. Закрываем соединение.")
    uploader.close()

if __name__ == "__main__":
    main()
    



