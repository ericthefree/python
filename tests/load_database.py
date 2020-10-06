# ./api_app/tests/load_database.py
# This will load database with some data
import json
import requests

data_file = 'tests/test_data.json'
url = 'http://localhost:5001/server_list/api/v1/servers'


# Load the database with server list
def load_database_data(json_file):
    with open(json_file) as file:
        json_data = json.load(file)

    for server in json_data:
        response = requests.post(url, json=server)

        print(response)


# run the code to load the data to the database
load_database_data(data_file)
