#coding:utf8
import sys
sys.path.append('../')

import json
import redis
from src.libs.utils import TMSL
from src.config import Redis as C
from src.libs.log import L
import inspect


class MyRedis(object):
    '''
    classdocs
                兼容redis无法连接情形
                支持从内存记录切换到redis
    '''
    redis_status = True
    index = 0
    ZMaxCount = 10000
    data = {}
    dataHash = {}
    channel_default = "ChannelMain"
    rs, pool = None, None
    '''本地程序内存模式'''
    local_model = False
    
    if not local_model: 
        pool = redis.ConnectionPool(host=C.HOST, password=C.PASSWORD, port=C.PORT, db=C.DB_NAME)
        rs = redis.Redis(connection_pool=pool)
    
    def __init__(self):
        pass
        
    
    @staticmethod
    def sendMessage(msg, channel = None):
        if not channel: channel = MyRedis.channel_default
        MyRedis.rs.publish(channel, msg)
    
    @staticmethod
    def subscribe(channel = None, setDefault = False):
        if not channel: channel = MyRedis.channel_default
        pub = MyRedis.rs.pubsub() # 开始订阅
        pub.subscribe(channel) # 订阅频道
        pub.parse_response() # 准备接收
        if setDefault: MyRedis.pubsub = pub
        return  pub
    
    @staticmethod
    def getMessage(pub = None, toDict = True):
        if not pub: pub = MyRedis.pubsub 
        msg = pub.parse_response()
        value = msg[2]
        return eval(value) if toDict and value!=None else value
        
        
    @staticmethod
    def SwitchToLocal():
        MyRedis.redis_status = False
        raise RuntimeError('Redis Error')
        L.error("redisEx find error in Function :" + inspect.stack()[1][3])
        
    @staticmethod
    def checkConn():
        if MyRedis.local_model: return
        MyRedis.index += 1
        if not MyRedis.redis_status:
            if (MyRedis.index % 30) != 0: return 
            try:
                MyRedis.rs.get('*')
                for key in MyRedis.data: MyRedis.rs.set(key, MyRedis.data[key])
                for key in MyRedis.dataHash: 
                    for dKey in MyRedis.dataHash[key]: 
                        MyRedis.rs.hset(key, dKey, MyRedis.dataHash[key][dKey])
                MyRedis.redis_status = True
            except:
                L.info('reconnect failed')
        '''End if'''
    '''End checkConn'''
        
    @staticmethod
    def set(key, value, ex=None):
        MyRedis.checkConn()
        if MyRedis.redis_status:
            try:
                return MyRedis.rs.set(key, value, ex)
            except:
                MyRedis.SwitchToLocal()
        MyRedis.data[key] = value
        return False
    '''End set'''
       
    @staticmethod
    def get(key, toDict=True):
        MyRedis.checkConn()
        if MyRedis.redis_status:
            try: 
                value = MyRedis.rs.get(key)
                return eval(value) if toDict and value!=None else value
            except:
                MyRedis.SwitchToLocal()
        return MyRedis.data[key] if key in MyRedis.data else None
    
    '''End get'''
    @staticmethod
    def delete(key):
        MyRedis.checkConn()
        if MyRedis.redis_status:
            try: 
                return MyRedis.rs.delete(key)
            except:
                MyRedis.SwitchToLocal()
        if key in MyRedis.dataHash: MyRedis.dataHash.pop(key)
    '''End get'''
    
    @staticmethod
    def hset(key, dKey, dValue):
        MyRedis.checkConn()
        if MyRedis.redis_status:
            try:
                if type(dValue) == type({}) or type(dValue) == type([]):
                    dValue = json.dumps(dValue, ensure_ascii=False)
                return MyRedis.rs.hset(key, dKey, dValue)
            except:
                MyRedis.SwitchToLocal()
        if key not in MyRedis.dataHash: MyRedis.dataHash[key] = {}
        MyRedis.dataHash[key][dKey] = dValue
        return False
    '''End hset'''
    
    @staticmethod
    def hget(key, dKey, toDict = True):
        MyRedis.checkConn()
        if MyRedis.redis_status:
            try:
                value = MyRedis.rs.hget(key, dKey)
                return eval(value) if toDict and value!=None else value
            except Exception as e:
                L.error(str(e))
                MyRedis.SwitchToLocal()
        if key not in MyRedis.dataHash: return None
        return MyRedis.dataHash[key][dKey] if dKey in MyRedis.dataHash[key] else None
    '''End hset'''
    
    @staticmethod
    def hdel(key, dKey):
        if MyRedis.redis_status:
            try:
                return MyRedis.rs.hdel(key, dKey)
            except:
                MyRedis.SwitchToLocal()
        if key not in MyRedis.dataHash: return False
        if dKey in MyRedis.dataHash[key]: MyRedis.dataHash[key].pop(dKey)
    ''''''
       
    @staticmethod
    def hexists(key, dKey):
        if MyRedis.redis_status:
            try:
                return MyRedis.rs.hexists(key, dKey)
            except:
                MyRedis.redis_status = False
        if key not in MyRedis.dataHash: return False
        return dKey in MyRedis.dataHash[key]
    ''''''
    
    @staticmethod
    def hlen(key):
        if MyRedis.redis_status:
            try:
                return MyRedis.rs.hlen(key)
            except:
                MyRedis.redis_status = False
        if key not in MyRedis.dataHash: return False
        return len(MyRedis.dataHash[key])
    ''''''
   
    @staticmethod
    def hkeys(key):
        if MyRedis.redis_status:
            try:
                return MyRedis.rs.hkeys(key)
            except:
                MyRedis.redis_status = False
        if key not in MyRedis.dataHash: MyRedis.dataHash[key] = {}
        return MyRedis.dataHash[key].keys()
    ''''''
    @staticmethod
    def hvals(key, toDict = True):
        if MyRedis.redis_status:
            try:
                return [d if d==None and toDict else eval(d) for d in MyRedis.rs.hvals(key)]
            except:
                MyRedis.redis_status = False
                
        if key not in MyRedis.dataHash: MyRedis.dataHash[key] = {}
        return MyRedis.dataHash[key].values()
    ''''''
    @staticmethod
    def hgetall(key, toDict = True):
        if MyRedis.redis_status:
            try:
                item = MyRedis.rs.hgetall(key)
                if not toDict: return dict((k, item[k]) for k in item)
                return dict([(k, item[k] if item[k]==None else eval(item[k])) for k in item])
            except:
                MyRedis.redis_status = False
        if key not in MyRedis.dataHash: MyRedis.dataHash[key] = {}
        return dict(MyRedis.dataHash[key].items())
    ''''''
   
    @staticmethod
    def zadd(key, value, score):
        # 暂时不支持本地模式
        MyRedis.checkConn()
        if MyRedis.redis_status:
            try:
                if MyRedis.rs.zcard(key) < MyRedis.ZMaxCount: 
                    return MyRedis.rs.zadd(key, value, score)
                else:
                    return L.error('Collection size is too big over ZMaxCount when zadd')
            except:
                MyRedis.SwitchToLocal()
        if key not in MyRedis.dataHash: MyRedis.dataHash[key] = {}
        MyRedis.dataHash[key][score] = value
        return False
    
    @staticmethod
    def zremRangeByScore(key, _min = 0, _max = None):
        if _max == None: _max = TMSL()
        if MyRedis.redis_status:
            return MyRedis.rs.zremrangebyscore(key, _min, _max)
        return []
        
    @staticmethod
    def zrangeByScore(key, _min = 0, _max = None):
        if _max == None: _max = TMSL()
        if MyRedis.redis_status:
            return MyRedis.rs.zrangebyscore(key, _min, _max)
        return None
    
    '''取完就删'''
    @staticmethod
    def zRangeRemByScore(key, _min = 0, _max = None):
        if _max == None: _max = TMSL()
        if MyRedis.redis_status:
            try:
                lines = MyRedis.rs.zrangebyscore(key, _min, _max)
                MyRedis.rs.zremrangebyscore(key, _min, _max)
                return [eval(line) for line in lines]
            except:
                L.error('zrangeRemByScore error', key)
        return []
    
    @staticmethod
    def zcard(key):
        MyRedis.checkConn()
        if MyRedis.redis_status:
            return MyRedis.rs.zcard(key)
        return None 
        
    @staticmethod
    def addDict(key, dKey, dValue):
        value = MyRedis.get(key)
        if None==value: value = '{}'
        if type(value) == type(''): value = eval(value)
        value[dKey] = dValue
        MyRedis.set(key, value) 
    
    @staticmethod
    def addValue(key, value = 1):
        origin = MyRedis.get(key)
        if None==origin: origin = 0
        MyRedis.set(key, origin + value, 86400) 
        return origin + value
'''End Class'''

           
if __name__ == '__main__':
    rs = MyRedis()
    rs.set("Test", '123')
    print(rs.get("Test"))
    
