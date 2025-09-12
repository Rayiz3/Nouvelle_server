import logging
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pydantic import ValidationError
from bson import ObjectId

from src.collections.User import User

MONGOURI = "mongodb+srv://jusmint:rayiz3@nouvelle.c8ucr.mongodb.net/?retryWrites=true&w=majority&appName=nouvelle&tls=true"

client = MongoClient(MONGOURI)
nouvelle = client['nouvelle'] # cluster
collection_users = nouvelle['Users'] # collection

users_bp = Blueprint('users', __name__)
user_bp = Blueprint('user', __name__)


@users_bp.route('', methods=['GET'])
def get_users():
    try:
        users = list(collection_users.find())
        
        # Convert ObjectId -> string
        for user in users:
            user['_id'] = str(user['_id'])

        return jsonify(users), 200

    except PyMongoError as e:
        logging.error(f"Database error: {str(e)}")
        return jsonify({"message": "Database error", "error": str(e)}), 500

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "Internal server error", "error": str(e)}), 500
    
@users_bp.route('', methods=['POST'])
def add_user():
    try:
        # load json data
        data = request.get_json()
        
        # pydantic validation check
        doc_user = User(**data)
        
        # redundant check
        if collection_users.find_one({"email": doc_user.email}):
            return jsonify({"message": "Email already exist"}), 400
        
        # add user to the collection
        collection_users.insert_one(doc_user.to_mongo_dict())
        return jsonify({
            "message": "User created successful",
            "user": {"email": doc_user.email, "name": doc_user.name}
        }), 201
    
    # error with pydantic
    except ValidationError as e:
        logging.error(f"Validation error: {e.errors()}")
        return jsonify({"message": "Validation error", "errors": e.errors()}), 400
    
    # error with MongoDB
    except PyMongoError as e:
        logging.error(f"Database error: {str(e)}")
        return jsonify({"message": "Database error", "error": str(e)}), 500

    # internal server error
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "Internal server error", "error": str(e)}), 500
    
@user_bp.route('', methods=['GET'])
def get_user():
    try:
        id = request.args.get("id")
        email = request.args.get("email")
        
        if id:
            # convert string -> ObjectId
            id = ObjectId(id)
            found_user = collection_users.find_one({"_id": id})
        elif email:
            found_user = collection_users.find_one({"email": email})
        else:
            return jsonify({"message": "id or email is not given"}), 400
        
        if found_user:
            found_user['_id'] = str(found_user['_id'])
            return jsonify(found_user), 200
        else:
            return jsonify({"message": "Email not found"}), 404
        
    # error with MongoDB
    except PyMongoError as e:
        logging.error(f"Database error: {str(e)}")
        return jsonify({"message": "Database error", "error": str(e)}), 500

    # internal server error
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "Internal server error", "error": str(e)}), 500
    
@user_bp.route('/config', methods=['PATCH'])
def set_config():
    try:
        id = request.args.get("id")
        if id:
            id = ObjectId(id)
        else:
            return jsonify({"message": "id is not given"}), 400
        
        config_data = request.get_json()
        if not config_data:
            return jsonify({"message": "Config data not privided"}), 400
        
        # update
        result = collection_users.update_one(
            {"_id": id},
            {"$set": {"config": config_data}}
        )
        
        if result.matched_count:
            found_user = collection_users.find_one({"_id": id})
            found_user['_id'] = str(found_user['_id'])
            return jsonify(found_user), 200
        else:
            return jsonify({"message": "id not found"}), 404
        
    # error with MongoDB
    except PyMongoError as e:
        logging.error(f"Database error: {str(e)}")
        return jsonify({"message": "Database error", "error": str(e)}), 500

    # internal server error
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "Internal server error", "error": str(e)}), 500