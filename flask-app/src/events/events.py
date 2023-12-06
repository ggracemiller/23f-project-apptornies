from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


events = Blueprint('events', __name__)

def getValString(val):
    if (val is None):
        return 'Null'
    else:
      return '"' + str(val) + '"'

# Return a list of all events
# Checks for employee and client query string parameters
# Specifies the list based on them
@events.route('/events', methods=['GET'])
def get_events():
    cursor = db.get_db().cursor()
    employee = request.args.get('employee')
    client = request.args.get('client')

    if employee and client:
        cursor.execute('SELECT * FROM  events JOIN employee_event JOIN client_event WHERE employee_id = {0} AND client_id = {0}'.format(employee, client))
    elif employee:
        cursor.execute('SELECT * FROM  events JOIN employee_event WHERE employee_id = {0}'.format(employee))
    elif client:
        cursor.execute('SELECT * FROM  events JOIN client_event WHERE client_id = {0}'.format(client))
    else:
        cursor.execute('SELECT * FROM  events')

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add an event to the system
@events.route('/events', methods=['POST'])
def add_event():
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    #event = the_data['event_id']
    description = the_data['event_description']
    location = the_data['event_location']
    time = the_data['event_datetime']

    # Constructing the query
    query = 'insert into events (description, location, date_time) values (' 
    #query += getValString(event) + ', '
    query += getValString(description) + ', '
    query += getValString(location) + ', '
    query += getValString(time) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Return the given event by id
@events.route('/events/<eventID>', methods=['GET'])
def get_event(eventID):
    cursor = db.get_db().cursor()
    query = '''
        SELECT event_id, description, location, date_time
        FROM events
        WHERE event_id = {0}
        ORDER BY date_time ASC
    '''.format(eventID)

    cursor.execute(query)
    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# Update an event in the system
@events.route('/events/<eventID>', methods=['PUT'])
def update_event(eventID):
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    cursor = db.get_db().cursor()

    #extracting the variable
    event = the_data['event_id']
    description = the_data['event_description']
    location = the_data['event_location']
    time = the_data['event_datetime']

    cursor.execute('UPDATE events SET\
                   event = {0},\
                   description = {},\
                   location = {},\
                   time = {}\
                   WHERE client_id = {0}'.format(event, description, location, time, eventID))
    
    db.get_db().commit()
    
    return 'Event updated'

# Remove an event from the system
@events.route('/events', methods=['DELETE'])
def delete_event():
    eventID = request.json
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM events WHERE event_id = {0}'.format(eventID))
    #row_headers = [x[0] for x in cursor.description]
    #json_data = []
    #theData = cursor.fetchall()
    #for row in theData:
    #    json_data.append(dict(zip(row_headers, row)))
    the_response = make_response("delete success", eventID)#(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    db.get_db().commit()
    return 'Event deleted'
