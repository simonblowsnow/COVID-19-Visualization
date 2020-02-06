#coding: utf8
'''
Created on 2020年1月30日
'''

import sys
sys.path.append('..')
sys.path.append('../..')
import json
import time
from src.libs.log import L
from urllib import parse
from src.common.tools import request_url
from src.libs.utils import TS2S
from src.libs.database import Database
from src.data.region_recognition import REGIONS, check_city
from src.data.region import src_province as SP

# 国内地区名称对应检测
def get_name_privince():
    url = "https://lab.isaaclin.cn/nCoV/api/provinceName"
    rst = request_url(url)
    data = json.loads(rst, encoding = "utf8")
    cache = set(data['results'])
    for p in SP:
        if p['name'] not in cache:
            print(p)
    print(data)
    return data['results']


def get_all_data():
    url = "https://lab.isaaclin.cn/nCoV/api/area?latest=1"
    url = "https://lab.isaaclin.cn/nCoV/api/area?latest=0&province=" + parse.quote("湖北省") 
    rst = request_url(url)
    rst = json.loads(rst, encoding = "utf8")
    with open("data-all.json", "w", encoding="utf8") as fp:
        json.dump(rst["results"], fp, ensure_ascii = False)


        
'''检测数据中的市级行政区域，输出数据中的非标准行政区域'''
def detection_data_citys():
    db = Database()
    unknowns = {}    
    sql = '''SELECT region_parent, region_name FROM patients WHERE region_level=2 
        group by region_parent, region_name'''
    for (parent, name) in db.select(sql):
        if parent not in REGIONS:
            L.error("Not in Region Source: {}".format(parent))
            continue
        if check_city(name, parent): continue
        
        if parent not in unknowns: unknowns[parent] = set()
        unknowns[parent].add(name)

    for p in unknowns:
        print('----------------------')
        print([v['name'] for v in REGIONS[p]['children'].values()])
        print(list(unknowns[p]))
        
  
'''为市级区域增加清洗后的行政区域代码'''    
def add_city_code():
    db = Database()
    sql = "select id, region_name, region_parent FROM patients WHERE region_level=2 and region_code=0"
    comands = []
    for (id_, name, parent) in db.select(sql):
        code = check_city(name, parent)
        if not code: 
            print(parent, name, code)
            continue
        sql = "update patients set region_code=%s where id=%s"
        comands.append([sql, (code, id_)])
    db.Transaction(comands)
    
        
if __name__ == '__main__':
    pass
#     get_all_data()
    detection_data_citys()
