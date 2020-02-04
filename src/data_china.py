#coding: utf8
'''
Created on 2020年2月4日
'''

from src.libs.database import Database


'''
    地图数据统一格式：
    [code, value, name, ...]
'''
def getDataChina(type_):
    db = Database()
    sql = '''select a.region_code, region_name, numb_confirmed, numb_suspected, numb_die, numb_ok, 
            a.data_date from patients a 
        join (SELECT region_code, max(data_date) as tm FROM `patients` 
            where region_level=1 group by region_code) b 
            on a.region_code=b.region_code and a.data_date=b.tm'''
    lines = []
    for (code, name, confirmed, suspected, die, ok, tm) in db.select(sql):
        lines.append([code, confirmed, name, suspected, die, ok, str(tm)])
        
    return lines
    
    
    
if __name__ == '__main__':
    getDataChina()
    