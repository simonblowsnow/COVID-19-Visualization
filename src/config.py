#coding:utf8

class Mysql():
    HOST = "10.101.1.119"
    HOST = "localhost"
    PORT = 3306
    DB_NAME = "epidemic"
    USER_NAME = "root"
    PASSWORD = "root"
    TB_NAME = "patients"
    POOL_SIZE = 3

    HOST = "106.54.48.46"
    PASSWORD = ""
    
class Web():        
    PORT = 9400
    
    
class Config():
    mysql = Mysql
    web = Web
    
    
