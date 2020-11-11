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
        useremail = pay['data']['object']['charges']['data'][0]['billing_details']['email']
        print(pay['data']['object']['charges']['data'][0]['billing_details']['email'])
        print(useremail)
        if (pay['type'] == 'payment_intent.succeeded'):
            # payment = Payment(pay['data'])
            user = app.db['payments'].find_one({'email' : useremail})
            print(user)
            app.db['payments'].insert_one({'id' : pay['data']['object']['id'], 'time': pay['created'], 'amount':
                                           pay['data']['object']['amount'], 'username': user['username']})
            app.db['payments'].update_one({"username" : user['username']}, {"$inc" : {"amount": int(pay['data']['object']['amount'])}})
        return Response(status=200)