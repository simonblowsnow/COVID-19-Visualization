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


def get_all_data():
    url = "https://lab.isaaclin.cn/nCoV/api/area?latest=1"
    url = "https://lab.isaaclin.cn/nCoV/api/area?latest=0&province=" + parse.quote("湖北省") 
    rst = request_url(url)
    rst = json.loads(rst, encoding = "utf8")
    with open("data-all.json", "w", encoding="utf8") as fp:
        json.dump(rst["results"], fp, ensure_ascii = False)


        
def translate(items, p, lines):    
    keys = {'confirmedCount': 'numb_confirmed', 'suspectedCount': 'numb_suspected', 
        'curedCount': 'numb_ok', 'deadCount': 'numb_die', 'comment': 'comment'}
    
    for item in items:
        line = dict((keys[k], item[k]) for k in item if k in keys)
        line['data_date'] = TS2S(item['updateTime'] / 1000.0)
        line['region_code'], line['region_name'] = p['code'], p['name']
        line['sum_type'], line['region_level'], line['region_parent'] = 1, 1, 86
        lines.append(line)
        
        if 'cities' in item:
            for ct in item['cities']:
                cline = dict((keys[k], ct.get(k, "")) for k in ct if k in keys)
                cline['sum_type'], cline['region_level'] = 1, 2
                cline['region_name'], cline['region_parent'] = ct['cityName'], p['code']
                cline['data_date'] = line['data_date']
                cline['region_code'] = ct['locationId'] if 'locationId' in ct \
                    else check_city(ct['cityName'], p['code'])
                lines.append(cline)
        '''End If'''
    '''End For'''
    
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
    
    
def request_province_data():
    names = {'香港特别行政区': '香港', '澳门特别行政区': '澳门', '台湾省': '台湾'}
    url = "https://lab.isaaclin.cn/nCoV/api/area?latest=0&province="
    db = Database()
    idx = 0
    for p in SP:
        idx += 1
        if idx <= -1: continue
        purl = url + parse.quote(names.get(p['name'], p['name']))
        rst = request_url(purl)
        rst = json.loads(rst, encoding = "utf8")
        data, lines = rst['results'], []
        translate(data, p, lines)
        L.info("Get data count:" + str(len(data)))
    
        # 存入数据库
        comands = []
        for line in lines: 
            ks = line.keys()
            sql = "insert into patients (" + ','.join(ks) + ") values (" + ', '.join(['%s' for k in ks]) + ")"
            params = [line[k] for k in ks]
            comands.append([sql, params])
        db.Transaction(comands)
        print(idx, p)
#         L.info("{} saved, the index: {}".format(p['name'], idx))
        time.sleep(3)

        
if __name__ == '__main__':
    pass
#     get_all_data()
#     request_province_data()
    add_city_code()
