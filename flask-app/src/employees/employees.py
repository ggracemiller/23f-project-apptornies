from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db
import sys


employees = Blueprint('employee', __name__)

# Get all the products from the database
@employees.route('/employees', methods=['GET'])
def get_employees():
    print('attempting to get employees')
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT * FROM employee')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]
    print(column_headers, file=sys.stdout)

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()
    print(theData, file=sys.stdout)

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

@employees.route('/employees/<id>', methods=['GET'])
def get_employee_detail (id):

    query = 'SELECT * FROM employee WHERE id = ' + str(id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)
    

@employees.route('/employees', methods=['POST'])
def add_new_employee():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    street = the_data['street']
    city = the_data['city']
    state = the_data['state']
    zip = the_data['zip']
    hourlyRate = the_data['hourly_rate']
    lastName = the_data["last_name"]
    firstName = the_data['first_name']
    employeeType = the_data['employee_type']
    phoneNumber = the_data['phone_number']
    email = the_data['email']
    gender = the_data['gender']
    birthdate = the_data['birthdate']

    # Constructing the query
    query = 'insert into employee (street, city, state, zip, hourly_rate, last_name, first_name, employee_type, phone_number, email, gender, birthdate) values ("'
    query += street + '", "'
    query += city + '", "'
    query += state + '", '
    query += zip + '", '
    query += hourlyRate + '", '
    query += lastName + '", '
    query += firstName + '", '
    query += employeeType + '", '
    query += phoneNumber + '", '
    query += email + '", '
    query += gender + '", '
    query += birthdate + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'
