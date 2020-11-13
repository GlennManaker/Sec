import stripe
from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

stripe.api_key = os.environ.get('stripe_key')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
client = MongoClient(os.environ.get('database'))
db = client["users"]
CORS(app)
players_money = dict()
players_money[0] = 0

from routes.registration import bp_registration
app.register_blueprint(bp_registration)

from routes.auth import bp_auth
app.register_blueprint(bp_auth)

from routes.API_payments import bp_payment
app.register_blueprint(bp_payment)

from routes.profile import bp_profile
app.register_blueprint(bp_profile)

from routes.webhook import bps_webhook
app.register_blueprint(bps_webhook)

from routes.porfolio import bp_portfolio
app.register_blueprint(bp_portfolio)

if __name__ == '__main__':
    app.run()
