from pypdf import PdfReader


def extract_text(file_path):

    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text()

        return text

    raise ValueError("Unsupported file type")