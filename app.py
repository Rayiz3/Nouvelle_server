import os
from flask import Flask
from flask_cors import CORS
from src.routes.users import users_bp, user_bp
from src.routes.meshes import meshes_bp


app = Flask(__name__)
PORT = int(os.environ.get("PORT", 8080))

CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(meshes_bp, url_prefix='/meshes')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True)