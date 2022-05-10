from flask import request, Blueprint
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('52.79.226.1', 27017, username='test', password='test')
db = client.project_map

post_api = Blueprint('post_api', __name__)

@post_api.route("/api/post")
def posttest():
    return "post"

@post_api.route('/last_id', methods=['GET'])
def getid():
    if len(list(db.post.find({}, {'_id': False}))) == 0:
        result = 1
    else:
        result = int(sorted(list(db.post.find({},{'_id':False})), key=lambda x: x['postid'])[-1]['postid']) + 1

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

    receive_postid = request.form['give_postid']
    receive_userid = request.form['give_userid']
    receive_img = request.form['give_img']
    receive_day = request.form['give_day']
    receive_title = request.form['give_title']
    receive_like = request.form['give_like']

    doc = {
        'postid' : receive_postid,
        'userid': receive_userid,
        'img': receive_img,
        'day' : receive_day,
        'title': receive_title,
        'like': int(receive_like)
    }

    db.post.insert_one(doc)
    return jsonify({'result': 'createpoast success'})

@post_api.route('/detail/<keyword>')
def detail_plus(keyword):
    # API에서 단어 뜻 찾아서 결과 보내기
    post_result = db.post.find_one({'postid':str(keyword)},{'_id':False})
    schedule_list = list(db.schedule.find({'postid':str(keyword)},{'_id':False}))
    print(post_result)
    print(schedule_list)
    return render_template("detail.html", post_result=post_result, schedule_list=schedule_list)