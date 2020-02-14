#coding: utf8
'''
-----------------------------------------------------------
Author:     David
Date:       2020年1月29日
-----------------------------------------------------------
'''
import sys
sys.path.append('..')
from src.libs.log import L
from urllib import request, parse
from http import cookiejar
# from selenium import webdriver
# from pyquery import PyQuery as pq
from src.config import Config as C
# import requests


def get_cookie(url):
    cookie = cookiejar.CookieJar()
    handler=request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)
    response = opener.open(url)
    for item in cookie:
        print('Name = %s' % item.name)
        print('Value = %s' % item.value)

def test(url):
    cookie_dict = {}
    driver=webdriver.PhantomJS(executable_path=C.js_path)
    driver.get(url)
    # 获取cookie列表
#     cookie_list=driver.get_cookies()
#     for cookie in cookie_list:
#         cookie_dict[cookie['name']] = cookie['value']
    print(cookie_dict)
    print("=======================================")
    print(driver.page_source)
    # get_cookie(url)
    
#     driver.add_cookie(cookie_dict)
    
#     sleep(3)
#     driver.refresh()

#     driver.get(url)
#     print(driver.page_source)
    
    return
    import urllib
    
    print(requests.get(url, headers={'User-Agent': 'Chrome'}))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3;Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    response = urllib.urlopen(url).read()
    print(response)
    
    
    return res

def request_driver(url):
    driver=webdriver.PhantomJS(executable_path=C.js_path)
    driver.get(url)
    res = driver.page_source
    return res

'''主要请求过程'''    
def request_url(url, text = False, param = {}):
    res = ''
    if 1:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
#             'Connection': 'keep-alive',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#             'Accept-Encoding': 'gzip, deflate',
#             'Accept-Language': 'zh-CN,zh;q=0.9,und;q=0.8,en;q=0.7',
#             'Upgrade-Insecure-Requests': '1',
#             'Cache-Control': 'max-age=0',
#             'Host': 'wjw.hubei.gov.cn',
#             'X-Requested-With': 'XMLHttpRequest',
#             'Cookie': ': ___rl__test__cookies=1580368240830; FSSBBIl1UgzbN7N80S=AGHCUAdqSo3kSSqkFeZ5SD03t5DOiUW3z2K9C2.vYwRTIbY6wczilwmhvUhTKSW4; _trs_uv=k5zh14sp_2998_ej0p; dataHide2=14896cc4-7803-4582-bdd1-dffae2ff408e; Hm_lvt_e37fa67878f8cf7e90f75ce937b18223=1580312117; OUTFOX_SEARCH_USER_ID_NCOO=153694012.12084207; ___rl__test__cookies=1580355003420; Hm_lpvt_e37fa67878f8cf7e90f75ce937b18223=1580355009; _trs_ua_s_1=k60lexyq_2998_f17x; FSSBBIl1UgzbN7N80T=4jc.Gy9B1wHwgtXgeh5k3DD2Mb7cncEp0eS49kJb2FyM_vPMU7CLTzeT.dnZ8YilGuPJERuVKRa8RPMShPVDAO4Yu6fLmQs3UjMD4Abc2PnXWkmM4NJTTQt5V70ywpANnCbL6EHxcN2oHbImRbtIVbZ7WtOE7gLDe92O_QdUkOATovvK7Mmn604lEaRENk9Q9Hztzg73L81CmypxDO8KaCX0Hcaduleqm5kfsbN2vn5yo.XQxmSXWyVOAAiVoiSJNmdRMILZC55TB02IMQujMRq5hKfuaHIWd4hLMA..oXKgYn_oclSQvdRETfpvPq2Ok56eWEkRUQMSK6kV6wy_dqBEs2_2ffWtuPKILnD7GcmaXNG'
            'Cookie': '___rl__test__cookies=1580384615519; insert_cookie=57963235; OUTFOX_SEARCH_USER_ID_NCOO=960198061.7916372; ___rl__test__cookies=1580384608274',
#             'Host': 'sxwjw.shaanxi.gov.cn',
#             'Referer': 'http://sxwjw.shaanxi.gov.cn/',
            'If-Modified-Since': 'Thu, 20 Jan 2020 11:01:41 GMT',
            'If-None-Match': "39e3-59d5961c93058"
        }
        data = bytes(parse.urlencode(param), encoding='utf-8') 
        req = request.Request(url, data=data, headers=headers, method='GET')
        response = request.urlopen(req) 
        rst = response.read()  
        res = str(rst, encoding="utf8")
#         res = pq(res)
#         if text: res = res.text()
#     except Exception as e:
#         L.error(str(e) + url)

    return res 

if __name__ == '__main__':
    pass