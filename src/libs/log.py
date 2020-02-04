#coding:utf8
import os
import time
import logging
import sys
sys.path.append('..')


class LOG():
    DEFINED_LOG = None
        
    '''本地日志配置'''
    @staticmethod
    def init(): 
        if LOG.DEFINED_LOG: return LOG.DEFINED_LOG
        '''
        logging.basicConfig(level=logging.DEBUG,
            format = '%(message)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(asctime)s',
            datefmt = '%Y-%m-%d %H:%M:%S',
            )
        '''
        logger = logging.getLogger('simple_example')
        
        log_path = os.path.dirname(os.path.dirname(__file__)) + '/logs/log'
        log_name = log_path + time.strftime("%Y-%m-%d_%p", time.localtime()) + '.txt'
        f_handle = logging.FileHandler(log_name)
        f_handle.setLevel(logging.DEBUG)
        
        c_handle = logging.StreamHandler()
        c_handle.setLevel(logging.DEBUG)
        
        datefmt = '%Y-%m-%d %H:%M:%S'
        f_formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        c_formatter = logging.Formatter('%(message)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(asctime)s', datefmt)
        
        c_handle.setFormatter(c_formatter)
        f_handle.setFormatter(f_formatter)
        
        logger.addHandler(c_handle)
        logger.addHandler(f_handle)
    
        # logging.config.fileConfig('logging.conf')
        logger.setLevel(logging.INFO)
        
        LOG.DEFINED_LOG = logger
        
        return logger
     
    

if not LOG.DEFINED_LOG: LOG.init()
L = LOG.DEFINED_LOG


    
if __name__ == '__main__':
    L.debug('Hello, World')
    L.info('Hello, 世界')
    L.info({'Hello': '世界'})
    
    

