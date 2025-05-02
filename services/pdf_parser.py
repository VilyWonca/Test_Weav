import pymupdf
import os


class PDFParser:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
    
    def get_pdf_files(self) -> list[str]:

        result = [os.path.join(self.folder_path, file)
                  for file in os.listdir(self.folder_path)
                  if file.lower().endswith(".pdf")]
        
        return result


    def clean_text(self, text: str) -> str:
        text = text.replace('\n', '').replace('\r', '').replace('\t', '').replace('\xa0', '')
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
    
    def parse_and_chunk(self, file_path: str, max_length: int = 500, overlap:  int = 50) -> list[str]:

        list_dict = self.extract_text(file_name=file_path)
        if not list_dict:
            return []
        
        chunks = []
        for i in list_dict:
            start = 0
            while start < len(i["text"]):
                chunk = i["text"][start:start + max_length]
                chunks.append({
                        "text": chunk,
                        "page_num": i["page_num"]
                    })
                start += max_length - overlap

        return chunks