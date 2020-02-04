#coding:utf8
import sys
import platform

# 2 or 3
PYTHON_VERSION = int(platform.python_version().split('.')[0])
# 27 or 35
PYTHON_VERSION_INFO = int(''.join(platform.python_version().split('.')[0:2]))

IS_PYTHON2 = PYTHON_VERSION == 2
IS_PYTHON3 = PYTHON_VERSION == 3 

def version():
    return platform.python_version()

if IS_PYTHON2:
    reload(sys)
    sys.setdefaultencoding('utf8') 

    
def long_(n):
    return long(n) if IS_PYTHON2 else int(n)  
    
if __name__ == '__main__':
    print(IS_PYTHON2)
    print(IS_PYTHON3)
    print(version())
    print(PYTHON_VERSION)
    print(PYTHON_VERSION_INFO)
    print(long_('123'))
