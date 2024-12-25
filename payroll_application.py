from flask import Flask, request, jsonify
from data_model import db, FileData, EmployeeData
from utils import format_amount_paid, get_pay_period
import csv
import sys


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.app_context().push()
db.create_all()


# API to handle csv file upload
@app.route('/upload-file', methods=['POST'])
def upload_file(file):

    # If no file is present in the input
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    # get the file object from the input request
    file = request.files['file']







def parse_file(file_data):

    file=open(file_data,'r')

    print('Filename  ',file)

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400


    # If file is present and file is of .csv format
    if file and file.filename.endswith('.csv'):

        # Check if file with the same name already exists
        existing_file = FileData.query.filter_by(filename=file.filename).first()

        # If file is existing, return file already exists message
        if existing_file:
            return jsonify({'message': 'File already exists'}), 409


        # Save the file to the database
        new_file = FileData(filename=file.filename, data=file.read())
        db.session.add(new_file)
        db.session.commit()

        # Go to the start of the file
        file.stream.seek(0)


        csv_reader = csv.reader(file.stream.read().decode('utf-8').splitlines())

        # Skip the row header of csv file
        next(csv_reader)

        for row in csv_reader:
            employee_row = EmployeeData(date=row[0], hours_worked=row[1], employee_id=row[2], job_group=row[3])
            db.session.add(employee_row)


        db.session.commit()

        return jsonify({'message': 'File successfully uploaded and saved'}), 200
    else:
        return jsonify({'error': 'Only CSV files are allowed'}), 400


# API to return all the data in the database
@app.route('/get-data', methods=['GET'])
def retrieve_report():
    # Query all rows from the CSVData table
    csv_data = EmployeeData.query.all()

    # Convert the data to a list of dictionaries
    result = []
    for row in csv_data:
        row_dict = {
            'id': row.id,
            'date': row.date,
            'hours worked': row.hours_worked,
            'employee id': row.employee_id,
            'job group': row.job_group
        }
        result.append(row_dict)

    return jsonify(result), 200




# API to get payroll report of employees in the database
@app.route('/get-payroll-report', methods=['GET'])
def get_payroll_report():


    # Hourly rates for job groups
    hourly_rates = {'A': 20.00, 'B': 30.00}

    # Query all work data and organize it by employee and pay period
    work_data = EmployeeData.query.all()


    # Dictionary to store the payroll data
    # Key is (employee_id, start_date, end_date)
    payroll_data = {}


    # Iterate over all the data
    for entry in work_data:

        employee_id = entry.employee_id

        # get start and end date based on the date given
        pay_period = get_pay_period(entry.date)

        # store (employee_id, start_date, end_date) as key for an employee to get amount paid
        pay_period_key = (employee_id, pay_period['startDate'], pay_period['endDate'])

        # if pay_period_key not in payroll_data dictionary, make an entry
        if pay_period_key not in payroll_data:
            payroll_data[pay_period_key] = {
                'employeeId': employee_id,
                'payPeriod': pay_period,
                'amountPaid': 0.0
            }


        # compute amount paid based on hours worked and hourly rates
        payroll_data[pay_period_key]['amountPaid'] += entry.hours_worked * hourly_rates[entry.job_group]


    # format amount paid after processing all data
    format_amount_paid(payroll_data)

    #filter those employees who were not paid
    result = {k: v for k, v in payroll_data.items() if v['amountPaid'] != '$0.00'}

    # Convert the payroll data to the desired JSON format
    payroll_report = {
        'payrollReport': {
            'employeeReports': sorted(result.values(), key=lambda x: (x['employeeId'], x['payPeriod']['startDate']))
        }
    }


    # return json string of payroll data and http code
    return jsonify(payroll_report), 200



def save_file(file):

    if not file:
        return 'Please enter file'


    parse_file(file)



#if __name__ == '__main__':
if len(sys.argv)==0:
    app.run(debug=True)
else:
    save_file(sys.argv[1])
