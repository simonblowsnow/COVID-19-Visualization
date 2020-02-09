#coding: utf8
'''
Created on 2020年2月4日
'''
import sys
sys.path.append('..')

from src.libs.database import Database
from src.data.region import src_province

'''
    地图数据统一格式：
    [code, value, name, ...]
'''
def get_data_latest(level = 1, code=86):
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

'''
Return: {
    '2020-02-09': [code, value, name, ...]
}
注：各地区每天可能有多次数据记录，也可能没有记录
    原思路：查每天各地区的最新数据作为该地区的当天数据
    瑕疵：可能某天某地并没有数据
  TODO:    若当日无数据，应取昨日数据(暂使用代码方式解决)
'''
def get_time_data(level = 1, code=86):
    db = Database()
    whr = "" if level == 1 else " and region_parent={}".format(code)
    sql = '''select a.region_code, region_name, numb_confirmed, numb_suspected, numb_die, numb_ok, 
            a.data_date, DATE(tm) from patients a 
        join (SELECT region_code, max(data_date) as tm FROM patients 
            where region_level={}'''.format(level) + whr + ''' 
            group by region_code, DATE(data_date)) b 
            on a.region_code=b.region_code and a.data_date=b.tm order by data_date'''
    dts, latest, yesterday = {}, {}, None
    regions = get_regions(code, db)
    
    '''数据检查与填充'''
    def data_fill(date_):
        for p in regions:
            if p['code'] in dts[date_]: continue
            dts[date_][p['code']] = latest.get(p['code'], [p['code'], 0, p['name'], 0, 0, 0, date_])
    for (code, name, confirmed, suspected, die, ok, tm, date_) in db.select(sql):
        date_ = str(date_)
        if date_ not in dts: 
            dts[date_] = {}
            '''昨日数据检查填补，以下四行 '''
            if yesterday: data_fill(yesterday)
            yesterday = date_
        '''各地区缓存一份最新数据，用于数据填补''' 
        latest[code] = [code, confirmed, name, suspected, die, ok, str(tm)] 
        
        dts[date_][code] = latest[code]
    data_fill(yesterday)
 
    return dict((k, list(dts[k].values())) for k in dts)

'''获取下级行政区域列表'''
def get_regions(code=86, db=None):
    if code==86: return src_province
    if not db: db = Database()
    sql = "select code, name from region where parent=%s"
    return [{'name': name, 'code': code} for (code, name) in db.select(sql, (code, ))] 
    
    
if __name__ == '__main__':
#     for item in get_data_latest():
#         print(item)
#     for item in get_data_latest(2, "500000"):
#         print(item)
    print(get_time_data())
#     for item in get_time_data():
#         print(item)
#     for item in get_time_data(2, "500000"):
#         print(item)
    
        
    