import logging
import requests
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pydantic import ValidationError
from bson import ObjectId

from src.collections.Mesh import Mesh

MONGOURI = "mongodb+srv://jusmint:rayiz3@nouvelle.c8ucr.mongodb.net/?retryWrites=true&w=majority&appName=nouvelle"
MODAL_ENDPOINT = "https://jusmint3--nouvelle-shape-generate-mesh-api.modal.run"

client = MongoClient(MONGOURI)
nouvelle = client['nouvelle'] # cluster
collection_meshes = nouvelle['Meshes'] # collection (made automatically)

meshes_bp = Blueprint('meshes', __name__)


@meshes_bp.route('', methods=['POST'])
def add_mesh():
    try:
        user_id = request.args.get("id")
        if user_id:
            user_id = ObjectId(user_id)
        else:
            return jsonify({"message": "id is not given"}), 400
        
        prompt_data = request.get_json()
        if not prompt_data:
            return jsonify({"message": "prompt not privided"}), 400
        
        # pydantic validation check
        data = {
            'user_id': str(user_id),
            'prompt': prompt_data["prompt"],
            'iconMeshUrl': ""
        }
        
        doc_mesh = Mesh(**data)
        
        # update
        result = collection_meshes.insert_one(doc_mesh.to_mongo_dict())
        mesh_id = result.inserted_id
        
        response = requests.post(
            MODAL_ENDPOINT,
            json={
                "prompt": doc_mesh.prompt,
                "user_id": doc_mesh.user_id,
                "mesh_id": str(mesh_id),
            },
            timeout=600,
        )
        
        if response.status_code != 200:
            return jsonify({"message": "Modal endpoint error", "error": response.text}), 500
        icon_mesh_url = response.json()["url"]

        collection_meshes.update_one(
            {"_id": mesh_id},
            {"$set": {"iconMeshUrl": icon_mesh_url}}
        )

        return jsonify({
            "message": "Mesh created successful",
            "iconMeshUrl": icon_mesh_url,
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