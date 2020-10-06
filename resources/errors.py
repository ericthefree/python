# ./api_app/resources/errors.py
# resource to return types of errors the user may encounter

class InternalServerError(Exception):
    pass


class SchemaValidationError(Exception):
    pass


class ServerAlreadyExistsError(Exception):
    pass


class UpdatingServerError(Exception):
    pass


class DeletingServerError(Exception):
    pass


class ServerNotExistsError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Server returned an error",
        "status": 500
    },
    "SchemaValidationError": {
         "message": "Request is missing required fields or invalid format",
         "status": 400
    },
    "ServerAlreadyExistsError": {
         "message": "A server with given name already exists",
         "status": 400
    },
    "UpdatingServerError": {
         "message": "Updating server info failed and returned an error",
         "status": 403
    },
    "DeletingServerError": {
         "message": "Deleting server failed and returned an error",
         "status": 403
    },
    "ServerNotExistsError": {
         "message": "Server with given name does not exist",
         "status": 400
    }
}
