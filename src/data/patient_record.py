#coding: utf8
'''
Created on 2020年2月17日
'''
import os
import json
import sys
from builtins import staticmethod
sys.path.append('..')
sys.path.append('../..')
FILE_PATH = os.path.dirname(__file__) + "/patient-position"
from src.libs.database import Database
from src.data.region_recognition import REGIONS, check_city
from src.data.region import PROVINCE

class Info():
    def __init__(self, name, code, p_name, p_code, county="", source="", source_url=""):
        self.name, self.code, self.p_name, self.p_code = name, code, p_name, p_code
        self.county = county
        self.source = source
        self.source_url = source_url
        
'''数据转换·行政区域清洗'''
class Position():
    '''
    ['ah.json', 'bj.json', 'fj.json', 'gd.json', 'hb.json', 'he.json', 
        'hin.json', 'hn.json', 'js.json', 'jx.json', 'sc.json', 'sd.json', 'sx.json']
            暂不处理: GaoDeYiQin.json
    '''
    Cache = {}
    Errors = {}
    def __init__(self, item, parent):
        info = self.recognise_name(parent)
        '''item中可能含有详细城市信息'''
        self.check_region(info, item)
        '''记录未识别的城市'''
        if info.code == 0: 
            Position.Errors[info.name] = Position.Errors.get(info.name, 0) + 1
            
        self.data = {}
        '''行政区域·待关联行政区域编码'''
        self.data['region_name'] = info.name
        self.data['region_code'] = info.code
        self.data['province_name'] = info.p_name
        self.data['province_code'] = info.p_code
        self.data['county_name'] = info.county
        self.data['source'] = info.source
        self.data['source_url'] = info.source_url
        
        self.data['center_type'] = parent['center']['type']
        self.data['center_coordinates'] = parent['center']['coordinates']
        self.data['update_time'] = parent['updated_at'].replace('/', '-')
        
        self.data['name'] = item['name']
        self.data['point_type'] = item['point']['type']
        self.data['point_coordinates'] = item['point']['coordinates'] 
        self.data['geometry_type'] = item['geometry']['type']
        self.data['geometry_coordinates'] = item['geometry']['coordinates']
        if item['date'] != '': self.data['data_date'] = item['date']
        
        '''数据里有个错误，不符合时间格式，修复一下，若后期存在其他错误，则修改数据库该字段为非日期格式'''
        if len(self.data['update_time'].strip()) != 19:
            self.data['update_time'] = self.data['update_time'][:10] + ' ' \
                + self.data['update_time'][10:] 
         
         
    '''根据name, province字段初步识别行政区域'''
    def recognise_name(self, parent):
        if parent.get('province', '') in PROVINCE:
            p_name = parent['province']
            p_code = PROVINCE[p_name]  
            '''省市级同名'''
            if parent['name'] == p_name: return Info(p_name, p_code, p_name, p_code)
            code = check_city(parent['name'], p_code)
            return Info(parent['name'], code, p_name, p_code)
        else:
            '''无province字段情况'''
            if parent['name'] in PROVINCE:
                p_name = parent['name']
                p_code = PROVINCE[p_name]
                return Info(parent['name'], p_code, p_name, p_code)
            info = Position.find_name(parent['name'])
            return info
        
    '''
                部分数据列表里含有city字段，根绝列表中的数据信息填补
    '''
    def check_region(self, info, item):
        if not info: print("Error Found:", item)
        if item.get('city', None):
            info_detail = Position.find_name(item['city'])
            if not info_detail: 
                print("Error Found in city field", item)
            else:
                info.name = info_detail.name
                info.code = info_detail.code
            info.county = item.get('county', '')
            info.source = item.get('source', '')
            info.source_url = item.get('sourceurl', '')
            
        
    @staticmethod
    def find_name(name):
        if name in Position.Cache: return Position.Cache[name] 
        for p in REGIONS:
            code = check_city(name, p)
            '''
                                        以下语句速度更快些，但对于特殊别名无法识别
                if name in REGIONS[p]['name_code']: 
                    code = REGIONS[p]['name_code'][name]
            '''
            if code:
                Position.Cache[name] = info = Info(name, code, REGIONS[p]['name'], p)
                return info
        '''End For'''
        Position.Cache[name] = None
        return None
        
    
    def get_sql(self):
        keys = self.data.keys()
        params = [str(self.data[k]) for k in keys] 
        sql = "insert into patient_pos (" + ','.join(keys) + ") values (" + \
            ','.join(['%s' for k in keys]) + ")"
        return [sql, params]

'''End Class'''    
        
        
def get_files():
    path = FILE_PATH
    return (os.path.join(path, f) for f in os.listdir(path) \
            if f.endswith(".json") and f != 'GaoDeYiQin.json') 

def import_data_from_files():
    db = Database()
    idx = 0
    for filename in get_files():
        idx += 1
        print(filename)
        commands = load_file_province(filename)
        db.Transaction(commands)
        print(idx, "OK! ")
        
    print("Finished!")
    for c in Position.Errors: 
        print("未识别的城市：{}, {}处".format(c, Position.Errors[c]))
              
              
def load_file_province(filename):
    commands = []
    with open(filename, encoding='utf8') as fp:
        txt = ''.join(fp.readlines())
        
        '''源文件可能有误（jx.json），会导致出错，需要处理一下'''
        try:
            data = json.loads(txt, encoding='utf8')
        except:
            txt = txt.replace("\n", "").replace(' ', '').replace(",,", ',')
            data = json.loads(txt, encoding='utf8')
        '''End Try'''
        
        for item in data:
            for p in item['pois']:
                pos = Position(p, item)
                commands.append(pos.get_sql())
    return commands

    
    
if __name__ == '__main__':
#     print(list(get_files()))
#     load_file_province("patient-position/ah.json")
    import_data_from_files()
    
    
    
    pass