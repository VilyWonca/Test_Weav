import pymupdf
import pymupdf4llm
import os
from sentence_transformers import SentenceTransformer, util
import nltk
import numpy as np
from markitdown import MarkItDown


class PDFParser:
    def __init__(self, folder_path: str, model_name='all-MiniLM-L6-v2'):
        self.folder_path = folder_path
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        self.model = SentenceTransformer(model_name
                                         
                                         )
    def get_pdf_files(self) -> list[str]:

        result = [os.path.join(self.folder_path, file)
                  for file in os.listdir(self.folder_path)
                  if file.lower().endswith(".pdf")]
        
        return result


    def clean_text(self, text: str) -> str:
        text = text.replace('\n', ' ').replace('\r', '').replace('\t', '').replace('\xa0', '').replace('\xa0', '')
        return text

    def extract_text(self, file_name: str) -> list[dict]:
        try:
            doc = pymupdf.open(file_name)  
        except Exception as e:
            print(f"Возникла ошибка при открытии файла: {e}")
            return []
        
        out = []

        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            clear_text = self.clean_text(text)
            out.append({
                "text": clear_text,
                "page_num": page_num
            })
        doc.close()
        return out
    
    def semantic_chunk(self, text: str, max_tokens: int, similarity_threshold: float):

        sentences = nltk.sent_tokenize(text)
        if not sentences:
            return []
        
        embeddings = self.model.encode(sentences)

        chunks = []
        current_chunk = [sentences[0]]
        current_embedding = embeddings[0]
        current_len = len(sentences[0])

        for i in range(1, len(sentences)):
            sentence = sentences[i]
            sentence_embedding = embeddings[i]
            sentence_len = len(sentence)

            similarity = util.cos_sim(current_embedding, sentence_embedding).item()

            if (current_len + sentence_len <= max_tokens) and (similarity >= similarity_threshold):
                current_chunk.append(sentence)
                current_len += sentence_len
                # обновим среднее представление чанка
                current_embedding = (current_embedding + sentence_embedding) / 2
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_embedding = sentence_embedding
                current_len = sentence_len

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks


    def parse_and_chunk(self, file_path: str, max_tokens: int = 500) -> list[str]:

        list_dict = self.extract_text(file_name=file_path)
        if not list_dict:
            return []
        
        chunks = []

        for page in list_dict:
            chunks_page = self.semantic_chunk(page["text"], max_tokens, 0.3)
            for chunk in chunks_page:
                print("Сейчас пока прасим страницы:", page["page_num"])
                if len(chunk) < 100:
                    continue 
                chunks.append({
                    "text": chunk,
                    "page_num": page["page_num"] 
                })

        return chunks