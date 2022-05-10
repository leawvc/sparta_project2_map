from flask import request, Blueprint


like_api = Blueprint('like_api', __name__)

@like_api.route("/api/like")
def liketest():
    return "like_api"