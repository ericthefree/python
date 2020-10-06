# ./api_app/app_start.py
# This is the starting point for the application
from resources.routes import app_api
from flask import Flask

api_app = Flask(__name__)
api_app.register_blueprint(app_api)


# application starts from here
if __name__ == '__main__':
    api_app.run(debug=True, port=5001, host='0.0.0.0')
