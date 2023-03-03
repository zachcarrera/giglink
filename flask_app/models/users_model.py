import re

from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, BCRYPT

from flask_app.models import gigs_model

# constant instance of email regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    # ------ CREATE ------
    @classmethod
    def create(cls, form):

        # insert query
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s,%(email)s,%(password)s)"""

        # hash the password and wrap it with other inputs
        # in a data dictionary
        data = {
            **form,
            "password": BCRYPT.generate_password_hash(form["password"])
        }

        return connectToMySQL(DATABASE).query_db(query, data)



    # ------ READ ------
    @classmethod
    def get_one_by_id(cls, data):
        # return one user instance based off of an id

        # select query
        query = "SELECT * FROM users WHERE id = %(id)s"


        results = connectToMySQL(DATABASE).query_db(query,data)
        user = cls(results[0])
        user.gigs = gigs_model.Gig.get_all_for_user({"user_id":user.id})
        return user


    @classmethod
    def get_one_by_email(cls, data):
        # return one user based off an email
        # or return false if not found

        # select query
        query = "SELECT * FROM users WHERE email = %(email)s"

        results = connectToMySQL(DATABASE).query_db(query,data)


        if results:
            return cls(results[0])
        
        return False




    # ------ VALIDATIONS ------
    @classmethod
    def validate_login(cls, form):
        # validate a login based off inputs from request.form

        found_user = cls.get_one_by_email(form)

        # check if the email exists in db
        if not found_user:
            flash("Email/Password not valid")
            return False
        
        # check if password is correct for that email
        if not BCRYPT.check_password_hash(found_user.password, form["password"]):
            flash("Email/Password not valid")
            return False
        
        return found_user





    @staticmethod
    def validate_new(form):
        # take in a form submission and return false if any requirements are not met

        is_valid = True

        # check if first name is atleast 2 characters
        if len(form["first_name"]) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        
        # check if last name is atleast 2 characters
        if len(form["last_name"]) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False

        # check if email matches EMAIL_REGEX
        if not EMAIL_REGEX.match(form["email"]):
            flash("Email must be valid.")
            is_valid = False

        # check if email already exists in the db
        if User.get_one_by_email(form):
            flash("This email is already taken.")
            is_valid = False

        # check if password is atleast 8 characters
        if len(form["password"]) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False

        # check that password matches confirm_password
        if form["password"] != form["confirm_password"]:
            flash("Passwords must match.")
            is_valid = False

        return is_valid