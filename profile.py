from flask import request, Blueprint, render_template
from pymongo import MongoClient
from werkzeug.utils import redirect, secure_filename
from flask import jsonify, request, redirect, url_for
import jwt

profile_api = Blueprint('profile_api', __name__)

client = MongoClient('52.79.226.1', 27017, username='test', password='test')
db = client.project_map

SECRET_KEY = "team"

@profile_api.route('/trip/mypage/update', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        id = payload["id"]
        name_receive = request.form["name_give"]
        about_receive = request.form["about_give"]
        new_doc = {
            "profile_name" : name_receive
        }
        if 'file_give' in request.files:
            file = request.files["file_give"]
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{id}.{extension}"
            file.save("./static/"+file_path)
            new_doc["profile_pic"] = filename
            new_doc["profile_pic_real"] = file_path
        db.user.update_one({'username': payload['id']}, {'$set':new_doc})
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@profile_api.route('/trip/mypage/<id>', methods=['POST'])
def get_user(id):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (id == payload["id"])

        user_info = db.user.find_one({"id": id}, {"_id": False})
        return render_template('mypage.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("main"))




