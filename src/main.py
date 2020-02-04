#coding: utf8

import src.libs.platform_version
import os
import json
from flask import Flask, request, Response, current_app, g, render_template, redirect, make_response
from flask_cors import CORS
from src.config import Config as C
# from src.common.key import KEY
from src.libs.log import L
from src.libs.redisEx2 import MyRedis as rs
from src.common.response import NormalResponseJson, NormalResponse, ErrorResponse, ErrorResponseJson, ErrorResponseData

import src.data_china as DC

app = Flask(__name__, static_url_path='')
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'AreUOK'
app.config['TOKEN_EXPIRATION'] = 86400
basedir = os.path.abspath(os.path.dirname(__file__)) + "/static/upload/"




@app.route('/')
def index():
    return "Welcome..."

@app.route('/test')
def test(r):
    R = request.form if request.method=='POST' else request.args
    status = R.get('status', '')
    if status=='': return ErrorResponseJson("请求的参数有误！")
    return NormalResponseJson(request, {'status': status}) 

def getDataChina():
    R = request.form if request.method=='POST' else request.args
    type_ = R.get('type', '')
    data = DC.getDataChina(type_)
    return NormalResponseJson(request, data)

@app.route('/getMap')
def get_map():
    R = request.form if request.method=='POST' else request.args
    name = R.get('id', '')
    path = "data/geojson/{}.json".format(name)
    if not os.path.exists(path):
        return ErrorResponseJson("地图文件不存在")
    
    with open(path, encoding='utf8') as fp:
        data = ''.join(fp.readlines())
        return NormalResponseJson(request, data)
    
    
if __name__ == '__main__':
    L.info("Server Start...")
    app.run(port=C.web.PORT)
    