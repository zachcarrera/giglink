from flask_app import app

# import controllers here
from flask_app.controllers import users_controller, musicians_controller, gigs_controller

if __name__ == "__main__":
    app.run(debug=True)
