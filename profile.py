from flask import request, Blueprint

profile_api = Blueprint('profile_api', __name__)

@profile_api.route("/api/profile")
def profiletest():
    return "profile"