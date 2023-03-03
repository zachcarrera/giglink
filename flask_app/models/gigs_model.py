from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import users_model
from flask_app.models import musicians_model


class Gig:
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.musician_id = data["musician_id"]
        self.location = data["location"]
        self.gig_at = data["gig_at"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    # ----- CREATE -----
    @classmethod
    def create(cls, data):

        query = """
                INSERT INTO gigs (user_id, musician_id, location, gig_at)
                VALUES (%(user_id)s, %(musician_id)s, %(location)s, %(gig_at)s);
                """
        
        return connectToMySQL(DATABASE).query_db(query, data)



    # ----- READ -----
    @classmethod
    def get_all_for_musician(cls, data):
        """
        get a list of gig objects all for one musician with the user attached

        :param data: musician_id wrapped in dictionary
        :return: list of Gig instances or False if no results
        """

        query = """
                SELECT * FROM gigs
                LEFT JOIN users ON gigs.user_id = users.id
                WHERE gigs.musician_id = %(musician_id)s;"""
        
        results = connectToMySQL(DATABASE).query_db(query,data)

        if not results:
            return False
        
        gigs = []

        for row in results:
            gig = cls(row)

            user_data = {
                **row,
                "id": row["users.id"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            gig.user = users_model.User(user_data)

            gigs.append(gig)
        
        return gigs



    @classmethod
    def get_all_for_user(cls, data):
        """
        get a list of gig objects all for one user with the musician attached

        :param data: user_id wrapped in dictionary
        :return: list of Gig instances or False if no results
        """

        query = """
                SELECT * FROM gigs
                LEFT JOIN musicians ON gigs.musician_id = musicians.id
                WHERE gigs.user_id = %(user_id)s;"""
        
        results = connectToMySQL(DATABASE).query_db(query,data)

        if not results:
            return False
        
        gigs = []

        for row in results:
            gig = cls(row)

            musician_data = {
                **row,
                "id": row["musicians.id"],
                "created_at": row["musicians.created_at"],
                "updated_at": row["musicians.updated_at"]
            }
            gig.musician = musicians_model.Musician(musician_data)

            gigs.append(gig)
        
        return gigs
