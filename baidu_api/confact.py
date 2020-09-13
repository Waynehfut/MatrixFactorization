# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:57:03 2017

@author: Administrator
"""

import MySQLdb

class DatabaseConnection:
    def __init__(self):
        self.cur = None
    def dbConnect(self,data):
        conn = MySQLdb.connect(
        host = '127.0.0.1',
        port = 3306,
        user = 'root',
        passwd = 'root',
        db = data,
        charset='utf8')
        cur = conn.cursor()
        return cur ,conn