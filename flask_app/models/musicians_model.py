import re

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, BCRYPT
from flask import flash

from flask_app.models import gigs_model

# constant instance of email regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Musician:
    def __init__(self, data):
        self.id = data["id"]
        self.stage_name = data["stage_name"]
        self.about = data["about"]
        self.image_url = data["image_url"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]



    def image_url_str(self):
        if self.image_url:
            return self.image_url
    
        return ""

    def about_str(self):
        if self.about:
            return self.about

        return ""



    # ----- READ -----
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM musicians ORDER BY id DESC;"

        results = connectToMySQL(DATABASE).query_db(query)

        musicians = []

        for row in results:
            musicians.append(cls(row))
        
        return musicians


    @classmethod
    def get_one_by_id(cls, data):
        """
        Query the DB for one Musician by their id
        
        :param data: musician id wrapped in a dictionary
        :return: The found musician from the db
        """


        query = "SELECT * FROM musicians WHERE id = %(id)s"

        results = connectToMySQL(DATABASE).query_db(query, data)
        musician = cls(results[0])
        musician.gigs = gigs_model.Gig.get_all_for_musician({"musician_id": musician.id})

        return musician
    



    @classmethod
    def get_one_by_email(cls, data):

        query = "SELECT * FROM musicians WHERE email = %(email)s"

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return cls(results[0])
        
        return False




    @classmethod
    def search_by_stage_name(cls, form):



        query = "SELECT * FROM musicians WHERE stage_name LIKE %(pattern)s"



        data = {
            "pattern" : f"%%{form['stage_name']}%%",
        }

        results = connectToMySQL(DATABASE).query_db(query, data)

        musicians = []

        if not results:
            return False

        for row in results:
            musicians.append(cls(row))
        return musicians




    # ----- CREATE -----
    @classmethod
    def create(cls, form):

        query = """
                INSERT INTO musicians (stage_name, email, password)
                VALUES (%(stage_name)s, %(email)s, %(password)s);"""

        data = {
            **form,
            "password" : BCRYPT.generate_password_hash(form["password"])
        }

        return connectToMySQL(DATABASE).query_db(query, data)
    

    # ----- UPDATE -----

    # update the about me section
    @classmethod
    def update(cls, data):
        query = """
                UPDATE musicians
                SET about = %(about)s, image_url = %(image_url)s
                WHERE id = %(id)s;"""
        
        return connectToMySQL(DATABASE).query_db(query, data)


    # ----- VALIDATIONS -----
    @classmethod
    def validate_login(cls, form):
        
        found_user = cls.get_one_by_email(form)

        if not found_user:
            flash("Email/Password not valid")
            return False

        if not BCRYPT.check_password_hash(found_user.password, form["password"]):
            flash("Email/Password not valid")
            return False

        return found_user
    

    @staticmethod
    def validate_new(form):
        
        is_valid = True

        if len(form["stage_name"]) < 2:
            flash("Stage name must be at least 2 characters.")
            is_valid = False
        
        if not EMAIL_REGEX.match(form["email"]):
            flash("Email must be valid.")
            is_valid = False
        
        if Musician.get_one_by_email(form):
            flash("This email is already taken.")
            is_valid = False
        
        if len(form["password"]) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False

        if form["password"] != form["confirm_password"]:
            flash("Password must match.")
            is_valid = False


        return is_valid