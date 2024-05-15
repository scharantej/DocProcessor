
# main.py

# Import required libraries
from flask import Flask, request, render_template, redirect
import PyPDF2
from gspread import service

# Initialize the Flask app
app = Flask(__name__)

# Define the upload route for handling PDF report uploads
@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded PDF reports from the request
    reports = request.files.getlist('reports')

    # Create a list to store the extracted data
    extracted_data = []

    # Parse each PDF report and extract the desired data
    for report in reports:
        # Open the report using PyPDF2
        pdf_reader = PyPDF2.PdfFileReader(report)

        # Get the text from the report
        text = pdf_reader.getPage(0).extractText()

        # Extract the data points
        date_submitted = text.split('Date:')[1].strip()
        report_number = text.split('Report Number:')[1].strip()
        amount_claimed = text.split('Amount Claimed:')[1].strip()
        patient_name = text.split('Patient Name:')[1].strip()
        treatment_type = text.split('Treatment Type:')[1].strip()

        # Append the extracted data to the list
        extracted_data.append([date_submitted, report_number, amount_claimed, patient_name, treatment_type])

    # Save the extracted data to a Google Sheet
    # Assuming you have authorized the app to access Google Sheets
    gc = service.Client()
    worksheet = gc.open('Report Data').sheet1

    # Append the extracted data to the worksheet
    worksheet.append_rows(extracted_data)

    # Redirect to the results page
    return redirect('/get_results')


# Define the route for displaying the extracted data
@app.route('/get_results')
def get_results():
    # Get the extracted data from the Google Sheet
    gc = service.Client()
    worksheet = gc.open('Report Data').sheet1

    # Get the data from the worksheet
    data = worksheet.get_all_values()

    # Render the results page
    return render_template('results.html', data=data)


# Define the export route for exporting the data to a file
@app.route('/export', methods=['POST'])
def export():
    # Get the export format from the request
    export_format = request.form.get('export_format')

    # Export the data to the specified format
    if export_format == 'google_sheet':
        # Save the extracted data to a Google Sheet
        # Assuming you have authorized the app to access Google Sheets
        gc = service.Client()
        worksheet = gc.open('Report Data').sheet1

        # Append the extracted data to the worksheet
        worksheet.append_rows(extracted_data)

    elif export_format == 'excel':
        # Save the extracted data to an Excel file
        import openpyxl

        # Create a new workbook
        workbook = openpyxl.Workbook()

        # Create a new worksheet
        worksheet = workbook.active

        # Add the extracted data to the worksheet
        worksheet.append(extracted_data)

        # Save the workbook
        workbook.save('report_data.xlsx')

    # Redirect to the results page
    return redirect('/get_results')


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
