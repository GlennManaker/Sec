import stripe
from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
import json
from routes.registration import registration
from pymongo import MongoClient


stripe.api_key = "sk_test_51HkaJuH96yTZyVZDxrA8lRaKERxn6xdtYSLcWBBz22z1HxHGqqDFnhcsp61nFd8Kb0ok25yn1wDK9mULku7mWwJM008yNCeH9x"
app = Flask(__name__)
client = MongoClient("mongodb+srv://dbUser:t9rd4hMMgdN9rDNc@cluster0.31idn.mongodb.net/Finance?retryWrites=true&w=majority")
db = client["users"]
CORS(app)
players_money = dict()
players_money[0] = 0
app.register_blueprint(registration)
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
  x = json.loads(request.get_data())
  print(x)
  session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
      'price_data': {
         'currency': 'usd',
        'product_data': {
          'name': 'Deposit',
        },
        'unit_amount': 500,
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url= "https://stripeuseful.herokuapp.com/api/add_balance/" + str(x["login"]),
    cancel_url='https://example.com/cancel',
  )
  return jsonify(id=session.id)

@app.route('/api/v1/get_balance/<string:user>')
def gets_balance(user):
    dbU = db["users"]
    x = dbU.find_one({'login': user})
    print(x)
    return jsonify({'balance' : x['balance']})
@app.route('/api/add_balance/<string:user>')
def add_balance(user):
    dbU = db["users"]
    x = dbU.find_one({'login' : user})
    dbU.update_one({"login": user}, {"$set": {"balance": x['balance'] + 500}})
    return 'true'
@app.route('/api/retrieve-charge/<string:id>')
def retrieve_charge(id):
    return stripe.Charge.retrieve(id)
@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/api/v1/balance')
def get_balance():
    return stripe.Balance.retrieve()
@app.route('/api/v1/login')
def login():
    x = json.loads(request.get_data())
    login = x["login"]
    password = x["password"]
    dbU = db["users"]
    y = dbU.find_one({"login" : login, "password" : password})
    if not y:
        return {"error" : "no user"}
    else:
        return jsonify({"login" : y['login'], "balance" : y['balance']})
@app.route('/api/check_charge/<string:id>', methods=["GET"])
def check_charge(id):
    x = json.loads(retrieve_charge(id))
    if (x['status'] == 'succeeded'):
        return jsonify({'amount' : x['amount']})
    else:
        return jsonify({'error' : 'status'})

@app.route('/api/v1/register', methods=["POST"])
def register():
    print(request.data)
    x = json.loads(request.get_data())
    login = x["login"]
    password = x["password"]
    dbU = db["users"]
    dbU.insert_many([{"login" : str(login), "password" : str(password), "balance" : 0}])
    return {'complete' : 'ok'}




if __name__ == '__main__':
    app.run()
