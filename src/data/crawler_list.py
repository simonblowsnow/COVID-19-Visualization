#coding:utf8
'''
Created on 2020年1月30日
'''
import sys
sys.path.append('..')
from src.libs.log import L
from src.data.source import src_province as SP
from src.common.tools import request_url, request_driver
from pyquery import PyQuery as pq
import html


'''
    最早原计划爬取所有卫健委疫情通报，使用文本挖掘提取数据。
   已放弃，因为有现成的……
    "最新疫情通报"
'''
    
conf = {
#     150000: [""]
    650000: [0, 'tr>td', '最新情况'],
    430000: [0, 'tr>td'],
    330000: [0, 'script'],
    610000: [1, 'li'],
    
#     520000: [1, 'li'],  # js source
    350000: [0, 'a'],    # a with data self
    420000: [-1, 'li'], #
    310000: [-1, 'li'] # 
}


def test():
    url = SP
    idx = -1
    methods = [request_url, request_driver]
    for item in SP:
        idx += 1
        url = item['url']
        if url == "" or item['name'] == '西藏自治区': continue
        c = conf.get(item['code'], [0, 'ul>li'])
        if c[0] == -1: continue
        request_html, tag = methods[c[0]], c[1]
        
        current = 22
        if idx == current:
            print(item)
            print(url)
            res = request_html(url)
            res = pq(res)
            ts = res.find(tag).items() 
            if tag == 'script': ts = script_data(ts)
            print(tag)
            for p in ts:
                print(p.text())
                print("------------------------------")
                
            print(item)
        
        if idx > current: break
        
def script_data(items):
    item = [pq(e.text()) for e in items if e.text() != '' and pq(e.text())('datastore') != []][0]
    for p in item.find('recordset>record').items():
        pass
    return
    for item in items:
        print('=====')
        txt = item.text()
        print(txt)

if __name__ == '__main__':
    test()
    pass