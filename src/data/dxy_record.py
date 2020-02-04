#coding: utf8
'''
Created on 2020年1月30日
'''

import sys
from idlelib.iomenu import encoding
sys.path.append('..')
import json
import time
from src.libs.log import L
from urllib import parse
from src.data.source import src_province as SP
from src.common.tools import request_url
from src.libs.utils import TS2S
from src.libs.database import Database

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

'''
Return:
    {150000: {'name': '内蒙古自治区', 'children': 
            { 150800: {'name': '巴彦淖尔市'} }
        }
    }
'''
def get_region_citys():
    db = Database()
    sql = "select name, code, level, parent from region"
    regions = {}
    for (name, code, level, parent) in db.select(sql):
        if level > 2: continue
        if level == 0: continue
        one = code if level == 1 else parent 
        if one not in regions: regions[one] = {'children': {}}
        if level == 1: regions[code]['name'] = name 
        if level == 2: regions[parent]['children'][code] = {'name': name}
    
    return regions

def get_all_data():
    url = "https://lab.isaaclin.cn/nCoV/api/area?latest=1"
    url = "https://lab.isaaclin.cn/nCoV/api/area?latest=0&province=" + parse.quote("湖北省") 
    rst = request_url(url)
    rst = json.loads(rst, encoding = "utf8")
    with open("data-all.json", "w", encoding="utf8") as fp:
        json.dump(rst["results"], fp, ensure_ascii = False)
            

def get_name_citys():
    
    pass
        
#         data = rst['results']
#         lines = []
    

        
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
                cline['region_code'] = 0
                # region_code 暂时置为0，稍后清洗标准化行政区划
                lines.append(cline)
        '''End If'''
    '''End For'''
    
    
def get_province():
    names = {'香港特别行政区': '香港', '澳门特别行政区': '澳门', '台湾省': '台湾'}
    url = "https://lab.isaaclin.cn/nCoV/api/area?latest=0&province="
    db = Database()
    idx = 0
    for p in SP:
        idx += 1
        if idx <= 0: continue
        purl = url + parse.quote(names.get(p['name'], p['name']))
        rst = request_url(purl)
        rst = json.loads(rst, encoding = "utf8")
        data, lines = rst['results'], []
        print(len(data))
        
        translate(data, p, lines)
    
        # 存入数据库
        comands = []
        for line in lines: 
            ks = line.keys()
            sql = "insert into patients (" + ','.join(ks) + ") values (" + ', '.join(['%s' for k in ks]) + ")"
            params = [line[k] for k in ks]
            comands.append([sql, params])
        db.Transaction(comands)
        print(idx, p)
        time.sleep(3)
         
#     provinceName
    
if __name__ == '__main__':
    pass
#     get_name_citys()
#     get_region_citys()
#     get_all_data()
    get_province()

