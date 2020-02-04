#coding:utf8

import sys
sys.path.append("..")


from src.config import Mysql as cfg
import mysql.connector
from mysql.connector import pooling, Error
from DBUtils.PooledDB import PooledDB
from src.libs.log import L

def GetSingleValue(sql):
    db = Database()
    for d in db.select(sql):
        return d[0]
    return None

def GetSingleLine(sql, params, db = None):
    if db == None: db = Database()
    return db.selectEx(sql, params)
    
'''connect database without use pool'''
        
class Database(object):
    ''' for query data in only one code '''
    initFlag = False
    objCount = 0
    dbconfig = { "host":cfg.HOST, "port":cfg.PORT, "user":cfg.USER_NAME, "password":cfg.PASSWORD, "database":cfg.DB_NAME }
    pool = None
    
    def __init__(self):
        self.objIndex = Database.objCount
        Database.objCount += 1
        self.lsConn = []
        self.lsCurs = []
    
    
    def getConnection(self):
        '''检查是否初始化'''
        if not Database.pool:
            Database.pool = PooledDB(mysql.connector, cfg.POOL_SIZE, host=cfg.HOST, port=cfg.PORT, 
                    user=cfg.USER_NAME, passwd=cfg.PASSWORD, db=cfg.DB_NAME, use_unicode=True, charset='utf8')
        cnx = None
        try:
            cnx = Database.pool.connection()
            self.lsConn.append(cnx)
        except:
            L.error('pool error:' + str(len(self.lsConn)))
        return cnx
    
    def selectLine(self, sql, params):
        res = self.selectEx(sql, params)
        if not res or len(res) == 0: return None
        return res[0]
    
    def selectEx(self, sql, params, cursor=None):
        if cursor==None:
            cnx = self.getConnection()
            cursor = cnx.cursor()
        cursor.execute(sql, params)
        dt = cursor.fetchall()
        cursor.close()
        cnx.close()
        
        return dt
    
    def select(self, sql, params = (), cursor = None):
        if cursor==None:
            cnx = self.getConnection()
            cursor = cnx.cursor()
            self.lsCurs.append(cursor)
        
        cursor.execute(sql, params)
        
        '''TODO: Python3此处cursor不可迭代，需要fetchall？'''
        return cursor.fetchall()
    
    def selectPage(self, sql, params, page, size, cursor = None):
        sqlEx = "select count(*) from (" + sql + ") sc"
        if cursor==None:
            cnx = self.getConnection()
            cursor = cnx.cursor()
            self.lsCurs.append(cursor)
        cursor.execute(sqlEx, params)
        res = cursor.fetchall()
        
        sql += " limit %s, %s"
        args = list(params) + [int(page) * int(size), int(size)]
        cursor.execute(sql, tuple(args))
        
        return res[0][0], cursor
    
    def execute(self, sql, params):
        cnx = self.getConnection()
        cursor = cnx.cursor()
        
        emp_no = 0
        try:
            cursor.execute(sql, params)
            emp_no = cursor.lastrowid
            cnx.commit()
        except Exception as e:
            emp_no = -1
            L.error("Run Error: " + sql)
            L.error(e)
        '''End Try'''    
        cursor.close()
        cnx.close()
        return emp_no
    
    def run(self, sql):
        cnx = self.getConnection()
        cursor = cnx.cursor()
        
        emp_no = 0
        try:
            cursor.execute(sql)
            emp_no = cursor.lastrowid
            cnx.commit()
        except Exception as e:
            emp_no = -1
            L.error("Run Error: " + sql)
            L.error(e)
        '''End Try'''  
        cursor.close()
        cnx.close()
        return emp_no
    
    def Query(self, sql, params, cnx = None):
        if not cnx: cnx = self.getConnection()
        cursor = cnx.cursor()
        self.lsCurs.append(cursor)
        
        cursor.execute(sql, params)
        
        return cnx, cursor
    
    def QueryLine(self, cursor, sql, params):    
        cursor.execute(sql, params)
        res = cursor.fetchall()
        if not res or len(res) == 0: return None
        return res[0]
    
    def Transaction(self, lines, cnx = None, cursor = None):
        if cnx==None: cnx = self.getConnection()
        if cursor==None: 
            cursor = cnx.cursor()
            self.lsCurs.append(cursor)
        flag, lsRst = True, []
        '''开启事务'''
        cursor.execute("BEGIN;")
        try:
            for line in lines:
                cursor.execute(line[0], line[1])
                lsRst.append(cursor.lastrowid )
            cnx.commit()
        except Error as e:
            cnx.rollback()
            flag = False                
            L.error('Error: ' + str(e))
        '''End For'''
        
        cursor.close()
        cnx.close()
        return flag, lsRst 
     
    def getKeys(self, tbName):
        print(self.select("SHOW FULL COLUMNS FROM {}".format(tbName)))
        return [info[0] for info in self.select("SHOW FULL COLUMNS FROM {}".format(tbName), ())]
    


if __name__ == '__main__':
    db = Database()
    # for item in db.select("select * from user"): print(item)
    print(db.getKeys('user'))
    
    pass
    
