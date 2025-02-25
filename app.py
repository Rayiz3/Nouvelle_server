from flask import Flask
from flask_cors import CORS
from src.routes.users import users_bp


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(users_bp, url_prefix='/users')

if __name__ == '__main__':
    app.run(debug=True)