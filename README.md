# PDF Merger Web Application

This web application allows users to merge multiple PDF files and select specific pages from each PDF to create a new combined PDF document.

## Features

- Upload multiple PDF files
- Specify page numbers to extract from each PDF
- Merge selected pages into a single PDF
- Download the merged PDF file

## Technologies Used

- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- PDF Processing: PyPDF2

## Setup and Installation

1. Clone the repository:
git clone https://github.com/Mayukh27/pdf-merger-webapp.git cd pdf-merger-webapp

2. Install the required Python packages:
pip install flask PyPDF2

3. Run the Flask application:
python app.py

Edit
Copy code

4. Open a web browser and navigate to `http://localhost:5000` to use the application.

## How to Use

1. Enter the number of PDFs you want to merge.
2. Click the "Add PDFs" button to generate input fields for each PDF.
3. For each PDF:
- Select the PDF file using the file input.
- Enter the page numbers you want to extract (comma-separated).
4. Click the "Download Merged PDF" button to process and download the merged PDF.

## Project Structure

- `app.py`: Main Flask application file
- `PDFproject.py`: PDF processing script
- `templates/`: Contains HTML templates
- `PDFproject.html`: HTML template for the web interface
- `static/`: Contains static files
- `styles.css`: CSS styles for the web interface

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
