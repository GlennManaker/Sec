from flask import request, jsonify
import json
import stripe
from routes.API_payments import bp_payment
from routes.auth import token_required
@bp_payment.route('/create-checkout-session', methods=['POST'])
@token_required
def create_checkout_session(current_user):
    x: object = json.loads(request.get_data())
    print(x)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Deposit for ' + current_user,
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
