from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


billingstatements = Blueprint('billingstatements', __name__)

# Get a list of all billing statements
# Checks for employee and client query string parameters
# Specifies the list based on them
@billingstatements.route('/billingstatements', methods=['GET'])
def get_casefiles():
    cursor = db.get_db().cursor()
    employee = request.args.get('employee')
    client = request.args.get('client')

    if employee and client:
        cursor.execute('select employee_id, case_id, communication_type, number_of_hours,\
        from billing_statement join client_case\
        where employee_id = {} and client_id = {}').format(employee, client)
    elif employee:
        cursor.execute('select employee_id, case_id, communication_type, number_of_hours,\
        from billing_statement join client_case\
        where employee_id = {}').format(employee)
    elif client:
        cursor.execute('select employee_id, case_id, communication_type, number_of_hours,\
        from billing_statement join client_case\
        where client_id = {}').format(client)
    else:
        cursor.execute('select employee_id, case_id, communication_type, number_of_hours,\
        from billing_statement')

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
    query = 'insert into products (employee_id, case_id, communication_type, number_of_hours) values ("'
    query += str(employee_id) + '", "'
    query += str(case_id) + '", "'
    query += communication_type + '", '
    query += str(number_of_hours) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Get the given billing statement
@billingstatements.route('/billingstatements/<billingstatementID>', methods=['GET'])
def get_casefile(billingstatementID):
    cursor = db.get_db().cursor()
    cursor.execute('select employee_id, case_id, communication_type, number_of_hours,\
        from billing_statement join client_case\
        where billing_statement_id = {}').format(billingstatementID)
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
def get_casefile(billingstatementID):
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    cursor = db.get_db().cursor()

    #extracting the variable
    employee_id = the_data['employee_id']
    case_id = the_data['case_id']
    communication_type = the_data['communication_type']
    number_of_hours = the_data['number_of_hours']

    cursor.execute('update billing_statement\
        set {}, {}, {}, {}\
        where client_id = {}').format(employee_id, case_id, communication_type, number_of_hours, casefileID)

    db.get_db().commit()
    
    return 'Success!'

# Delete the given billing statement
@billingstatements.route('/billingstatements/<billingstatementID>', methods=['DELETE'])
def put_casefiles(billingstatementID):
    cursor = db.get_db().cursor()
    cursor.execute('delete from billing_statement where billing_statement_id = {0}'.format(billingstatementID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response