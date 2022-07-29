from flask import flash
from flask_app.config.mysqlconnections import connectToMySQL
import re

NAME_REGEX = re.compile (r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
ADDRESS_REGEX = re.compile (r'^[a-zA-Z0-9]+$')
ZIP_CODE_REGEX = re.compile (r'^[0-9]+$')

class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.id_card = data["id_card"]
        self.address = data["address"]
        self.city = data["city"]
        self.state = data["state"]
        self.zip_code = data["zip_code"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        
    @staticmethod
    def validate_user(data):
        is_valid = True

        if not NAME_REGEX.match(data['first_name']):
            flash ('First name has to be all letters (example: Jacob I, Jacob II)')
            is_valid = False

        if len(data['first_name']) < 1:
            flash ('Fill in your first name')
            is_valid = False

        if len(data['last_name']) < 1:
            flash ('Fill in your last name')
            is_valid = False

        if not NAME_REGEX.match(data['last_name']):
            flash ('Last name has to be all letters')
            is_valid = False

        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False

        if len(data['password']) < 8:
            flash("Password needs to have at least 8 characters")
            is_valid = False

        if data['password'] != data['confirm_password']:
            flash("Passwords must match")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_address(data):
        is_valid = True

        if len(data['address']) < 2:
            flash ('Please input a valid address (example: 1 Disney Road)')
            is_valid = False

        if not NAME_REGEX.match(data['city']):
            flash ('Please input a valid city (example: Whistle)')
            is_valid = False

        if not NAME_REGEX.match(data['state']):
            flash ('Please input a valid state (example: YG, California)')
            is_valid = False


        return is_valid

    @classmethod
    def register_user(cls,data):
        query = "insert into users (first_name, last_name, email, password, created_at, updated_at) values(%(first_name)s, %(last_name)s, %(email)s, %(password)s, now(), now());"

        return connectToMySQL("dmv_rex").query_db(query,data)

    @classmethod
    def get_user_by_email(cls,data):
        query = 'select * from users where email = %(email)s;'

        results = connectToMySQL("dmv_rex").query_db(query,data)
        #did't find a matching user
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_user_by_id(cls,data):
        query = 'select * from users where id = %(id)s;'

        results = connectToMySQL("dmv_rex").query_db(query,data)

        return cls(results[0])

    @classmethod
    def edit_user(cls,data):
        query = 'update users set first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,id_card=%(id_card)s,address=%(address)s,city=%(city)s,state=%(state)s,zip_code=%(zip_code)s,updated_at=now() where id = %(id)s'

        return connectToMySQL ("dmv_rex").query_db(query,data)