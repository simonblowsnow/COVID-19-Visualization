#coding: utf8
'''
Created on 2020年1月30日
'''

import sys
sys.path.append('..')
sys.path.append('../..')
import time
import threading
from src.libs.log import L
from src.data.dxy_record import request_data_province

    
def worker():
    try:
        request_data_province()
        L.info("Sleep now, worker will run after 30 minutes")
    except:
        pass
        
def run():
    while True:
        t = threading.Thread(target=worker)
        t.start()
        time.sleep(1800)
    
if __name__ == '__main__':
    run()
