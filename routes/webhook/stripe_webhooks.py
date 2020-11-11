from flask import Flask, jsonify, request, Blueprint, make_response, Response
import json
from routes.webhook import bps_webhook
import app
class Payment:
    def __init__(self,data):
            self.username = data['object']['description'][12:]
            self.time = data['object']['created']
            self.amount = data['object']['amount']
            self.id = data['object']['id']
    def __str__(self):
        return str(self.username) + str(self.time) + str(self.amount) + str(self.id)
    def toDict(self):
        return {'username' : self.username, 'time' : self.time, 'amount' : self.amount, 'id' : self.id}
@bps_webhook.route('/webhook', methods = ["POST"])
def get_webhook():
        pay = json.loads(request.get_data())
        print(pay['data']['object'])
        if (pay['type'] == 'payment_intent.succeeded'):
            payment = Payment(pay['data'])
            app.db['payments'].insert_one(payment.toDict())
            app.db['payments'].update({"username" : payment.username}, {"$inc" : {"amount": 500}})
        return Response(status=200)
