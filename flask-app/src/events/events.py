from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

events = Blueprint('events', __name__)

# Return a list of all events
@events.route('/events', methods=['GET'])
def get_events():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT event_id, description, location, date_time FROM events')

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

# Add an event to the system
@events.route('/events', methods=['POST'])
def add_event():
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    event = the_data['event_id']
    description = the_data['event_description']
    location = the_data['event_location']
    time = the_data['event_datetime']

    # Constructing the query
    query = 'insert into events (event_id, description, location, date_time) values ("'
    query += event + '", "'
    query += description + '", "'
    query += location + '", "'
    query += time + '", "'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Return the given event by id
@events.route('/events/<event_id>', methods=['GET'])
def get_event(event_id):
    cursor = db.get_db().cursor()
    query = '''
        SELECT event_id, description, location, date_time
        FROM events
        WHERE event_id = given_event_id
        ORDER BY date_time
    '''
    ### not sure what to do with reutrn the given event by id here ###

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
@events.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    # ...
    return 'Event updated'

# Remove an event from the system
@events.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    # ...
    return 'Event deleted'

# Return a list of events associated with the given employee
@events.route('/events', methods=['GET'])
def get_events_by_employee():
    employee_id = request.args.get('employee')
    # ... 
    return 

# Return a list of events associated with the given client
@events.route('/events', methods=['GET'])
def get_events_by_client():
    client_id = request.args.get('client')
    # ...
    return 

