from flask import Blueprint, request
from pymongo import MongoClient
from pydantic import ValidationError

from src.models.User import User

MONGOURI = "mongodb+srv://jusmint:rayiz3@nouvelle.c8ucr.mongodb.net/?retryWrites=true&w=majority&appName=nouvelle"

client = MongoClient(MONGOURI)
nouvelle = client['nouvelle']
collection_users = nouvelle['Users']

users_bp = Blueprint('users', __name__)

users_bp.route('/', methos=['POST'])
def signup():
    try:
        data = request.get_json()
        user = User(**data)
    
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