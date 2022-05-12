from flask import request, Blueprint
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import jwt
app = Flask(__name__)

client = MongoClient('52.79.226.1', 27017, username='test', password='test')
db = client.project_map
SECRET_KEY = "team"
from datetime import datetime

post_api = Blueprint('post_api', __name__)

@post_api.route("/api/post")
def posttest():
    return "post"

@post_api.route('/last_id', methods=['GET'])
def getid():
    if len(list(db.post.find({}, {'_id': False}))) == 0:
        result = 1
    else:
        print(list(db.post.find({},{'_id':False})))
        result = int(sorted(list(db.post.find({},{'_id':False})), key=lambda x: x['postid'])[-1]['postid'])+1

    print(result)

    return jsonify({'result': result})

@post_api.route('/trip/schedule/create', methods=['POST'])
def createschedule():

    receive_postid = request.form['give_postid']
    receive_date = request.form['give_date']
    receive_place_name = request.form['give_place_name']
    receive_address = request.form['give_address']
    receive_x = request.form['give_x']
    receive_y = request.form['give_y']
    receive_phone = request.form['give_phone']
    receive_url = request.form['give_url']


    doc = {
        'postid': receive_postid,
        'date': receive_date,
        'place_name': receive_place_name,
        'address': receive_address,
        'x': receive_x,
        'y': receive_y,
        'phone': receive_phone,
        'place_url': receive_url
    }

    db.schedule.insert_one(doc);
    return jsonify({'result': 'success'})

@post_api.route('/trip/schedule/read', methods=['GET'])
def readschedule():
    receive_postid = request.args.get('give_postid')
    result = list(db.schedule.find({'postid':receive_postid},{'_id':False}))
    return jsonify({'result': result})


@post_api.route('/trip/schedule/delete', methods=['POST'])
def deleteschedule():

    receive_postid = request.form['give_postid']
    receive_date = request.form['give_date']
    receive_x = request.form['give_x']
    receive_y = request.form['give_y']

    print(receive_postid, receive_date, receive_x, receive_y)

    db.schedule.delete_one({'postid':receive_postid, 'date': receive_date, 'x':receive_x, 'y':receive_y})
    return jsonify({'result': 'schedule delete success'})

@post_api.route('/trip/schedule/alldelete', methods=['POST'])
def alldelete():
    receive_postid = request.form['give_postid']
    db.schedule.delete_many({'postid':receive_postid})

    return jsonify({'result': 'all_delete success'})

@post_api.route('/trip/posts/create', methods=['POST'])
def createpost():
    token_receive = request.cookies.get('mytoken')
    print("post 만들기")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        # 포스팅 생성
        user_info = db.users.find_one({"username": payload["id"]})
        receive_postid = request.form['give_postid']
        file = request.files['give_img']
        receive_day = request.form['give_day']
        receive_title = request.form['give_title']
        receive_like = 0

        extension = file.filename.split('.')[-1]

        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

        filename = f'file-{mytime}'

        save_to = f'static/{filename}.{extension}'
        file.save(save_to)

        doc = {
            "userid": user_info["username"],
            "postid": int(receive_postid),
            'img': f'{filename}.{extension}',
            'day' : receive_day,
            'title': receive_title,
            'like': int(receive_like),
            'time': today.strftime('%Y.%m.%d'),
            'like_by_me': False
        }

        db.post.insert_one(doc)
        return jsonify({"result": "success", "msg": '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@post_api.route('/trip/posts/read', methods=['GET'])
def readallpost():
    result = list(db.post.find({}, {'_id': False}).sort('postid', -1).limit(20))
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        for post in result:
            cntlike = db.like.count_documents({'postid': str(post['postid'])})
            like_by_me = bool(db.like.find_one({"postid": str(post["postid"]), "username": payload['id']}))
            print(cntlike, like_by_me)
            db.post.update_one({'postid':post['postid']}, {"$set":{"like":cntlike}})
            db.post.update_one({'postid':post['postid']}, {"$set":{"like_by_me":like_by_me}})
        result = list(db.post.find({}, {'_id': False}).sort('postid', -1).limit(20))
        return jsonify({'result': result, 'msg':'success'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return jsonify({'result': result, 'msg':'success'})

@post_api.route('/detail/<keyword>')
def detail_plus(keyword):
    # API에서 단어 뜻 찾아서 결과 보내기
    post_result = db.post.find_one({'postid':int(keyword)},{'_id':False})
    schedule_list = list(db.schedule.find({'postid':str(keyword)},{'_id':False}))
    print(post_result)
    print(schedule_list)
    return render_template("detail.html", post_result=post_result, schedule_list=schedule_list)

@post_api.route('/trip/posts/delete', methods=['POST'])
def delete_post():
    post_postid = request.form['postid']
    db.post.delete_one({"postid": int(post_postid)})
    db.schedule.delete_many({"postid": str(post_postid)})
    db.like.delete_many({"postid": str(post_postid)})
    return jsonify({'result': 'success', 'msg': '삭제 했습니다.'})



