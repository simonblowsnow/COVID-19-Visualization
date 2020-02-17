#coding:utf8
'''
Created on 2020年1月29日
'''
import sys
sys.path.append('..')
sys.path.append('../..')

import os
import json
from src.libs.database import Database

FILE_PATH = os.path.dirname(__file__) + "/"


def load_json(code):
    lines = []
    filename = FILE_PATH + str(code) + ".json"
    with open(filename) as load_f:
        dt = json.load(load_f)
        for item in dt['features']:
            print(item)
            
def create_config():
    db = Database()
    sql = "select name, code from region where level=1"
    for (name, code) in db.select(sql):
        print({'name': name, 'code': code, 'url': ''}, ", ")
        
        
def import_region():
    db = Database()
    lines = []
    levels = {'province': 1, 'city': 2, 'district': 3}
    with open("geojson/adcode-map.json", encoding='utf8') as load_f:
        dt = json.load(load_f)
        for item in dt:
            sql = "insert into region (name, code, level) values (%s, %s, %s)"
            param = (item['name'], item['adcode'], levels[item['level']])
            lines.append([sql, param])
    db.Transaction(lines)

def import_region_special():
    db = Database()
    lines = []
    levels = {'province': 1, 'city': 2, 'district': 3}
    for key in ["110000", "500000", "120000", "310000"]:
        with open("geojson/" + key + ".json", encoding='utf8') as load_f:
            dt = json.load(load_f)
            for item in dt["features"]:
                sql = "insert into region (name, code, level, parent) values (%s, %s, %s, %s)"
                param = (item['properties']['name'], item['id'], 2, key)
                lines.append([sql, param])
    db.Transaction(lines)
            
    
def set_region_parent():
    db = Database()
    sql = "select name, code, level from region"
    for (name, code, level) in db.select(sql):
        if len(str(code)) < 6:
            print('code short:', name, code, level)
            continue
        line = []
        if level == 1: line = [code, 86] 
        elif level == 2: line = [code, str(code)[:2] + "0000"]
        elif level == 3: line = [code, str(code)[:4] + "00"]    
        sql = "update region set parent = %s where code = %s"
        db.execute(sql, (line[1], line[0]))
    
    # print(name, code, level)    
    
                
            
if __name__ == '__main__':
#     load_json("china")
#     import_region()
    import_region_special()
#     create_config()
#     set_region_parent()
    pass