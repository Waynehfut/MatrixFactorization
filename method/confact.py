# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:57:03 2017

@author: Administrator
"""

import MySQLdb

class DatabaseConnection(object):
    def __init__(self):
        self.cur = None
    def dbConnect(self,data = 'lyq_sy_db'):
        conn = MySQLdb.connect(
        host = '127.0.0.1',
        port = 3306,
        user = 'root',
        passwd = 'root',
        db = data,
        charset='utf8')
        cur = conn.cursor()
        return cur
    def findSql(self,sql,table_name):
        cur = self.dbConnect(table_name)
        cur.execute(sql)
        return cur.fetchall()