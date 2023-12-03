from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


casefiles = Blueprint('casefiles', __name__)

# Get a list of all case files
# Checks for employee and client query string parameters
# Specifies the list based on them
@casefiles.route('/casefiles', methods=['GET'])
def get_casefiles():
    cursor = db.get_db().cursor()
    employee = request.args.get('employee')
    client = request.args.get('client')

    if employee and client:
        cursor.execute('select file, start_date, close_date,\
        from case_file join client_case\
        where employee_id = {} and client_id = {}').format(employee, client)
    elif employee:
        cursor.execute('select file, start_date, close_date,\
        from case_file join client_case\
        where employee_id = {}').format(employee)
    elif client:
        cursor.execute('select file, start_date, close_date,\
        from case_file join client_case\
        where client_id = {}').format(client)
    else:
        cursor.execute('select file, start_date, close_date,\
        from case_file join client_case')

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

    query1 = 'insert into client_case (start_date, close_date, client_id) values ("'
    query1 += str(start_date) + '", "' # how to get case_id when it was just created?
    query1 += str(close_date) + '", "'
    query1 += str(client_id) + ')'
    current_app.logger.info(query1)

    # Constructing the query
    query2 = 'insert into case_file (case_id, employee_id, file) values ("'
    query2 += case_id + '", "' # how to get case_id when it was just created?
    query2 += file + '", "'
    query2 += str(employee_id) + ')'
    current_app.logger.info(query2)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query1)
    cursor.execute(query2)
    db.get_db().commit()
    
    return 'Success!'

# Get the given case file
@casefiles.route('/casefiles/<casefileID>', methods=['GET'])
def get_casefile(casefileID):
    cursor = db.get_db().cursor()
    cursor.execute('select file, start_date, close_date,\
        from case_file join client_case\
        where case_file_id = {}').format(casefileID)
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
def get_casefile(casefileID):
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

    cursor.execute('update case_file\
        set {}, {},\
        where client_id = {}').format(employee_id, file, casefileID)
    
    cursor.execute('update client_case\
        set {}, {}, {},\
        where client_id = {}').format(start_date, close_date, client_id, casefileID)
    
    db.get_db().commit()
    
    return 'Success!'

# Delete the given case file
@casefiles.route('/casefiles/<casefileID>', methods=['DELETE'])
def put_casefiles(casefileID):
    cursor = db.get_db().cursor()
    cursor.execute('delete from case_file where case_file_id = {0}'.format(casefileID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response