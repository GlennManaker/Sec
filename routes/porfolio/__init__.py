from flask import Blueprint


bp_portfolio = Blueprint('bp_portfolio', __name__, url_prefix='/api/v1')

from routes.porfolio import portfolio_webhook
from routes.porfolio import portfolio
