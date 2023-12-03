from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


casefiles = Blueprint('casefiles', __name__)

def getValString(val):
    if (val is None):
        return 'Null'
    else:
      return '"' + str(val) + '"'

# Get a list of all case files
# Checks for employee and client query string parameters
# Specifies the list based on them
@casefiles.route('/casefiles', methods=['GET'])
def get_casefiles():
    cursor = db.get_db().cursor()
    employee = request.args.get('employee')
    client = request.args.get('client')

    if employee and client:
        cursor.execute('SELECT * FROM  case_file JOIN client_case WHERE employee_id = {0} AND client_id = {0}'.format(employee, client))
    elif employee:
        cursor.execute('SELECT * FROM case_file JOIN client_case WHERE employee_id = {0}'.format(employee))
    elif client:
        cursor.execute('SELECT * FROM case_file JOIN client_case WHERE client_id = {0}'.format(client))
    else:
        cursor.execute('SELECT * FROM case_file JOIN client_case ON case_file.case_id = client_case.case_id')

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add a case file to the system
@casefiles.route('/casefiles', methods=['POST'])
def post_casefiles():
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    file = the_data['file']
    start_date = the_data['start_date']
    close_date = the_data['close_date']
    employee_id = the_data['employee_id']
    client_id = the_data['client_id']

    query1 = 'INSERT INTO client_case (start_date, close_date, client_id) VALUES ("'
    query1 += getValString(start_date) + '", "'
    query1 += getValString(close_date) + '", "'
    query1 += getValString(client_id) + ')'
    current_app.logger.info(query1)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query1)

    # Constructing the query
    query2 = 'INSERT INTO case_file (case_id, employee_id, file) VALUES ("'
    query2 += cursor.lastrowid + '", "'
    query2 += getValString(file) + '", "'
    query2 += getValString(employee_id) + ')'
    current_app.logger.info(query2)

    cursor.execute(query2)
    db.get_db().commit()
    
    return 'Success!'

# Get the given case file
@casefiles.route('/casefiles/<casefileID>', methods=['GET'])
def get_casefile(casefileID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM case_file join client_case WHERE case_file_id = {0}'.format(casefileID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update the given case file
@casefiles.route('/casefiles/<casefileID>', methods=['PUT'])
def put_casefile(casefileID):
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    cursor = db.get_db().cursor()

    #extracting the variable
    file = the_data['file']
    start_date = the_data['start_date']
    close_date = the_data['close_date']
    employee_id = the_data['employee_id']
    client_id = the_data['client_id']
    
    cursor.execute('UPDATE case_file SET\
                   employee_id = {0},\
                   file = {}\
                   WHERE client_id = {0}'.format(employee_id, file, casefileID))
    
    cursor.execute('UPDATE client_case SET\
                   start_date = {},\
                   close_date = {},\
                   client_id = {0}\
                   WHERE client_id = {0}'.format(start_date, close_date, client_id, casefileID))
    
    db.get_db().commit()
    
    return 'Event updated'

# Delete the given case file
@casefiles.route('/casefiles/<casefileID>', methods=['DELETE'])
def delete_casefiles(casefileID):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM case_file WHERE case_file_id = {0}'.format(casefileID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return 'Event deleted'