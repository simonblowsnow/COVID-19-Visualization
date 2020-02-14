#coding:utf8

import sys
sys.path.append('..')

from src.libs.database import Database
from src.data.region import REGION_SHORT, SPECIAL_NAME, PROVINCE_WITH_COUNTY, PROVINCE_LEVEL_CITY

'''
建立行政区域双向对照表，含别名，见source.REGION_SHORT
Return:
    {150000: {
        'name': '内蒙古自治区', 
        'name_code': {'巴彦淖尔市': 150800}, 
        'children': { 150800: {'name': '巴彦淖尔市', 'names': set()} }
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
        if level == 2:
            regions[parent]['children'][code] = {'name': name}
            '''别名缓存'''
            if name in REGION_SHORT: 
                regions[parent]['children'][code]['names'] = set(REGION_SHORT[name])
        '''End If 1'''
    '''End For'''
    '''
                    建立查找索引·将各地区名称-代码列表存入name_code，含别名
                     特点：常规市含“市”；自治州不含“州”
    '''
    for p in regions: 
        regions[p]['name_code'] = {}
        for c, v in regions[p]['children'].items():
            regions[p]['name_code'][v['name']] = c
            for n in v.get('names', []): regions[p]['name_code'][n] = c 
            
    return regions

'''
二级区域（市、自治州、盟、地区、省属县、自治县、直辖市属区）识别，含常用别名
依赖     region.REGION_SHORT
目前数据识别率100%
Return: 行政区域代码
'''
def check_city(name, parent):
    names = REGIONS[parent]['name_code']
    if name in names: return names[name]
    if (name + "市") in names and name not in SPECIAL_NAME: return names[name + "市"] 
    if (name + "地区") in names: return names[name + "地区"]
    if name[-1] == '州' and name[:-1] in names: return names[name[:-1]]
    if len(name) > 2 and name[-3:] == '自治州' and name[:-3] in names: 
        return names[name[:-3]]
    if parent in PROVINCE_WITH_COUNTY and (name + "县") in names:
        return names[name + "县"]
    if parent in PROVINCE_LEVEL_CITY and (name + "区") in names:
        return names[name + "区"]
    return 0


REGIONS = get_region_citys()

