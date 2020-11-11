import datetime
import jwt
from flask import request, jsonify, Blueprint, make_response, current_app
import json, hashlib
from passlib.hash import sha256_crypt
import app

bp_registration = Blueprint('bp_registration', __name__, url_prefix='/api/v1')
class User:
    def __init__(self, data):
        self.username = data['username']
        self.email = data['username']
        self.password = data['password']
        self.balance = int(0)
        self.hash_pass = sha256_crypt.encrypt(self.password)
    def toDict(self):
        temp = {'username':self.username,
        'email' : self.email, 'password' : self.hash_pass, 'balance' : self.balance}
        return temp
@bp_registration.route('/register/user', methods=["POST"])
def register_user():
    try:
        data = json.loads(request.get_data())
        if not data or not data['username'] or not data['password']:
            return make_response('Could not register', 400, {'WWW-Authenticate' : 'Basic realm="Unregistered"'})
        user = User(data)
        _id = app.db['users'].insert_one(user.toDict()).inserted_id
        print(str(_id))
        token = jwt.encode({'_id': str(_id), 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)},
                           current_app.config['SECRET_KEY'])
        return {
            'message' : 'new user',
            'token' :  token.decode('UTF-8') }
    except:
        return make_response('Could not register', 400, {'WWW-Authenticate': 'Basic realm="Unregistered"'})