#coding: utf8
'''
Created on 2020年2月4日
'''
import sys
sys.path.append('..')

from src.libs.database import Database


'''
    地图数据统一格式：
    [code, value, name, ...]
'''
def getDataChina(level = 1, code=86):
    db = Database()
    whr = "" if level == 1 else " and region_parent={}".format(code)
    sql = '''select a.region_code, region_name, numb_confirmed, numb_suspected, numb_die, numb_ok, 
            a.data_date from patients a 
        join (SELECT region_code, max(data_date) as tm FROM patients 
            where region_level={}'''.format(level) + whr + ''' 
            group by region_code) b 
            on a.region_code=b.region_code and a.data_date=b.tm'''
    lines = []
    for (code, name, confirmed, suspected, die, ok, tm) in db.select(sql):
        lines.append([code, confirmed, name, suspected, die, ok, str(tm)])
        
    return lines

    
    
if __name__ == '__main__':
    for item in getDataChina():
        print(item)
    for item in getDataChina(2, "500000"):
        print(item)