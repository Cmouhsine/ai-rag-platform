from app.rag.loader import PDFLoader


class DocumentIngestionService:

    def __init__(self):

        self.loader = PDFLoader()

    def extract_text(self, path: str):

        return self.loader.load(path)