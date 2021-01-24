# Tesseract Optical Character Recognition

Setup
----------
Install Tesseract through [brew](https://formulae.brew.sh/formula/tesseract)

    brew install tesseract

Install Python [Libraries](https://pypi.org/project/pytesseract/)

    pip install -r tesseract_ocr/requirements.txt

Run Locally
----------
Call the OCR script

     python -m tesseract_ocr.reader -i <image_file>
