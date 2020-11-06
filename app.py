from flask import Flask, request, jsonify
import stripe
from flask_cors import CORS
stripe.api_key = "sk_test_51HkaJuH96yTZyVZDxrA8lRaKERxn6xdtYSLcWBBz22z1HxHGqqDFnhcsp61nFd8Kb0ok25yn1wDK9mULku7mWwJM008yNCeH9x"
app = Flask(__name__)
CORS(app)
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

@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/api/v1/balance')
def get_balance():
    return stripe.Balance.retrieve()

if __name__ == '__main__':
    app.run()
