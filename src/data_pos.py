#coding: utf8
'''
Created on 2020年2月4日
'''

import sys
sys.path.append('..')
sys.path.append('../..')

from src.libs.database import Database


def get_region_data(code=86):
    db = Database()
    sql = '''
        select name, geometry_type, geometry_coordinates, point_type, point_coordinates,
             data_date from patient_pos where province_code=%s
    '''
    lines = []
    for (name, tp, coords, p_tp, p_coords, tm) in db.select(sql, (code, )):
        lines.append([name, tp, coords, p_tp, p_coords, str(tm)])
    
    return lines
    
    
if __name__ == '__main__':
    get_region_data()