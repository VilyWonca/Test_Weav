from services.pdf_parser import PDFParser

parser = PDFParser("books/")

print(parser.get_pdf_files())