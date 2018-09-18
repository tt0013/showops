#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

from flask import Flask, request, Response
from flask_restful import reqparse, abort, Api, Resource
import json
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
api = Api(app)

parser_post = reqparse.RequestParser()
parser_post.add_argument("todo")
# parser_post.add_argument("user", type=str, required=True)
# parser_post.add_argument("pwd", type=str, required=True)



def to_do(arg1, args2):
    return str(arg1)+str(args2)

# 操作（post / get）资源列表
class TodoList(Resource):

    def post(self):
        args = parser_post.parse_args()
        print(args)
        # 构建新参数
        # user = args['user']
        # pwd = args['pwd']
        # # 调用方法to_do
        # info = {"info": to_do(user, pwd)}
        # # 资源添加成功，返回201
        # return info,201
        return 123



# 设置路由，即路由地址为http://127.0.0.1:5000/users
api.add_resource(TodoList, "/json")

# @app.route('/json', methods=['POST'])
# def my_json():
#     print(request.headers)
#     print(request.json)
#     rt = {'info':'hello '+request.json['week']}
#     return Response(json.dumps(rt),  mimetype='application/json')


if __name__ == '__main__':
    app.run(host='192.168.5.105',port='8002',debug=True)