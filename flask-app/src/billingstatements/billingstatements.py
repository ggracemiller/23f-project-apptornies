from flask import Blueprint, request, jsonify, make_response
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
        cursor.execute('select company, last_name,\
        first_name, job_title, business_phone from customers')
    elif employee:
        cursor.execute('select company, last_name,\
        first_name, job_title, business_phone from customers')
    elif client:
        cursor.execute('select company, last_name,\
        first_name, job_title, business_phone from customers')
    else:
        cursor.execute('select company, last_name,\
        first_name, job_title, business_phone from customers')

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
    cursor = db.get_db().cursor()
    cursor.execute('select company, last_name,\
    first_name, job_title, business_phone from customers')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get the given billing statement
@billingstatements.route('/billingstatements/<billingstatementID>', methods=['GET'])
def get_casefile(billingstatementID):
    cursor = db.get_db().cursor()
    # TODO
    cursor.execute('select * from customers where id = {0}'.format(billingstatementID))
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
    cursor = db.get_db().cursor()
    # TODO
    cursor.execute('select * from customers where id = {0}'.format(billingstatementID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Delete the given billing statement
@billingstatements.route('/billingstatements/<billingstatementID>', methods=['DELETE'])
def put_casefiles(billingstatementID):
    cursor = db.get_db().cursor()
    # TODO
    cursor.execute('select * from customers where id = {0}'.format(billingstatementID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response