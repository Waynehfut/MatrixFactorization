# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:57:03 2017

@author: Administrator
"""
from __future__ import division
from confact import *
import numpy as np
yiyuan = []
zhiji = []
jxzc = []
leiji = []
"""
得到前k个最相似医生的Sim_u相似性集合，二维数组形式，1：位置，2：sim
para:
i:第i个医生
k:前k个Sim_u
"""
def getTopSim_u(table_name,i,k):
    global yiyuan
    global zhiji
    global jxzc
    global leiji
    yiyuan = []
    zhiji = []
    jxzc = []
    leiji = []
    return sort_by_value(getAllSim(table_name,i))[:k]

"""
得到所有的Sim集合，二维数组形式
"""
def getAllSim(table_name,i):
    global yiyuan
    global zhiji
    global jxzc
    global leiji
    if(len(yiyuan)==0):
        yiyuan, zhiji, jxzc, leiji = getDocInfo(table_name)
    #分母下的两个式子
    denominator1 = 0.0
    denominator2 = 0.0
    bq_aver = 0
    all_sim = []
    i_aver = getAver(yiyuan[i],zhiji[i],jxzc[i],leiji[i])
    for j in range(len(yiyuan)):
        if j != i:
            temp = []
            yy_i = yiyuan[i] - i_aver
            zj_i = zhiji[i] - i_aver
            jz_i = jxzc[i] - i_aver
            lj_i = leiji[i] - i_aver
            bq_aver = getAver(yiyuan[j], zhiji[j], jxzc[j], leiji[j])
            yy_q = yiyuan[j] - bq_aver
            zj_q = zhiji[j] - bq_aver
            jz_q = jxzc[j] - bq_aver
            lj_q = leiji[j] - bq_aver
            # 分子部分值
            molecule = yy_i * yy_q + zj_i * zj_q + jz_i * jz_q + lj_i * lj_i
            denominator1 = np.sqrt(np.square(yy_i) + np.square(zj_i) + np.square(jz_i) + np.square(lj_i))
            denominator2 = np.sqrt(np.square(yy_q) + np.square(zj_q) + np.square(jz_q) + np.square(lj_q))
            temp.append(j)
            temp.append(molecule / (denominator1 * denominator2))
            if (temp[1] > 0):
                all_sim.append(temp)
    return all_sim
"""
求平均值
"""
def getAver(y,z,j,l):
    return (y+z+j+l)/4.0
"""
医生基本信息预处理
"""
def getDocInfo(table_name):
    global yiyuan
    global zhiji
    global jxzc
    global leiji

    i = 0
    sorted = []
    sql1 = 'select a.id,a.score,a.zhiji,a.jxzc,a.leiji from doc_msg3 a ,{0} b where a.id = b.id'
    sql1 = sql1.format(table_name)
    sql2 = 'select id from {0}'
    sql2 = sql2.format(table_name)
    db = DatabaseConnection()
    cur = db.dbConnect()
    cur.execute(sql2)
    #待分解矩阵中医生顺序
    doc_sort = cur.fetchall()
    cur.execute(sql1)
    doc_infor = cur.fetchall()
    #将医生基本信息按顺序排好
    for num in range(len(doc_sort)):
        for doc in doc_infor:
            if doc[0] == doc_sort[num][0]:
                sorted.append(doc)
    #将医生的各项基本信息放到各个数组中
    for d in sorted:
        yiyuan.append(d[1])
        zhiji.append(d[2])
        jxzc.append(d[3])
        leiji.append(d[4])
    #对医生的各项基本信息进行初始化
    # while i< len(yiyuan):
    yiyuan = initialize_doc(np.array(yiyuan))
    zhiji = initialize_doc(np.array(zhiji))
    jxzc = initialize_doc(np.array(jxzc))
    leiji = initialize_doc(np.array(leiji))
    return yiyuan,zhiji,jxzc,leiji


"""
基本信息进行归一化处理
"""
def initialize_doc(lis):
    new_lis = list()
    mean,var = getMV(lis)
    if(var != 0):
        for i in lis:
            new_lis.append((i - mean) / var)
        return new_lis
    #lis中所有值一样的情况下
    else:
        for i in lis:
            i = 1
        return lis
"""
求均值与标准差
"""
def getMV(nlist):
    mean = np.mean(nlist)
    # var = np.var(nlist)
    sd = np.sqrt(np.var(nlist))
    return mean,sd
"""
t中根据距离降序排序，以二维数组形式返回
"""
def sort_by_value(t):
    # tt = sorted(t,lambda x,y:cmp(x[1],y[1]),)
    tt = sorted(t, lambda x, y: cmp(y[1], x[1]))
    return tt

if __name__ == '__main__':
    # print getTopSim_u("tp_神经外科",0,20)
    # print "finshed"
    print sort_by_value(getAllSim("tp_神经外科", 3))[:10]
