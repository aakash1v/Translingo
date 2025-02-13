from PIL import Image
from pytesseract import pytesseract
from pdfminer.high_level import extract_text

def readPdf(filename):
    text = extract_text(filename)
    return text

def readImage(image_path):

    # path_to_tesseract = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    path_to_tesseract = "/usr/bin/tesseract" # for linux...


    img = Image.open(image_path)
    pytesseract.tesseract_cmd = path_to_tesseract
    text = pytesseract.image_to_string(img)

    return str(text)