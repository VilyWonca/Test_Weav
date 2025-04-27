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
    