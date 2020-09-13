# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 17:17:22 2017

@author: Administrator
"""
from confact import *
def check(table_name):
    """
    返回不在deep中的疾病字段列表
    :param table_name:
    :return:[disease,...,disease]
    """
    lis = []
    i = 0
    j = 0
    sql = 'select name from deep'
    sql1 = 'select * from %s'%table_name
    d1 = DatabaseConnection()
    cur1 = d1.dbConnect()
    cur1.execute(sql)
    deeps = cur1.fetchall()

    cur2 = d1.dbConnect()
    cur2.execute(sql1)
    #    fens = cur2.fetchall()
    for field in cur2.description:
        i = i+1
        j = 0
        for deep in deeps:
            #            print type(deep[0])
            if (field[0] == deep[0].encode('utf-8') or i<=2):
#                print "deep:", deep[0].encode('utf-8')
                 j = 1
        if j==0:
            lis.append(field[0])

#    print '不存在的', lis
    return lis
"""
for l in lis:
        print l
"""

def delete_disease(lis,table_name):
    sql = 'select name from deep'
    sql1 = 'alter table {0} drop column {1}'
    d1 = DatabaseConnection()
    cur1 = d1.dbConnect()
    for dis in lis:
        print
        sql2 = sql1.format(table_name,dis)
        print sql2
        print dis
        cur1.execute(sql2)
    cur1.close()
    print '删除完成'

"""
使tc矩阵与lc矩阵相同
"""
def changemitra(ch_table,dc_table):
    sql = 'select * from {0}'
    sql1 = 'alter table {0} drop column {1}'
    d1 = DatabaseConnection()
    cur = d1.dbConnect()
    cur.execute(sql.format(ch_table))
    ch_l = list()
    for ch in cur.description:
        ch_l.append(ch[0])
    cur.execute(sql.format(dc_table))
    for i in ch_l:
        for dc in cur.description:
            if(i!=dc[0]):
                print i
                cur.execute(sql1.format(ch_table, i))
    cur.close()
    print '改变完成'

"""
"""
if __name__ == "__main__":
    #除去掉不在deep中的疾病字段
    # delete_disease(check('tp_神经内科'),'tp_神经内科')
    delete_disease(check('lc_神经内科'), 'lc_神经内科')