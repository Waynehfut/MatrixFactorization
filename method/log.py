# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:57:03 2017

@author: Administrator
import time
"""
import time
FILE = None
def start_log(*args):
    global FILE
    # name = time.strftime('%m-%d-%H-%M',time.localtime(time.time()))
    name = args[1]
    if(len(args)>0):
        name = args[0]+'-'+name+'.txt'
    else:
        name = name+'.txt'
    # FILE = open('E:\Pycharm_Workspace\lyqystj\log\%s'%name.decode('utf-8'), 'a')
    FILE = open(args[1], 'a')
def write_log():
    global FILE
    return FILE
def close_log():
    global FILE
    FILE.close()

class uLog(object):
    def __init__(self,file_path):
        self.file_path = file_path
        self.file = open(file_path, 'a')

    def get_log(self):
        self.file = open(self.file_path, 'a')
        return self.file

    def write_log(self,input_content):
        print >>self.file,input_content

    def close_log(self):
        self.file.close()




