from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, EMAIL_REGEX, app
from flask import flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt( app )

class User:
    def __init__( self, data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.team_id = data['team_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.team = None

    @classmethod
    def create_one( cls, data ):
        query  = "INSERT INTO users ( first_name, last_name, email, password, team_id) "
        query += "VALUES( %(first_name)s, %(last_name)s, %(email)s, %(password)s, %(team_id)s);"
        result = connectToMySQL( DATABASE ).query_db( query, data )
        return result

    @classmethod
    def update_one( cls, data ):
        query  = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, team_id = %(team_id)s WHERE id = %(users_id)s;"
        result = connectToMySQL( DATABASE ).query_db( query, data )
        return result

    @classmethod
    def get_one( cls, data ):
        query  = "SELECT * "
        query += "FROM users "
        query += "WHERE email = %(email)s;"
        result = connectToMySQL( DATABASE ).query_db( query, data )
        if len( result ) == 0:
            return None
        else:
            return cls( result[0] )
    @classmethod
    def get_one_user( cls, data ):
        query  = "SELECT * FROM users WHERE id = %(users_id)s;"
        result = connectToMySQL( DATABASE ).query_db( query, data )
        current_user = cls( result[0] )
        return current_user
    @classmethod
    def get_team_with_user( cls, data ):
        query  = "SELECT * "
        query += "FROM users u JOIN teams t "
        query += "ON u.team_id = t.id "
        query += "WHERE u.id = %(id)s; "

        result = connectToMySQL( DATABASE ).query_db( query, data)
        row = result[0]
        current_user= cls(row)
        team_user = {
            **row,
        }
        current_user.team = user_model.User(team_user)
        return current_user
    @staticmethod
    def validate_user( data ):
        is_valid = True
        if len( data["first_name"] ) < 2:
            flash( "First Name must be atleast 2 characters !", "error_first_name" )
            is_valid = False
        if len( data["last_name"] ) < 2: 
            flash( "Last Name must be atleast 2 characters !", "error_last_name" ) 
            is_valid = False
        if not EMAIL_REGEX.match( data["email"] ):
            flash( "You must provide a valid email!", "error_email" )
            is_valid = False
        if len( data["password"] ) == 0:
            flash( "Please provide a password", "error_password" )
            is_valid = False
        if data["password"] != data["password_confirmation"]:
            flash( "Passwords do not match!", "error_password" )
            is_valid = False
        if User.get_one( data ) != None:
            flash( "The email is already taken!", "error_email" )
            is_valid = False
        if data["team_id"] == "0":  # Add this check
            flash("Please select your favorite team", "error_team_id")
            is_valid = False
        return is_valid
    @staticmethod
    def validate_user_again( data ):
        is_valid = True
        if len( data["first_name"] ) < 2:
            flash( "First Name must be atleast 2 characters !", "error_first_name" )
            is_valid = False
        if len( data["last_name"] ) < 2: 
            flash( "Last Name must be atleast 2 characters !", "error_last_name" ) 
            is_valid = False
        if not EMAIL_REGEX.match( data["email"] ):
            flash( "You must provide a valid email!", "error_email" )
            is_valid = False
        if data["team_id"] == "0":  # Add this check
            flash("Please select your favorite team", "error_team_id")
            is_valid = False
        return is_valid
    @staticmethod
    def validate_password( password, encrypted_password ):
        if not bcrypt.check_password_hash( encrypted_password, password ):
            flash( "Wrong credentials", "error_login_password" )
            return False
        return True

    @staticmethod
    def encrypt_string( text ):
        encrypted_string = bcrypt.generate_password_hash( text )
        return encrypted_string