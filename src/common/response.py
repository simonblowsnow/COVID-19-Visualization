#coding:utf8

'''
------------------------------------------------------------
Description:    
Author:              Simon
Date:                Created on 2019年9月3日
------------------------------------------------------------
'''
import json

'''请求错误返回格式'''
def ErrorResponse(request, message = "请求错误！", data = {}):
    callback = request.args.get('callback', '')
    rst = { 'error': True, 'message': message, 'data': data }
    
    return callback + "(" + json.dumps(rst, ensure_ascii = False) + ")"

'''请求错误返回格式'''
def ErrorResponseJson(message = "请求错误！", data = {}, errCode = '001'):
    rst = { 'error': True, 'message': message, 'data': data, 'code': errCode }
    
    return json.dumps(rst, ensure_ascii = False)

'''请求错误返回格式'''
def ErrorResponseData(data = {}):
    return json.dumps(data, ensure_ascii = False)

'''请求标准返回格式'''
def NormalResponseJson(request, data):
    rst = { 'error': 0, 'code':None, 'message': "请求成功", 'data': data }
    return json.dumps(rst, ensure_ascii = False)

'''请求标准返回格式'''
def NormalResponse(request, data):
    callback = request.args.get('callback', '')
    rst = { 'error': False, 'message': "OK", 'data': data }
    
    return callback + "(" + json.dumps(rst, ensure_ascii = False) + ")"


if __name__ == '__main__':
    pass