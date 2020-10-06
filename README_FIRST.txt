README_FIRST.txt

The code and images (in .tar format) are inside the zip file.  The START_HERE.md file inside the zipped file contains details about the source, api and docker images.

NOTE: I work on Mac and would have tried to test the images on a Windows machine with docker, but didn't have quite enough time.

I have unzipped this file on another Mac that had docker, loaded the images and ran the docker-compose command and they ran successful and web-page opened up as expected.  I did have to update the version of python on that machine, but simple to do.  The steps I followed are in the START_HERE.md file inside the project folder.

There is a lot more that could have been done with this, obviously.  If it were an ongoing and legitimate project I would have expected to setup a actual URL with a domain name.  Authentication would have been something important as well.  There is some basic authentication setup for the database, but as you'll see in the code at this point I have the database ROOT user and password in the URL inside the resources/db.py file for connecting to the URL.

There is some basic exception handling and error information returned in the API calls for things like when a server doesn't exist, or POSTing and the server_name is already in the database.  Of course there could have been a lot more that could have been done, but I believe I covered the basic worst case scenario's so the end user isn't seeing a bunch of weird errors aside from if the web-server or database are not running.

The REST api responses could use more detail in the responses.  I have worked with a web project in Python at my current company, but haven't set something like this up from scratch.  I also haven't run docker containers in a set of two where one needs to connect to the other, so that took some research and learning, but a great exercise.  I also haven't worked much with MongoDB, but I was able to get some of the basic understanding enough to store data there.

I'd love feedback on what could be improved or coded better as I am always interested in improving my knowledge.

Hopefully the START_HERE.md readme file has all the information needed to understand the API's.

I have 