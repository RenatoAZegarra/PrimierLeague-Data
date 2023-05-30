from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, app

class Team:
    def __init__( self, data ):
        self.id = data["id"]
        self.name = data["name"]
        self.stadium = data["stadium"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM teams WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])