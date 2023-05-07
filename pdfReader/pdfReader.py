import os
import sys
import re
from PIL import Image
from PyPDF2 import PdfFileReader
import ocrolib

# Set up OCRopus
ocrolib.tesseract_wrap.tesseract_available = True
ocrolib.tesseract_wrap.tesseract_cmd = "/usr/bin/tesseract"

# Define regex pattern to match hand-written text
handwriting_pattern = re.compile(r'^[a-z0-9\s,]+\n$', re.IGNORECASE)

# Define function to extract hand-written text from an image
def extract_handwriting(image_path):
    image = Image.open(image_path)
    image = image.convert('L')
    threshold = 200
    image = image.point(lambda p: p > threshold and 255)
    text = ocrolib.recognize.ocr(image)
    return text.strip()

# Define function to extract hand-written text from the second page of a PDF file
def extract_handwriting_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf_reader = PdfFileReader(f)
        if pdf_reader.numPages < 2:
            return ''
        page = pdf_reader.getPage(1)
        xObject = page['/Resources']['/XObject'].getObject()
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].getData()
                image = Image.frombytes('L', size, data)
                text = extract_handwriting(image)
                if handwriting_pattern.match(text):
                    return text
    return ''

# Define function to extract hand-written text from the second page of multiple PDF files
def extract_handwriting_from_pdf_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(directory, filename)
            text = extract_handwriting_from_pdf(pdf_path)
            if text:
                print(f'Handwriting in {pdf_path}: {text}')

# Call function to extract hand-written text from the second page of PDF files in a directory
extract_handwriting_from_pdf_files('/path/to/pdf/directory')
