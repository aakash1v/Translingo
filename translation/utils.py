import os
import pytesseract
import textblob
from PIL import Image
from PyPDF2 import PdfReader
from transformers import T5Tokenizer, T5ForConditionalGeneration

# 🔹 Model for Summarization (Ensure it is installed properly)
MODEL_NAME = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

# ✅ Function to Extract Text from PDFs
def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    :param pdf_path: Path to the PDF file
    :return: Extracted text as a string
    """
    try:
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
            return text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

# ✅ Function to Extract Text from Images (OCR)
def read_image(image_path):
    """
    Extracts text from an image using OCR.
    :param image_path: Path to the image file
    :return: Extracted text as a string
    """
    try:
        image = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(image, lang="eng")
        return extracted_text.strip()
    except Exception as e:
        print(f"Error in reading image: {e}")
        return ""

# ✅ Function to Summarize Text
def summarize_parallel(input_text):
    """
    Summarizes the given text using a Transformer model.
    :param input_text: Raw input text
    :return: Summarized text
    """
    try:
        input_ids = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=512, truncation=True)
        summary_ids = model.generate(input_ids, max_length=500, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
        return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return input_text  # Return original if summarization fails
