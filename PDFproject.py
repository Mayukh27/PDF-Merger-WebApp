import PyPDF2
import os
import sys
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_pdf_paths_and_page_numbers(args):
    pdfs = args.pdfs
    page_numbers = args.page_numbers
    return pdfs, page_numbers
def create_new_pdf(pdfs, page_numbers, pdf_writer):
    page_numbers_list = page_numbers.split(';')
    if len(pdfs) != len(page_numbers_list):
        logger.error("Error: The number of PDFs and page numbers must be the same.")
        return

    logger.info(f"Received page numbers: {page_numbers_list}")

    for pdf, pages in zip(pdfs, page_numbers_list):
        if not os.path.exists(pdf):
            logger.error(f"Error: File '{pdf}' not found.")
            continue

        try:
            with open(pdf, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                logger.info(f"Reading PDF file '{pdf}' with {len(pdf_reader.pages)} pages")
                for page in [int(p) for p in pages.split(',')]:
                    if page <= 0 or page > len(pdf_reader.pages):
                        logger.error(f"Error: Page {page} does not exist in '{pdf}'.")
                        continue
                    logger.info(f"Extracting page {page} from '{pdf}'")
                    pdf_writer.add_page(pdf_reader.pages[page - 1])
        except Exception as e:
            logger.error(f"Error: Unable to read '{pdf}'. {str(e)}")
            continue
def main():
     parser = argparse.ArgumentParser(description='Merge PDFs')
     parser.add_argument('pdfs', type=str, nargs='+', help='Paths to PDF files')
     parser.add_argument('page_numbers', type=str, help='Page numbers to extract from each PDF ( comma separated)')
     parser.add_argument('-o', '--output', type=str, required=True, help='Output PDF file path')

     args = parser.parse_args()

     if not args.pdfs:
        print("No PDF files provided")
        return 1
     pdfs, page_numbers = get_pdf_paths_and_page_numbers(args)
     pdf_writer = PyPDF2.PdfWriter()

     create_new_pdf(pdfs, page_numbers, pdf_writer)

     with open(args.output, 'wb') as f:
        pdf_writer.write(f)

     logger.info(f"New PDF created successfully and saved to {args.output}!")

if __name__ == "__main__":
    main()