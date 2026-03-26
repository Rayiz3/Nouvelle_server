import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from src.routes import users
from flask import Flask
from bson import ObjectId

class TempCollection:
    def __init__(self):
        self._data = [
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

    def find(self):
        return self._data

@pytest.fixture
def app(monkeypatch):
    app = Flask(__name__)

    monkeypatch.setattr(users, "collection_users", TempCollection())

    app.register_blueprint(users.users_bp, url_prefix="/users")
    app.register_blueprint(users.user_bp, url_prefix="/user")

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_users(client):
    response = client.get("/users")

    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]["name"] == "DevUser"
    assert data[0]["email"] == "dev@test.com"
    assert data[1]["name"] == "ArtistUser"