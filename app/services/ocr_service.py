from PIL import Image
import pytesseract
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(file_path):

    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)

    return text


def extract_text_from_scanned_pdf(file_path):

    from pdf2image import convert_from_path

    pages = convert_from_path(
        file_path,
        poppler_path=r"C:\poppler-25.12.0\Library\bin"
    )

    full_text = ""

    for page in pages:
        text = pytesseract.image_to_string(page)
        full_text += text + "\n"

    return full_text