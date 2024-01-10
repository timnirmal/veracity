from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io

pdf_path = 'clip.pdf'

def extract_text_and_tables(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as pdf_file:
        for page in PDFPage.get_pages(pdf_file):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # Now, 'text' contains the extracted text, including tables.
    return text

extracted_text = extract_text_and_tables(pdf_path)

print(extracted_text)






# import PyPDF2
#
# pdf_path = 'clip.pdf'
#
# pdf_text = ''
# with open(pdf_path, 'rb') as pdf_file:
#     pdf_reader = PyPDF2.PdfReader(pdf_file)
#     for page_num in range(len(pdf_reader.pages)):
#         page = pdf_reader.pages[page_num]
#         pdf_text += page.extract_text()
#
#
# print(pdf_text)


# ! pip install pdfminer.txt.six
# ! pip install PyPDF2



# import tabula
#
# pdf_path = 'clip.pdf'
#
# # Extract tables from PDF and return them as DataFrame(s)
# tables = tabula.read_pdf(pdf_path, pages='all')
#
# # 'tables' will contain a list of DataFrames, one for each page with tables.
# print(tables)
#
#
#
#
#
# # ! pip install tabula-py
# # ! pip install pdfminer.txt.six
# # ! pip install PyPDF2