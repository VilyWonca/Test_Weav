import pymupdf


class PDFParser:
    def __init__(self, file_name: str):
        self.file_name = file_name
    
    def clean_text(self, text: str) -> str:
        text = text.replace('\n', '').replace('\r', '').replace('\t', '').replace('\xa0', '')
        return text

    def extract_text(self) -> list[str]:
        try:
            doc = pymupdf.open(self.file_name)
            
        except Exception as e:
            print(f"Возникла ошибка при открытии файла: {e}")
            return []
        out = []
        for page in doc:
            text = page.get_text()
            clear_text = self.clean_text(text)
            out.append(clear_text)
        doc.close()
        return out
    
    def chunk_text(self, text: str, max_length: int = 500, overlap:  int = 50) -> list[str]:
        chunks = []
        start = 0
        while start < len(text):
            chunk = text[start:start + max_length]
            chunks.append(chunk)
            start += max_length - overlap
        return chunks
    
    def parse_and_chunk(self, max_length: int = 500, overlap:  int = 50) -> list[str]:
        list_text = self.extract_text()

        if not list_text:
            return []

        text = " ".join(list_text)
        clean_text = self.clean_text(text)
        chunks = self.chunk_text(clean_text, max_length=max_length, overlap=overlap)
        return chunks

        

            

    