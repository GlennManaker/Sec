from flask import Blueprint


bp_profile = Blueprint('bp_profile', __name__, url_prefix='/api/v1')

from routes.profile import profile