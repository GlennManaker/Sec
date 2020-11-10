from flask import Blueprint


bp_payment = Blueprint('bp_payment', __name__, url_prefix='/api/v1')

from routes.API_payments import payment