import PyPDF2
# from .models import PDFModel

def pdf_text(pdf_path):
    with open(f'./static/images/{pdf_path}', 'rb') as pdfFileObj:
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        pageObj = pdfReader.pages[0]  # Access the first page
        text = pageObj.extract_text()
    
    return text

# Specify the name of your PDF file (not the full path)
pdf_file_name = 'your_pdf_file.pdf'  # Replace with the actual PDF file name
pdf = pdf_text(pdf_file_name)
print(pdf)
