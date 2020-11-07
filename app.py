import stripe
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from pymongo import MongoClient
stripe.api_key = "sk_test_51HkaJuH96yTZyVZDxrA8lRaKERxn6xdtYSLcWBBz22z1HxHGqqDFnhcsp61nFd8Kb0ok25yn1wDK9mULku7mWwJM008yNCeH9x"
app = Flask(__name__)
client = MongoClient("mongodb+srv://dbUser:t9rd4hMMgdN9rDNc@cluster0.31idn.mongodb.net/Finance?retryWrites=true&w=majority")
db = client.users
CORS(app)
players_money = dict()
players_money[0] = 0
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
  session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
      'price_data': {
         'currency': 'usd',
        'product_data': {
          'name': 'Deposit',
        },
        'unit_amount': 100,
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url= "https://yoursite.com/success.html",
    cancel_url='https://example.com/cancel',
  )

  return jsonify(id=session.id)
@app.route('/api/retrieve-charge/<string:id>')
def retrieve_charge(id):
    return stripe.Charge.retrieve(id)
@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/api/v1/balance')
def get_balance():
    return stripe.Balance.retrieve()
@app.route('/api/check_charge/<string:id>', methods=["GET"])
def check_charge(id):
    x = json.loads(retrieve_charge(id))
    if (x['status'] == 'succeeded'):
        return jsonify({'amount' : x['amount']})
    else:
        return jsonify({'error' : 'status'})

@app.route('/api/v1/register', methods=["POST"])
def register():
    login = request.headers['user']['login']
    password = request.headers['user']['password']
    dbU =  db['users']
    dbU.inset_one({'login' : login, 'password' : password})
    return {'complete' : 'ok'}




if __name__ == '__main__':
    app.run()
