from flask import Flask, request, jsonify, make_response, Blueprint, current_app
from passlib.hash import sha256_crypt
from bson.objectid import ObjectId
import datetime, json
import jwt
import app
from routes.auth import token_required
from routes.profile import bp_profile

@bp_profile.route('/profile', methods=["GET"])
@token_required
def get_profile(current_user):
    user = app.db['users'].find_one({'username' : current_user['username']})
    return jsonify({'username' : user['username'] , 'email' : user['email'] , 'balance' : user['balance']})

@bp_profile.route('/history/deposits', methods=["GET"])
@token_required
def get_deposits(current_user):
    deposits = app.db['payments'].find({'username' : current_user['username']})
    data = []
    for one in deposits:
        data.append({'time' : one['time'], 'amount' : one['amount']})
    return jsonify({'currency' : 'usd', 'data' : data})
