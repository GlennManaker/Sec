from flask import Blueprint


bps_webhook = Blueprint('bps_webhook', __name__, url_prefix='/api/v1')

from routes.webhook import stripe_webhooks