#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

from flask import Flask, abort, request, jsonify
import json

app = Flask(__name__)

# 测试数据暂时存放
tasks = []

@app.route('/add_task/', methods=['POST'])
def add_task():
    print(request.json['platform'])
    if not request.json or 'id' not in request.json or 'info' not in request.json:
        abort(400)
    task = {
        'platform': request.json['platform']






    }
    tasks.append(task)
    return jsonify({'result': 'success'})


@app.route('/get_task/', methods=['GET'])
def get_task():
    if not request.args or 'id' not in request.args:
        # 没有指定id则返回全部
        return jsonify(tasks)
    else:
        task_id = request.args['id']
        task = filter(lambda t: t['id'] == int(task_id), tasks)
        return jsonify(task) if task else jsonify({'result': 'not found'})


if __name__ == '__main__':
    app.run(host='192.168.5.105',port='8002',debug=True)