from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


billingstatements = Blueprint('billingstatements', __name__)

def getValString(val):
    if (val is None):
        return 'Null'
    else:
      return '"' + str(val) + '"'

# Get a list of all billing statements
# Checks for employee and client query string parameters
# Specifies the list based on them
@billingstatements.route('/billingstatements', methods=['GET'])
def get_casefiles():
    cursor = db.get_db().cursor()
    employee = request.args.get('employee')
    client = request.args.get('client')

    if employee and client:
        cursor.execute('SELECT * FROM billing_statement WHERE employee_id = {0} and client_id = {0}').format(employee, client)
    elif employee:
        cursor.execute('SELECT * FROM billing_statement WHERE employee_id = {0}').format(employee)
    elif client:
        cursor.execute('SELECT * FROM billing_statement WHERE client_id = {0}').format(client)
    else:
        cursor.execute('SELECT * FROM billing_statement')

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add a billing statements to the system
@billingstatements.route('/billingstatements', methods=['POST'])
def post_casefiles():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    employee_id = the_data['employee_id']
    case_id = the_data['case_id']
    communication_type = the_data['communication_type']
    number_of_hours = the_data['number_of_hours']

    # Constructing the query
    query = 'INSERT INTO products (employee_id, case_id, communication_type, number_of_hours) VALUES ("'
    query += getValString(employee_id) + '", "'
    query += getValString(case_id) + '", "'
    query += getValString(communication_type) + '", '
    query += getValString(number_of_hours) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Get the given billing statement
@billingstatements.route('/billingstatements/<billingstatementID>', methods=['GET'])
def get_specific_casefile(billingstatementID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM billing_statement WHERE billing_statement_id = {0}').format(billingstatementID)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update the given billing statement
@billingstatements.route('/billingstatements/<billingstatementID>', methods=['PUT'])
def put_casefile(billingstatementID):
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    cursor = db.get_db().cursor()

    #extracting the variable
    employee_id = the_data['employee_id']
    case_id = the_data['case_id']
    communication_type = the_data['communication_type']
    number_of_hours = the_data['number_of_hours']

    cursor.execute('UPDATE billing_statement\
        SET {0}, {0}, {}, {0}\
        WHERE client_id = {0}').format(employee_id, case_id, communication_type, number_of_hours, billingstatementID)

    db.get_db().commit()
    
    return 'Success!'

# Delete the given billing statement
@billingstatements.route('/billingstatements/<billingstatementID>', methods=['DELETE'])
def delete_casefiles(billingstatementID):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM billing_statement WHERE billing_statement_id = {0}'.format(billingstatementID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response