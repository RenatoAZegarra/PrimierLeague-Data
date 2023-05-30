from flask_app import app
from flask_app.controllers import users_controller, api_controller, teams_controller

if __name__ == "__main__":
    app.run( debug = True)