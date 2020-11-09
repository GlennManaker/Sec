from flask import request, jsonify, Blueprint
import json, hashlib
from passlib.hash import sha256_crypt
import app

registration = Blueprint('registration', __name__, url_prefix='/api/v1')

class User:
    def __init__(self, data):
        self.username = data['username']
        self.email = data['username']
        self.password = data['password']
        self.hash_pass = sha256_crypt.encrypt(self.password)
    def toDict(self):
        temp = {'username':self.username,
        'email' : self.email, 'password' : self.hash_pass}
        return temp
@registration.route('/register/user', methods=["POST"])
def register_user():
    data = json.loads(request.get_data())
    user = User(data)
    app.db['users'].insert_one(user.toDict())
    return {'status' : 'new user'}