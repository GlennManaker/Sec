from flask import request, jsonify
import json
import stripe
from routes.API_payments import bp_payment
@bp_payment.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    x: object = json.loads(request.get_data())
    print(x)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Deposit',
                },
                'unit_amount': int(x['amount']),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url="https://example.com/success",
        cancel_url='https://example.com/cancel',
    )
    return jsonify(id=session.id)
