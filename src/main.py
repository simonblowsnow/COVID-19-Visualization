#coding: utf8

import sys
sys.path.append('..')

import os
import src.libs.platform_version
import json
from flask import Flask, request, Response, current_app, g, render_template, redirect, make_response
from flask_cors import CORS
from src.config import Config as C
# from src.common.key import KEY
from src.libs.log import L
from src.common.response import NormalResponseJson, NormalResponse, ErrorResponse, ErrorResponseJson, ErrorResponseData

import src.data_china as DC
import src.data_pos as DP

app = Flask(__name__, static_url_path='')
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'AreUOK'
app.config['TOKEN_EXPIRATION'] = 86400
BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + "/static/upload/"
FILE_PATH = os.path.dirname(__file__) + "/"



@app.route('/')
def index():
    return "Welcome..."

@app.route('/test')
def test(r):
    R = request.form if request.method=='POST' else request.args
    status = R.get('status', '')
    if status=='': return ErrorResponseJson("请求的参数有误！")
    return NormalResponseJson(request, {'status': status}) 

@app.route('/getDataSummary')
def get_data_summary():
    R = request.form if request.method=='POST' else request.args
    level = int(R.get('level', 1))
    code = R.get('name', '86')
    if code == 'china' or code == '': code = '86'
    
    data = DC.get_data_summary(level, code)
    return NormalResponseJson(request, data)

@app.route('/getDataDetails')
def get_data_details():
    R = request.form if request.method=='POST' else request.args
    level = int(R.get('level', 1))
    code = R.get('name', '')
    
    data = DC.get_data_latest(level, code)
    return NormalResponseJson(request, data)

@app.route('/getTimeData')
def get_time_data():
    R = request.form if request.method=='POST' else request.args
    level = int(R.get('level', 1))
    code = R.get('name', '86')
    if code == 'china' or code == '': code = '86'
    
    data = DC.get_time_data(level, int(code))
    return NormalResponseJson(request, data)

@app.route('/getDataPos')
def get_data_pos():
    R = request.form if request.method=='POST' else request.args
    code = R.get('code', '420000')
    
    data = DP.get_region_data(int(code))
    return NormalResponseJson(request, data)


@app.route('/getMap')
def get_map():
    R = request.form if request.method=='POST' else request.args
    name = R.get('id', '')
    path = FILE_PATH + "/data/geojson/{}.json".format(name)
    if not os.path.exists(path):
        return ErrorResponseJson("地图文件不存在")
    
    with open(path, encoding='utf8') as fp:
        data = ''.join(fp.readlines())
        return NormalResponseJson(request, data)
    
    
if __name__ == '__main__':
    L.info("Server Start...")
    app.run(port=C.web.PORT)
    