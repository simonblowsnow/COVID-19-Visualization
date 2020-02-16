#coding:utf8

import time
import datetime
import random
from src.libs.platform_version import IS_PYTHON2
# import md5


def LONG(n):
    return long(n) if IS_PYTHON2 else int(n)

'''获取当前时间字符串'''
def TM():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

'''获取当前日期字符串'''
def DT():
    return time.strftime("%Y-%m-%d", time.localtime())

'''获取当前日期戳'''
def TMS():
    return time.time() * 1000

'''获取当前日期戳'''
def TMSL():
    return LONG(time.time() * 1000)

'''获取当前日期戳字符串'''
def TMSS():
    return str(LONG(time.time() * 1000))

'''时间字符串·纯数字'''
def TMN():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]

'''时间转字符串时间'''
def T2S(tm):
    return time.strftime("%Y-%m-%d %H:%M:%S", tm.timetuple()) if tm else ''

'''时间戳转字符串时间'''
def TS2S(stamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stamp))

'''字符串转时间'''
def S2T(s):
    return time.strptime(s, "%Y-%m-%d %H:%M:%S")

'''字符串转时间'''
def S2DT(s):
    return datetime.datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S") 

'''字符串转datetime时间'''
def S2D(s = ''):
    if s == '': return datetime.datetime.now()
    return datetime.datetime.strptime(s, "%Y-%m-%d") 
    
def DT2TMS(dt):
    if not dt: return None
    return int(time.mktime(dt.timetuple())) * 1000

def F0(n):
    n = str(int(n))
    return n if len(n) > 1 else "0" + n

def F00(n):
    n = str(int(n))
    if len(n) < 3: n = "0" + n
    return n if len(n) > 2 else "0" + n

def F000(n):
    n = str(int(n))
    for i in range(4 - len(n)): n = "0" + n
    return n

def FLOAT(n):
    if not n: return 0
    return float(n)

def CardR4(c):
    if not c: return "****"
    return c[-4:]
    
# def TJS(stamp):
#     return TS(stamp/1000)

def MU():
    return int(time.strftime("%M")) % 10

def DateOffset(n = 0, dt = ''):
    sf = '%Y%m%d' if len(dt) == 8 else '%Y-%m-%d' 
    dt = datetime.datetime.now() if dt == '' else datetime.datetime.strptime(dt, sf) 
    return str(dt + datetime.timedelta(days=n)).split(" ")[0]

'''params - seconds'''
def TimeOffset(n = 60, tm = ''):
    sf = '%Y-%m-%d %H:%M:%S' 
    tm = datetime.datetime.now() if tm == '' else datetime.datetime.strptime(tm, sf) 
    return str(tm + datetime.timedelta(seconds=n))

'''params - seconds'''
def TimeOffsetS(n = 60, tm = ''):
    sf = '%Y-%m-%d %H:%M:%S' 
    tm = datetime.datetime.now() if tm == '' else datetime.datetime.strptime(tm, sf) 
    st = (tm + datetime.timedelta(seconds=n)).strftime(sf)
    return LONG(time.mktime(time.strptime(st, sf)) * 1000)
    
def date_less(t1, t2):
    if not t1 or not t2: return False
    if type(t1) != datetime.datetime: t1 = S2DT(t1)
    if type(t2) != datetime.datetime: t2 = S2DT(t2)
    return t1 < t2 

def DiffDay(s1, s2):
    t1 = datetime.datetime.strptime(s1.split(" ")[0], "%Y-%m-%d")
    t2 = datetime.datetime.strptime(s2.split(" ")[0], "%Y-%m-%d")
    return (t2 - t1).days

'''时间差，s1比s2大的秒数'''
def DiffSecond(t1, t2 = None):
    if type(t1) == type(9999999999):
        t1 = datetime.datetime.fromtimestamp(t1 / 1000.0)
    else:
        t1 = datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S")
        
    if t2:
        t2 = datetime.datetime.strptime(t2, "%Y-%m-%d %H:%M:%S")
    else:
        t2 = datetime.datetime.now()
    
    # return LONG((t2 - t1).seconds) * (1 if t2 < t1 else -1) 
    return LONG((t1 - t2).seconds + (t1 - t2).days * 86400) 

def NextDay(dt = None):
    if not dt: dt = DT()
    dt = datetime.datetime.strptime(dt, "%Y-%m-%d") 
    return str(dt + datetime.timedelta(days=1)).split(" ")[0]

def LastDay(dt):
    dt = datetime.datetime.strptime(dt, "%Y-%m-%d") 
    return str(dt + datetime.timedelta(days=-1)).split(" ")[0]

def pre30s(s):
    dt = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S") 
    return str(dt + datetime.timedelta(seconds = 30))

def after30s(s):
    dt = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S") 
    return str(dt + datetime.timedelta(seconds = -30))

def dayTime(s):
    return str(datetime.datetime.strptime(s[:8], "%Y%m%d")) 

def time2second(s):    
    if s == '': return 0
    ps = s.split(":")
    return int(ps[0]) * 3600 + int(ps[1]) * 60

def second2time(s):    
    if s >= 86400: s -= 86400 # 43200
    return F0(s / 3600) + ':' + F0(s % 3600 / 60) + ':' + F0(s % 3600 % 60) 
        
    
'''字符串转时间戳'''
def S2TS(s):
    timeArray = time.strptime(s, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(timeArray)) * 1000

'''字符串转时间戳'''
def S2TSL(s):
    timeArray = time.strptime(s, "%Y-%m-%d %H:%M:%S")
    return LONG(time.mktime(timeArray) * 1000)


def PreNow(tm):
    tn = datetime.datetime.now()
    if type(tm) != type(tn): tm = S2DT(tm)
    return tm < tn

def LaterNow(tm):
    tn = datetime.datetime.now()
    if type(tm) != type(tn): tm = S2DT(tm)
    return tm > tn

def RandCode(length = 10):
    txt = str(random.random())[2:]
    return txt[:length] if len(txt) > length else txt + str(random.random())[2:length - len(txt) + 2]

def KV2Dict(keys, values):    
    return dict((keys[i], values[i]) for i in range(len(keys)))
    
    return 

def P2C(p):
    return float(p) * 20 + 1800

def GetMd5(st):
    m1 = md5.new()
    m1.update(st.encode('utf8'))
    return m1.hexdigest()
   
    
if __name__ == '__main__':
    pass
#     print(S2DT("2020-02-05 11:23:09.23"))


