from io import BytesIO
from flask import Flask, request, send_file, render_template
import subprocess
import os
import logging

app = Flask(__name__, static_folder='static')

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('PDFproject.html')

@app.route('/merge_pdfs', methods=['POST'])
def merge_pdfs():
    try:
        pdf_files = request.files.getlist('pdf_files[]')
        page_numbers = request.form.getlist('page_numbers[]')

        logger.info(f"Received files: {[f.filename for f in pdf_files]}")
        logger.info(f"Received page numbers: {page_numbers}")

        if not pdf_files or not page_numbers:
            return 'No files or page numbers provided', 400

        # Create a temporary directory to store the PDF files
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
        os.makedirs(temp_dir, exist_ok=True)

        # Save the uploaded PDF files to the temporary directory
        pdf_paths = []
        for file in pdf_files:
            file_path = os.path.join(temp_dir, file.filename)
            file.save(file_path)
            pdf_paths.append(file_path)

        # Call PDFproject.py to merge the PDFs
        output_path = os.path.join(temp_dir, 'output.pdf')
        page_numbers_str = ';'.join(page_numbers)
        logger.info(f"Calling PDFproject.py with page numbers: {page_numbers_str}")
        cmd = ['python', 'PDFproject.py', *pdf_paths, page_numbers_str, '-o', output_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"Error running PDFproject.py: {result.stderr}")
            return f'Error merging PDFs: {result.stderr}', 500

        # Send the merged PDF as a response
        with open(output_path, 'rb') as f:
            pdf_data = f.read()
        response = send_file(BytesIO(pdf_data), as_attachment=True, download_name='merged.pdf', mimetype='application/pdf')
        return response
    except Exception as e:
        logger.error('Error merging PDFs: %s', e)
        return f'Error merging PDFs: {str(e)}', 500
    
if __name__ == '__main__':
    app.template_folder = 'templates'
    app.run(debug=True)