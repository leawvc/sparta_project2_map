from flask import request, Blueprint
from pymongo import MongoClient
from flask import jsonify, request, redirect, url_for
import jwt

SECRET_KEY = "team"

index_api = Blueprint('index_api', __name__)

client = MongoClient('52.79.226.1', 27017, username='test', password='test')
db = client.project_map

@index_api.route('/trip/index/read', methods=['GET'])
def index():

    receive_local = request.args.get('give_local')
    local_list = receive_local.replace(',',' ').split()
    print(local_list)

    postid_list = []
    for i in local_list:
        for j in list(db.schedule.find({'address':{'$regex':i}},{'_id':False})):
            postid_list.append(int(j['postid']))

    postid_list = list(set(postid_list))

    result = []
    for i in postid_list:
        result.append(db.post.find_one({'postid': i},{'_id':False}))

    return jsonify({'result': result})