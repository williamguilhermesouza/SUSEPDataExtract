import ocrmypdf

## This class was introduced as a way to parse the scanned documents to text
# so we can extract data from them
def main(pdf_name):
    ocrmypdf.ocr(pdf_name, pdf_name)

if __name__ == '__main__':  # To ensure correct behavior
    ocrmypdf.ocr('10.001828-00-21.pdf', 'ocred.pdf', deskew=True)
