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
from src.libs.utils import TS2S, date_less
from src.libs.database import Database
from src.data.region_recognition import REGIONS, check_city
from src.data.region import src_province as SP


def test_get_data():
    url = "https://lab.isaaclin.cn/nCoV/api/area?latest=1"
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
        
        if item.get('cities', None):
            for ct in item['cities']:
                cline = dict((keys[k], ct.get(k, "")) for k in ct if k in keys)
                cline['sum_type'], cline['region_level'] = 1, 2
                cline['region_name'], cline['region_parent'] = ct['cityName'], p['code']
                cline['data_date'] = line['data_date']
                cline['region_code'] = ct.get('locationId', 0)
                '''行政编码和级别判断'''
                if cline['region_code'] not in  REGIONS[p['code']]['children']:
                    cline['region_code'] = check_city(ct['cityName'], p['code'])
                    if not cline['region_code']: cline['region_level'] = 3

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

'''
各地区数据最新时间
前提：历史数据是准确的，不会在后期有改动
'''
def getLatest(db=None):
    if not db: db = Database()
    dt = {}
    sql = '''select region_code, region_name, region_parent, max(data_date) from patients \
        group by region_code, region_name, region_parent'''
    for (code, name, parent, tm) in db.select(sql):
        dt['_'.join([str(code), name, str(parent)])] = tm
        
    return dt    

def request_data(url, name):
    err_count = 0
    while True:
        try:
            rst = request_url(url)
            rst = json.loads(rst, encoding = "utf8")
            return rst
        except:
            err_count += 1
            L.info("Error request found when {}, the {} times".format(name, err_count))
            if err_count > 10: return None
            time.sleep(3)
    return None

'''
    各省核心数据请求，含港澳台地区
        逻辑前提：中国数据等于各省数据之和
'''    
def request_data_province():
    names = {'香港特别行政区': '香港', '澳门特别行政区': '澳门', '台湾省': '台湾'}
    url = "https://lab.isaaclin.cn/nCoV/api/area?latest=0&province="
    db = Database()
    history = getLatest(db)
    idx = 0
    for p in SP:
        idx += 1
        # if idx <= 23: continue
        purl = url + parse.quote(names.get(p['name'], p['name']))
        rst = request_data(purl, p['name'])
        if not rst: continue
        data, lines = rst['results'], []
        translate(data, p, lines)
        L.info("Get data collects count:" + str(len(data)))
        
        comands = []
        for line in lines:
            '''排除已有历史数据''' 
            key = '_'.join([str(line['region_code']), line['region_name'], str(line['region_parent'])])
            if key in history and not date_less(history[key], line['data_date']): continue 
            
            ks = line.keys()
            sql = "insert into patients (" + ','.join(ks) + ") values (" + ', '.join(['%s' for k in ks]) + ")"
            params = [line[k] for k in ks]
            comands.append([sql, params])
        L.info("New data lines count:" + str(len(comands)))
        if len(comands) > 0: db.Transaction(comands)
        L.info("{}\t {}  finished!".format(idx, p['name']))
        time.sleep(3)

'''暂未使用（本项目当前只关心国内）'''
def request_data_overall():
    url = "https://lab.isaaclin.cn/nCoV/api/overall?latest=0"
    rst = request_data(url, "全国")
    if not rst: return 
    data, lines = rst['results'], []
   
    
if __name__ == '__main__':
    pass
#     test_get_data()
    request_data_province()
#     request_data_overall()
#     add_city_code()
