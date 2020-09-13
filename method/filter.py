# -*- coding: utf-8 -*-
"""
Created on 2017/8/28 9:56
@file: filter.py
@author: Administrator
"""
import doc_matrix as docm
from confact import *


def getdoc_mat(table_name,city):
    """
    得到在目标城市的医院的医生矩阵
    :param table_name:投票医生表
    :param city: 目标城市
    :return:筛选过的医生矩阵 type：list
    """
    mat = docm.getMatrix(table_name)
    filter_doc = filter(table_name,city)
    temp = []
    for i in filter_doc:
        temp.append(mat[i])
    return temp

def filter(table_name,city):
    """
    得到在原始医生矩阵中符合条件的医生的索引号
    :param table_name: 投票医生表
    :param city: 目标城市
    :return:原始医生矩阵中符合条件的医生的索引号 type：list
    """
    target_doctor = []
    sql1 = 'select a.id from {0} a,doc_msg b where a.id = b.id and b.city = {1}'
    sql2 = 'select * from {0}'
    sql1 = sql1.format(table_name,city)
    sql2 = sql2.format(table_name)
    db = DatabaseConnection()
    cur = db.dbConnect()
    cur.execute(sql1)
    id_city = cur.fetchall()
    cur.execute(sql2)
    doctor = cur.fetchall()
    for c in id_city:
        i = 0
        for d in doctor:
            if(c[0] == d[0]):
                target_doctor.append(i)
            i += 1
    cur.close()
    return target_doctor