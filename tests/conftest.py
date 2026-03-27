import os
import sys
import copy

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from src.routes import users, meshes
from flask import Flask
from bson import ObjectId

class InsertOneResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id

class UpdateResult:
    def __init__(self, matched_count):
        self.matched_count = matched_count

class FakeCollection:
    def __init__(self, initial_data=None):
        self._data = copy.deepcopy(initial_data or [])

    def find(self):
        return copy.deepcopy(self._data)
    
    def find_one(self, query):
        for doc in self._data:
            matched = True
            for key, value in query.items():
                if doc.get(key) != value:
                    matched = False
                    break
            if matched:
                return copy.deepcopy(doc)
        return None
    
    def insert_one(self, doc):
        new_doc = dict(doc)
        if "_id" not in new_doc:
            new_doc["_id"] = ObjectId()
        self._data.append(new_doc)
        return InsertOneResult(new_doc["_id"])
    
    def update_one(self, query, update):
        for i, doc in enumerate(self._data):
            matched = True
            for key, value in query.items():
                if doc.get(key) != value:
                    matched = False
                    break
            if matched:
                updated_doc = copy.deepcopy(doc)
                for key, value in update.get("$set", {}).items():
                    updated_doc[key] = value
                self._data[i] = updated_doc

                return UpdateResult(matched_count=1)
        return UpdateResult(matched_count=0)

class FakeResponse:
    def __init__(self, status_code=200, url="https://pub-example.r2.dev/newmesh.glb"):
        self.status_code = status_code
        self._url = url
        self.text = "ok"

    def json(self):
        return {"url": self._url}

@pytest.fixture
def users_collection():
    return FakeCollection([
            {
                "_id": ObjectId(),
                "email": "dev@test.com",
                "password": "password123",
                "name": "DevUser",
                "config": {
                    "color": "#2c3e50",
                    "stacks": ["react","nodejs","docker","postgresql","graphql","aws"],
                    "links": [
                        "https://velog.io/@devlog",
                        "https://github.com/devhub",
                        "https://notion.so/dev-portfolio",
                        "",
                        ""
                    ],
                    "iconMeshUrl": "https://pub-example.r2.dev/devmesh1.glb"
                }
            },
            {
                "_id": ObjectId(),
                "email": "artist@test.com",
                "password": "password456",
                "name": "ArtistUser",
                "config": {
                    "color": "#8e44ad",
                    "stacks": ["blender","unrealengine","substancepainter","photoshop","aftereffects"],
                    "links": [
                        "https://artstation.com/artist_portfolio",
                        "https://behance.net/creativeworks",
                        "https://youtube.com/@3dcreator",
                        "https://instagram.com/visual_creator",
                        ""
                    ],
                    "iconMeshUrl": "https://pub-example.r2.dev/devmesh2.glb"
                }
            }
        ]
    )

@pytest.fixture
def meshes_collection():
    return FakeCollection([
            {
                "_id": ObjectId(),
                'user_id': '1234',
                'prompt': 'game controller',
                'iconMeshUrl': 'https://pub-example.r2.dev/mesh1.glb',
            },
            {
                "_id": ObjectId(),
                'user_id': '5678',
                'prompt': 'spaceship',
                'iconMeshUrl': 'https://pub-example.r2.dev/mesh2.glb',
            }
        ]
    )

@pytest.fixture
def users_app(monkeypatch, users_collection):
    app = Flask(__name__)

    monkeypatch.setattr(users, "collection_users", users_collection)

    app.register_blueprint(users.users_bp, url_prefix="/users")
    app.register_blueprint(users.user_bp, url_prefix="/user")

    return app

@pytest.fixture
def users_client(users_app):
    return users_app.test_client()

@pytest.fixture
def meshes_app(monkeypatch, meshes_collection):
    app = Flask(__name__)

    monkeypatch.setattr(meshes, "collection_meshes", meshes_collection)
    monkeypatch.setattr(meshes.requests, "post", lambda *args, **kwargs: FakeResponse())

    app.register_blueprint(meshes.meshes_bp, url_prefix="/meshes")

    return app

@pytest.fixture
def meshes_client(meshes_app):
    return meshes_app.test_client()