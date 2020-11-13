from flask import request,jsonify
from app import db
from routes.porfolio import bp_portfolio
from routes.auth import token_required
import requests,json

@bp_portfolio.route('/user/portfolio', methods=["GET"])
@token_required
def get_portfolio(current_user):
    portf = db['portfolio'].find_one({'username' : current_user['username']})
    if portf:
        del portf['_id']
    return jsonify(portf)
queryString ="https://query1.finance.yahoo.com/v8/finance/chart/?symbol={}&period1={}&period2={}&interval=1d"
@bp_portfolio.route('/history/portfolio', methods = ["GET"])
@token_required
def histPortfolio(current_user):
    history = db['historyPortfolio'].find({'username' : current_user['username']}).sort('time', 1)
    result = []
    for his in history:
        del his['_id']
        result.append(his)
    used = dict()
    tickers = ['AAPL', 'ATVI']
    for t in tickers:
        query = queryString.format(t, result[0]['time'], 9999999999)
        req = requests.get(query)
        result.append(json.loads(req.text))



    return jsonify(result)