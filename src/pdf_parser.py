import pymupdf


class PDFParser:
    def __init__(self, file_name: str):
        self.file_name = file_name
    
    def clean_text(text: str) -> str:
        

    def extract_text(self, file_name: str) -> list[str]:
        doc = pymupdf.open(file_name)
        out = []
        for page in doc:
            text = page.get_text().encode("utf-8")
            out.append(text)
        return out