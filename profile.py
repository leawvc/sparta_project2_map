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

        new_doc = {
            "profile_name": name_receive
        }

        if 'file_give' in request.files:
            file = request.files["file_give"]
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{id}.{extension}"
            file.save("./static/"+file_path)
            new_doc["profile_pic"] = filename
            new_doc["profile_pic_real"] = file_path
        db.users.update_one({'username': payload['id']}, {'$set':new_doc})
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("main"))


# 수정 필요
@profile_api.route('/trip/mypage/<usernmae>', methods=['POST'])
def get_user(username):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (username == payload["id"])

        user_info = db.users.find_one({"id": username}, {"_id": False})
        return render_template('mypage.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("main"))


# 아래 코드로 하면 username 관계없이 나옴(json 리턴은 함) _  토큰값 받아서 id랑 비교 필요함

# @profile_api.route('/mypage/getmypost', methods=['GET'])
# def get_mypost():
#     # token_receive = request.cookies.get('mytoken')
#     username_receive = request.args.get("username_give")
#     my_post = []
#
#     try:
#         # payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         # userid_receive = payload["id"]
#         #내가 작성한 포스트를 가져옴
#         post = db.post.find({'userid': username_receive}, {})
#
#         for result in post:
#             postid = result['postid']
#             title = result['title']
#             img = result['img']
#
#             doc = {
#                 "postid": postid,
#                 "title": title,
#                 "img": img,
#             }
#             my_post.append(doc)
#             # 최신목록 불러오기
#             my_post.reverse()
#
#         return jsonify({"result": "success", "msg": "내 여행 불러옴", "all_post": my_post})
#
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("main"))




# username -> userid로 변경하기
# 일단 username으로 작성하고 추후에 변경
# @profile_api.route('/mypage/getmypost')
# def getmypost():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         # 내 프로필인 경우만 True
#         status = (username == payload["id"])
#         # 해당 유저의 정보
#         user_info = db.users.find_one({"username": username}, {"_id": False})
#         # 해당 유저가 작성한 포스트 정보
#         post_info = db.post.find_one({"userid": username}, {"_id": False})
#
#         return render_template('mypage.html', post_info=post_info, status=status)
#
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError) :
#         return redirect(url_for("main"))


# URL 수정!
# @profile_api.route('/trip/posts/read', methods=['GET'])
# def get_posts():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         username_receive = request.args.get("username_give")
#         if username_receive == "":
#             postlist = list(db.post.find({"username": username_receive}))
#
#         # 마이페이지에서 함수 호출 (내 유저정보 이용)
#         else:
#             postlist = list(db.post.find({"username": username_receive}))
#
#         return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.", "postlist": postlist})
#
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("main"))



### 아이디 바로 payload로 가져오는 방식으로  - 성공 ###
@profile_api.route('/mypage/getmypost')
def get_mypost():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        my_id = payload['id']  # 내 아이디 가져오기

        # 내 아이디랑 비교해서 작성자 userid 가 같으면 가져오기
        mypost = list(db.post.find({'userid': my_id}, {'_id': False}))

        return jsonify({'mypost': mypost})

    except jwt.ExpiredSignatureError:
        return redirect(url_for("main"))

    except jwt.DecodeError:
        return redirect(url_for("main"))
