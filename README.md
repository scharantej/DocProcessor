## Flask Application Design

### HTML Files

- **form.html**: A simple HTML file containing a form for uploading multiple PDF reports.
- **results.html**: An HTML file that displays the extracted data from the uploaded reports in tabular format.

### Routes

- **upload**:
    - HTTP Method: POST
    - Accepts multiple PDF reports as input using a form data key called `reports`.
    - Parses the uploaded reports using a PDF parsing library (e.g., PyPDF2).
    - Extracts the desired data points from the reports.

- **get_results**:
    - HTTP Method: GET
    - Renders the `results.html` file.
    - Passes the extracted data to the `results.html` file.

- **export**:
    - HTTP Method: POST
    - Exports the extracted data to a Google Sheet or Excel file.
    - Uses a library like gspread or openpyxl for integration with Google Sheets or Excel.