from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from like import like_api
from login import login_api
from post import post_api
from profile import profile_api
from schedule import schedule_api
import jwt
SECRET_KEY = "team"

app = Flask(__name__)

app.register_blueprint(like_api)
app.register_blueprint(login_api)
app.register_blueprint(post_api)
app.register_blueprint(profile_api)
app.register_blueprint(schedule_api)

client = MongoClient('52.79.226.1', 27017, username='test', password='test')
db = client.project_map

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/plan')
def plan():
    return render_template('plan.html')

@app.route('/mypage')
def mypage():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('mypage.html', id = payload['id'])
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("main"))


# @app.route('/detail')
# def detail():
#     return render_template('detail.html')

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)