import os
from flask import Flask
from flask_cors import CORS
from src.routes.users import users_bp, user_bp


app = Flask(__name__)
PORT = int(os.environ.get("PORT", 5000))

CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True)