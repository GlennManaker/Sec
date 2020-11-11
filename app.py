import stripe
from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

stripe.api_key = "sk_test_51HkaJuH96yTZyVZDxrA8lRaKERxn6xdtYSLcWBBz22z1HxHGqqDFnhcsp61nFd8Kb0ok25yn1wDK9mULku7mWwJM008yNCeH9x"
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
client = MongoClient("mongodb+srv://dbUser:t9rd4hMMgdN9rDNc@cluster0.31idn.mongodb.net/Finance?retryWrites=true&w=majority")
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


if __name__ == '__main__':
    app.run()
