#coding: utf8
'''
-----------------------------------------------------------
Author:     David
Date:       2020年1月29日
-----------------------------------------------------------
'''
import sys
sys.path.append('..')
from src.common.tools import request_url




if __name__ == '__main__':
    url = 'http://www.nhc.gov.cn/xcs/yqfkdt/202001/1c259a68d81d40abb939a0781c1fe237.shtml'
    txt = request_url(url)
    print(txt)
