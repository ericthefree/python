# flask_api_mongodb app with docker

# Introduction

    This API allows a user to store a list of servers in a Mongo DB server.  You can do a health check, view servers, 
    find a server by name, add a new server and DELETE server by server_name. Update API has not yet been implemented.

# Requirements to run this app locally

This app requires python to run.  The app was developer with python 3.8.  If you work from a Mac,
I personally recommend you install python locally following the steps from the "What we should do" 
section of the following URL: 
    
    https://opensource.com/article/19/5/python-3-default-mac
    
    Basic setup steps:
    
    Install Homebrew:
        
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)" 
       
    Install pyenv:
    
        brew install pyenv
        
    Check for the latest version or versions of python available:
    
        pyenv install --list
        
    Install python:
    
        pyenv install 3.8.5
        
    Set version globally:
    
        pyenv global 3.8.5
        
    Check version:
    
        pyenv version
    
    Update the configuration file or files .zshrc and/or .bash_profile:
    
        echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshrc
        echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
        
    NOTE: Remove any aliases in these file if they exist.
    
    Reset the current shell or start a new terminal instance and check where python lives:
    
        exec $O
        which python
        python -V
        pip -V # Checking the version of pip
        
    PYTHON should now be installed and setup
    
You will need to have docker installed in order to load and run the images and containers and can 
find the download from here:
    
    https://www.docker.com/products/docker-desktop

You can connect to the mongodb via gui by installing Mongo Compass from here:
    
    https://docs.mongodb.com/compass/master/install/
    
I also recommend Postman for running api calls, but not necessary.   You can install Postman from here:

    https://www.postman.com/downloads/
    
    
# Overview
Currently if you hit the base URL http://localhost:5001 or http://localhost:5001/health_check, you will see a return 
code for both the web host and the database server.

The quick overview:

    The API base calls are run from the following URL:
    <http://localhost:5001/server_list/api/v1/servers>.  

    For searching for information about a particular database you will need to know the server_name.  If you do not, you can always hit the url <http://localhost:5001/server_list> or <http://localhost:5001/server_list/api/v1/servers> without anything else and it will return the full list of servers on the database.

    Simply adding the server_name at the end of the API url will run your CRUD action agains the database. 

    If you need to search for a particular server or delete a server you will need to enter the <server_name>.

    To create a new server you need to enter the following format and each field is required for creating a new server:
    
        {
            "server_name": "sea_win_webhost_westreg_001",
            "server_os": "windows",
            "server_flavor": "windows_server", 
            "server_version": "2019",
            "server_type": "web_host"
        }
    
NOTE: There is a more detailed overview of the api after this section.

# Docker Image Detail and API information

Load the images from the following files:
    
    The .tar files are located in the 'docker_container_images' directory:
    
    docker load < mongodb_apidb_save.tar
    docker load < api_app_save.tar

Build the docker image if doesn't load:

    docker build --tag api_app:1.0 .

Bring the docker container's online in the application:

    docker compose up -d
    Containers will come up as application: api_project
    
Populate database with servers:

    You can connect the the api_app container and run:
        python tests/load_database.py
    Of course you can run the docker exec command against the container.  I did not
    get far enough to list the command here.
    
Docker images info

    Currently built against following images:
        MongoDB - mongo:latest - from docker hub
            Image Name: mongodb_apidb
            Container Name: api_db
            Authentication enabled and users added
            URL to connect via MongoDB Compass
                mongodb://mongodbuser:password_unsecure@localhost:27017
        Python/Flask - python:3.8.6-alpine3.12
            Image Name: api_app
            Container Name: api_app
            Application runs against port 5001
                BASE URL: http://localhost:5001
                
# Running the application locally

    To run the application locally I recommend the following commands assuming you've installed python already:
    
    NOTE: If you are wanting to run locally, you will need to UNCOMMENT and COMMENT a line in the:
        resources/db.py file.

    BELOW is the code in the file:        
    *******************
    
        # LOCAL RUN UNCOMMENT THE LINE BELOW FOR CONNECTING TO THE DATABASE SERVER
        mongo_client = MongoClient('mongodb://mongodbuser:password_unsecure@localhost:27017')

        # UNCOMMENT THE NEXT LINE IF YOU ARE REBUILDING THE IMAGE
        # mongo_client = MongoClient('mongodb://mongodbuser:password_unsecure@mongo_db:27017')

    *******************   

    Once set run the following on a system that isn't setup with Python:
    
        pip install --user pipenv
        pip install -r requirements.txt
        pipenv run python app_start.py
        
    NOTE: If the database is not running, you won't be able to bring any data up in the browser.
    
    

# The detailed overview:

Web/API URL's:

    API BASE URL:

    http://localhost:5001/server_list/api/v1/servers

HEALTH CHECK URL:

    http://localhost:5001
    http://localhost:5001/health_check

Health Check API:

    curl --header "Content-Type: application/json" --request GET http://localhost:5001
     --or--
    curl --header "Content-Type: application/json" --request GET http://localhost:5001/health_check
        
    HEALTH CHECK API RESPONSE:

            "API Web Host Status": "Server is running" ~ "status": 200
            "MongoDB Status": "Server is running" ~ '(ok: 1.0)'

API GET/DELETE by server_name:

    http://localhost:5001/server_list/api/v1/servers/<server_name> # No brackets <>
    
GET server that exists in the database by name:

    curl --header "Content-Type: application/json" --request GET http://localhost:5001/server_list/api/v1/servers/sea_win_webhost_westreg_001
        
    SERVER EXISTS API RESPONSE:
    
    {
        "results": {
            "_id": "5f7c005a135a775e950ec637",
            "created_date": "Tuesday, October 06, 2020 ~ 05:27 AM",
            "server_flavor": "windows_server",
            "server_name": "sea_win_webhost_westreg_001",
            "server_os": "windows",
            "server_type": "web_host",
            "server_version": "2019"
        },
        "server_exists": true
    }

    SERVER NOT EXISTS:
    curl --header "Content-Type: application/json" --request GET http://localhost:5001/server_list/api/v1/servers/sea_win_webhost_westreg_006
    
    API RESPONSE:
    
    {
      "results": null,
      "server_exists": false
    }
        
SERVER LIST URL:

    http://localhost:5001/server_list
        -- OR --
    http://localhost:5001/server_list/api/v1/servers

GET current list of servers in the database 'api_db':

    curl --header "Content-Type: application/json" --request GET http://localhost:5001/server_list
     --or--
    curl --header "Content-Type: application/json" --request GET http://localhost:5001/server_list/api/v1/servers

    API RESPONSE:
    
    {
        "results": [
        {
            "_id": "5f7c005a135a775e950ec637",
            "created_date": "Tuesday, October 06, 2020 ~ 05:27 AM",
            "server_flavor": "windows_server",
            "server_name": "sea_win_webhost_westreg_001",
            "server_os": "windows",
            "server_type": "web_host",
            "server_version": "2019"
        },
        {
            "_id": "5f7c005a135a775e950ec638",
            "created_date": "Tuesday, October 06, 2020 ~ 05:27 AM",
            "server_flavor": "windows_server",
            "server_name": "sea_win_webhost_westreg_002",
            "server_os": "windows",
            "server_type": "web_host",
            "server_version": "2019"
        },
        {
            "_id": "5f7c005b135a775e950ec639",
            "created_date": "Tuesday, October 06, 2020 ~ 05:27 AM",
            "server_flavor": "centos",
            "server_name": "phx_linux_proxy_westreg_001",
            "server_os": "linux",
            "server_type": "proxy_server",
            "server_version": "8(2004)"
        }
      ]
    }
        
POST a new server:

    * Post a server with a new name and get a return
    * Post a server with a server that already exists with the same name and get an error message
    
        curl --header "Content-Type: application/json" --request POST --data '{"server_flavor": "windows_server", "server_name": "sea_win_webhost_westreg_004", "server_os": "windows", "server_type": "web_host", "server_version": "2019"}' http://localhost:5001/server_list/api/v1/servers
        
    SERVER ADDED API RESPONSE:

        {
            "server_add_success": {
            "_id": "5f7c03e9135a775e950ec63f",
            "response": true,
            "server_name": "sea_win_webhost_westreg_004"
            }
        }
        
    SERVER EXISTS API RESPONSE:

        {
            "server_add_failure": "A server with the server_name sea_win_webhost_westreg_004 already exists in the database.  Please update server_name to a unique name, status_code=304, Not Modified"
        }
    
DELETE a server by server_name:

    curl --header "Content-Type: application/json" --request DELETE http://localhost:5001/server_list/api/v1/servers/phx_linux_proxy_westreg_001
    
    DELETE SERVER API RESPONSE SERVER EXISTS:
    
        {
            "server_deleted": {
            "response": true, 
            "server_name": "phx_linux_proxy_westreg_001"
            }
        }
        
    DELETE API RESPONSE WHEN SERVER DOES NOT EXIST:
    
        {
          "server_not_exist_failure": "A server with the server_name phx_linux_proxy_westreg_001 does not exist in the database.  Please check servername you are trying to delete."
        }

# Authentication
Authentication has not yet been implemented, so you can run API tests against this API set without requiring any sort of authentication.

# Error Codes
Some error handling has been implemented such as the following:

    * If no servers exist, a message that no server data will be returned.
    * If you try to add a server with the same server_name of a server already in the database, 
      you will get a message that one already exists.
    * If you try to search for an existing server by server_name and it doesn't exists, an error
      message will be displayed telling you that it doesn't exist.
      * Currently, the only way to search for a server is by server_name.
    * There has been some other exception error handling implemented, but not to the extent that it could be.
    

# Rate limit
There should not be a limit to the number of API calls you can send.  It should only be limited by your machine and the limites of the container it runs in.

