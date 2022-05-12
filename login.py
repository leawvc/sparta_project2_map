from flask import request, Blueprint
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

client = MongoClient('52.79.226.1', 27017, username='test', password='test')
db = client.project_map

login_api = Blueprint('login_api', __name__)

SECRET_KEY = "team"


@login_api.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # payload로부터 아이디 들고 와서 클라이언트로 보냄
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('index.html', user_info=user_info, status='yes', userid=payload['id'])
    except jwt.ExpiredSignatureError:
        return render_template('index.html', status='no')
    except jwt.exceptions.DecodeError:
        return render_template('index.html', status='no')


@login_api.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@login_api.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    # 패스워드 해쉬 값으로 변환
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            # 하루동안 유효한 로그인 클라 아이디 패스워드 받아서 서버에 보냄 섭가 db에 매칭해서 맞으면 jwt 토큰에 답아서 클라에 던져줌
            # 쿠키 확인은 콘솔 창에서 application cokiees확인
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 회원 가입(4)
@login_api.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    # 패스워드 받고 아이디 해쉬태그와
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@login_api.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    # request.form으로 유저 네임 받아서 회원 가입(2)
    username_receive = request.form['username_give']
    # 유저 네임이 하나라도 찾는다면 bool로 묶었기 때문에 존재하면 true 없으면 false
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})
