from flask import Flask, request, jsonify, make_response, Blueprint, current_app
from passlib.hash import sha256_crypt
from bson.objectid import ObjectId
import datetime, json
import jwt
from functools import wraps
import app
bp_auth = Blueprint('bp_auth', __name__, url_prefix='/api/v1')
def token_required(f):
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = app.db['users'].find_one({"_id": ObjectId(data['_id'])})
            current_user = {'username' : user['username']}
        except jwt.ExpiredSignatureError:
            return jsonify({'message' : 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@bp_auth.route('/check_token', methods = ["GET"])
@token_required
def check_token(current_user):
    return 'True token for ' + current_user['username']

@bp_auth.route('/login', methods = ["POST"])
def login():
    auth = json.loads(request.get_data())
    if not auth or not auth['username'] or not auth['password']:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    user = app.db['users'].find_one({"username" : auth['username']})
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    if sha256_crypt.verify(auth['password'], user['password']):
        token = jwt.encode({'_id' : str(user['_id']), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=30)}, current_app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

