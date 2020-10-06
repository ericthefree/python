# ./api_app/resources/routes.py
# Defines the routes for the api calls
from flask import Response, request, Blueprint
from pymongo.errors import InvalidDocument
from resources.errors import SchemaValidationError, InternalServerError, ServerNotExistsError
from bson import ObjectId
from datetime import datetime
import resources.db as db

app_api = Blueprint('app_api', __name__)


# Return the health of the web host and the mongodb server here
@app_api.route('/')
@app_api.route('/health_check')
def health_check():
    # Check the mongo db status should return {'ok': 1.0} if it's up and running
    mongodb_server_status = "\"MongoDB Status\": \"Server is running\" ~ \'(ok: 1.0)\'" if str(db.mongo_db.command(
        'ping')) == '''{'ok': 1.0}''' else "MongoDB Status\": \"ERROR: Unable to connect to database server\""

    # Check the web_host response
    web_response = "\"API Web Host Status\": \"Server is running\" ~ \"status\": 200\n" \
        if Response.default_status == 200 else"\"API Web Host Status\": \"Not responding\" ~ " \
                                              "\"status\": {}\n".format(Response.default_status)

    return Response(response=(web_response + mongodb_server_status), status=200, mimetype='application/json')


# Get the list of servers
@app_api.route('/server_list', methods=['GET'])
@app_api.route('/server_list/api/v1/servers', methods=['GET'])
def get_all_servers():
    # Get the server list from the database and collection
    request_output = list(db.mongo_col.find({}))

    # Check if anything was returned first and set the output if nothing found
    try:
        # If no servers were returned, the length will be 0 here
        if len(request_output) == 0:
            request_output = "No Server Data Exists"
        else:
            # Loop through the list and set the Object ID to be a string so we can display in JSON format
            for item in request_output:
                if isinstance(item['_id'], ObjectId):
                    item['_id'] = str(item['_id'])
        server_response = {'results': request_output}
    except InvalidDocument:
        raise SchemaValidationError
    except Exception:
        raise InternalServerError

    return server_response


# Find a server by name and return the table data for that server
@app_api.route('/server_list/api/v1/servers/<server_name>', methods=['GET'])
def get_server_by_name(server_name):
    find_server_response = None
    server_exists = False
    # Get the server list from the database and collection
    request_output = list(db.mongo_col.find({}))
    try:
        if len(request_output) == 0:
            find_server_response = {"No servers returned from the request with the name {}".format(server_name)}
        else:
            for server in request_output:
                if server['server_name'] == server_name:
                    if isinstance(server['_id'], ObjectId):
                        server['_id'] = str(server['_id'])
                    find_server_response = server
                    server_exists = True
    except ServerNotExistsError:
        raise ServerNotExistsError
    except Exception:
        raise InternalServerError

    server_response = {'results': find_server_response, 'server_exists': server_exists}

    return server_response


# Add a new server to the list
@app_api.route('/server_list/api/v1/servers', methods=['POST'])
def add_new_server():
    server_data = request.get_json()
    # Getting the current date/time so we can set the date and time the server was added
    current_time = datetime.now()
    set_date = current_time.strftime("%A, %B %d, %Y ~ %I:%M %p")
    # update the server data with the created date
    server_data['created_date'] = set_date
    server_name = server_data['server_name']

    # Check if the server already exists in the database before trying to add
    if not get_server_by_name(server_name)['server_exists']:
        try:
            # add the server to the database
            response = db.mongo_col.insert_one(server_data)
            # get the id that was created by mongo db and return it here
            server_id = str(response.inserted_id)
            return_response = {'server_add_success': {'server_name': f"{server_name}", '_id': f"{server_id}",
                                                      'response': response.acknowledged}}
        except Exception:
            raise InternalServerError
    else:
        return {'server_add_failure': f"A server with the server_name {server_name} already exists "
                                      f"in the database.  Please update server_name to a unique name, "
                                      f"status_code=304, Not Modified"}

    return return_response


# NOTE: Didn't have enough time to finish this portion of the api
# delete an existing server from the server_list
@app_api.route('/server_list/api/v1/servers/<server_name>', methods=['DELETE'])
def delete_server(server_name):

    # Get server info about server we are trying to delete
    server_info = get_server_by_name(server_name)
    # Convert server_info to a list
    list(server_info)
    # Check if the server already exists in the database before trying to add
    if server_info['server_exists']:
        try:
            # Delete the server by servername and get the return response
            response = db.mongo_col.delete_one({"server_name": server_name})
            # get the id that was created by mongo db and return it here
            return_response = {'server_deleted': {'server_name': server_name, 'response': response.acknowledged}}
        except Exception:
            raise InternalServerError
    else:
        return_response = {'server_not_exist_failure': f"A server with the server_name {server_name} does not "
                                                       f"exist in the database.  Please check servername you are "
                                                       f"trying to delete."}

    return return_response
