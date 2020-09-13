# -*- coding: utf-8 -*-
"""
Created on 2018/1/19 15:31
@file: test.py
@author: Administrator
"""
class TT(object):
    def __init__(self):
        print 'This is a init func'
        # global num  # 使用global 可以访问到全局变量
        # num += 10
        # print 'gloal num:', num
        # TT.num += 1
        # print 'ClassName.num:', TT.num
        self.func()

    def func(self):
        print 'ClassName.num:'


if __name__ == '__main__':
    c1 = TT()
    # c1.func()
    # print 'sss'