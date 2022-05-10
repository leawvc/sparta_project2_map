from flask import request, Blueprint


login_api = Blueprint('login_api', __name__)

@login_api.route("/api/login")
def logintest():
    return "test"