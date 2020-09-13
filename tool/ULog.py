# -*- coding: utf-8 -*-
"""
Created on 2018/1/30 17:11
@file: Log.py
@author: Administrator
"""

def write_log(file_path,input_content):
    f = open(file_path, 'a')
    print >>f,input_content
    f.close()

class ULog():
    """

    """
    def __init__(self,file_path):
        self.log = open(file_path, 'a')
    def start_log(*args):
        pass
        # global FILE
        # # name = time.strftime('%m-%d-%H-%M',time.localtime(time.time()))
        # name = args[1]
        # if (len(args) > 0):
        #     # print type(args[0])
        #     name = args[2] + '-' + name + '.txt'
        #     # print type(name)
        # else:
        #     name = name + '.txt'
        # # FILE = open('E:\Pycharm_Workspace\lyqystj\log\%s'%name.decode('utf-8'), 'a')
        # Log.FILE = open(args[0], 'a')

    def get_log(self):
        return self.log

    def write_log(self,s):
        print >>self.log,s

    def close_log(self):
        self.log.close()

if __name__ == '__main__':
    # f = ULog('D://test.txt')
    # print >>f.get_log() ,"cheish"
    # f.close_log()
    write_log('D://test.txt',("%-10s%-10s%-10s" % ('ss','20', '30')))