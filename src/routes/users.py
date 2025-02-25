import logging
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pydantic import ValidationError

from src.collections.User import User

MONGOURI = "mongodb+srv://jusmint:rayiz3@nouvelle.c8ucr.mongodb.net/?retryWrites=true&w=majority&appName=nouvelle"

client = MongoClient(MONGOURI)
nouvelle = client['nouvelle'] # cluster
collection_users = nouvelle['Users'] # collection

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['POST'])
def signup():
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