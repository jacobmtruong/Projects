from flask import flash
from flask_app.config.mysqlconnections import connectToMySQL
from flask_app.models.user import User
import re
PLATE_REGEX = re.compile(r'^[A-Z0-9]+$')
VIN_REGEX = re.compile(r'^[A-Z0-9]+$')
NAME_REGEX = re.compile (r'^[a-zA-Z]+$')
ID_CARD_REGEX = re.compile(r'^[A-Z]{1}\d{7}$')



class Vehicle:
    def __init__(self, data):
        self.id = data["id"]
        self.make = data["make"]
        self.year = data["year"]
        self.model = data["model"]
        self.owner_first_name = data["owner_first_name"]
        self.owner_last_name = data["owner_last_name"]
        self.owner_id_card = data["owner_id_card"]
        self.address = data["address"]
        self.city = data["city"]
        self.state = data["state"]
        self.zip_code = data["zip_code"]
        self.VIN = data["VIN"]
        self.plate = data["plate"]
        self.registration_fee = data["registration_fee"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.poster = None


    @staticmethod
    def validate_vehicle(data):
        is_valid = True

        if not PLATE_REGEX.match(data['plate']):
            flash ('Invalid plate input')
            is_valid = False
        
        if not VIN_REGEX.match(data['VIN']):
            flash ('Invalid VIN input')
            is_valid = False
    

        return is_valid

    @staticmethod
    def validate_new_owner(data):
        is_valid = True

        if not NAME_REGEX.match(data['owner_first_name']) and len(data["owner_first_name"]) < 1:
            flash ('Invalid first name input')
            is_valid = False

        if not NAME_REGEX.match(data['owner_last_name']) and len(data["owner_last_name"]) < 1:
            flash ('Invalid last name input')
            is_valid = False
        
        if not ID_CARD_REGEX.match(data['owner_id_card']) and len(data["owner_id_card"]) < 1:
            flash ('Invalid ID/DL input')
            is_valid = False

        # if len(data["owner_first_name"]) < 1:
        #     flash ('Please enter your legal first name')
        #     is_valid = False

        # if len(data["owner_last_name"]) < 1:
        #     flash ('Please enter your legal last name')
        #     is_valid = False

        # if len(data["owner_id_card"]) < 1:
        #     flash ('Please enter your ID/DL number')
        #     is_valid = False
            
        if len(data["address"]) < 5:
            flash ('Please enter your current address')
            is_valid = False

        if len(data["city"]) < 2:
            flash ('Please enter the city name')
            is_valid = False

        if len(data["state"]) < 2:
            flash ('Please enter the state that you live in')
            is_valid = False

        if len(data["zip_code"]) < 5:
            flash ('Please enter valid zip code')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_new_address(data):
        is_valid = True

        if len(data['address']) < 2:
            flash ('Please fill out a valid address.')
            is_valid = False

        if len(data['city']) < 2:
            flash ('Please fill out a valid city.')
            is_valid = False

        if len(data['state']) < 2:
            flash ('Please fill out your state.')
            is_valid = False

        if len(data['zip_code']) < 4:
            flash ('Please fill out a valid zip code.')
            is_valid = False

        return is_valid


    @classmethod
    def get_vehicle_by_plate(cls,data):
        # query = 'select * from vehicles where plate = %(plate)s;'
        query = 'select * from vehicles where plate = %(plate)s and right(vin,5) = %(right(vin,5))s'

        return connectToMySQL ('dmv_rex').query_db(query,data)



    @classmethod
    def get_vehicle_by_id(cls,data):
        query = 'select * from vehicles where id = %(id)s;'

        results = connectToMySQL("dmv_rex").query_db(query,data)

        return cls(results[0])

    @classmethod
    def update_vehicle_with_new_owner(cls,data):
        query = 'create event transferToNewOwner on schedule at CURRENT_TIMESTAMP + INTERVAL 30 SECOND DO update vehicles set owner_first_name = %(owner_first_name)s, owner_last_name = %(owner_last_name)s, owner_id_card = %(owner_id_card)s, address = %(address)s, city = %(city)s, state = %(state)s, zip_code = %(zip_code)s, updated_at = now() where id = %(id)s'

        return connectToMySQL("dmv_rex").query_db(query,data)

    
    @classmethod
    def update_address_on_vehicle(cls,data):

        query = 'update vehicles set address = %(address)s, state = %(state)s, city = %(city)s, zip_code = %(zip_code)s, updated_at = now() where id = %(id)s '

        return connectToMySQL("dmv_rex").query_db(query,data)

    # @classmethod
    # def get_all_with_users(cls):
    #     query = "select * from vehicles join users on vehicles.users_id = users.id"

    #     results = connectToMySQL("dmv_rex").query_db(query)
    #     print(results)

    #     all_vehicles = []

    #     for vehicle in results:
    #         one_vehicle = cls(vehicle)
    #         user_data = {
    #             "id": vehicle["users.id"],
    #             "first_name": vehicle["first_name"],
    #             "last_name": vehicle["last_name"],
    #             "email": vehicle["email"],
    #             "password": vehicle["password"],
    #             "created_at": vehicle["users.created_at"],
    #             "updated_at": vehicle["users.updated_at"],
    #             "users_id": vehicle["users_id"]
    #         }
    #         one_vehicle.poster = User(user_data)
    #         all_vehicles.append(one_vehicle)

    #     return all_vehicles