from flask import request, Blueprint


post_api = Blueprint('post_api', __name__)

@post_api.route("/api/post")
def posttest():
    return "post"