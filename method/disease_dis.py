# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:57:03 2017

@author: Administrator
"""
from __future__ import division
from confact import *
import log

def getTopSim_v(lamda,disease,k,table_name):
    """
    返回前k个疾病最相似的Sim_v集合,二维数组形式
    :param lamda: 参数
    :param disease: 疾病序列号 int
    :param k: top_k个最相似的
    :param table_name:
    :return: Sim_v[[,]] 1:位置，2：距离
    """
    all_distance = getAllDistance(disease,table_name)
    # print 'simv_finshed'
    return sort_by_value(getALLSim(lamda,all_distance))[:k]

"""
def getAllDistance(disease,table_name):
    all_distance = []
    d_list = getAllDis(table_name)
    for d in d_list:
        all_distance.append(getDistance(disease,d[1]))
    return all_distance
"""
"""
d1为病人所得的疾病
获得疾病d1与d2的距离
"""
def getDistance(d1,d2):
    branch1 = getTreeList(d1)
    branch2 = getTreeList(d2)
    layer1 = int(branch1[0])
    layer2 = int(branch2[0])
    if(layer1>=layer2):
        distance = calculateDis(branch1,branch2)
    else:
        distance = calculateDis(branch2,branch1)
    return distance

"""
得到disease疾病所在的枝和层数
"""   
def getTreeList(disease):
    layer = getLayer(disease)
    # print 'layer',layer
    # print 'disease',disease
    sql = "select * from tree a where a.{0}='{1}'"
    sql = sql.format(layer,disease)
    db = DatabaseConnection()
    cur = db.dbConnect()
    cur.execute(sql)
    dis_tree = cur.fetchone()
    cur.close()
    return layer,dis_tree

"""
获得疾病disease的在树中的位置层数
"""
def getLayer(disease):
    sql1 = "select layer from deep where name ='{0}'"
    sql1 = sql1.format(disease)
    db = DatabaseConnection()
    cur = db.dbConnect()
    cur.execute(sql1)
    layer = cur.fetchone()
    cur.close()
    # print 'layer:',layer[0]
    return layer[0]

"""
根据枝的对比计算疾病距离
"""
def calculateDis(branch1,branch2):
    i = int(branch1[0])
    j = int(branch2[0])
    stop = 0
    distance = 0
    while stop ==0:
        if(i==j):
            i = i-1
            j = j-1
            distance = distance + 2
            # print '+1'
        else:
            i = i-1
            distance = distance + 1
#        print 'branch1',branch1[1][i-1]
#        print 'branch2',branch2[1][j-1]
        if branch1[1][i-1].encode('utf-8') == branch2[1][j-1].encode('utf-8') :
            # print 'stop'
            stop = 1
    return distance

"""
返回矩阵中所有的疾病字段,以二维数组形式返回,第一个为位置信息，第二个为疾病名
"""
def getAllDis(table_name):
    all_dis = []
    temp = []
    i = 0
    sql = "select * from %s"%table_name
    db = DatabaseConnection()
    cur = db.dbConnect()
    cur.execute(sql)
    for name in cur.description:
        i = i+1
        if i>2:
            temp.append(name[0])
    for dis in enumerate(temp):
        all_dis.append(dis)
    cur.close()
    return all_dis
"""
得到所有疾病与目标疾病disease的距离,disease值为该疾病在矩阵中的位置,
以[[,]]返回，1：位置；2：距离
值都为int
"""
def getAllDistance(disease,table_name):
    f = log.write_log()
    all_distance = []
    #diseases:[[,]]第一个为位置信息，第二个为疾病名
    diseases = getAllDis(table_name)
    for d in diseases:
        #不计算与疾病自身的比较
        if d[1] != diseases[disease][1]:
            temp = []
            temp.append(d[0])
            temp.append(getDistance(diseases[disease][1],d[1]))
            all_distance.append(temp)
        # else:
        #     temp = []
        #     temp.append(d[0])
        #     temp.append(0)
        #     all_distance.append(temp)
    return all_distance
    # print >> f,'距离：',all_distance
"""
lamda为可调参数
得到所有疾病与目标疾病(disease)的距离的Sim
以[[,]]形式返回，1：位置；2：Sim
值都为int
"""
def getALLSim(lamda,all_distance):
    lis = []
    for i in all_distance:
        temp = []
        temp.append(i[0])
        temp.append(lamda/(lamda+i[1]))
        if (temp[1]>0):
            lis.append(temp)
    return lis

"""
t中根据距离降序序排序，以[[,]]形式返回
"""
def sort_by_value(t):
    # tt = sorted(t,lambda x,y:cmp(x[1],y[1]))
    tt = sorted(t,lambda x,y:cmp(y[1],x[1]))
    return tt

if __name__=="__main__":
   print 'f'
   all_distance = getAllDistance(4,'tp_神经外科')
   t = sort_by_value(getALLSim(0.05, all_distance))[:8]
   print  t
   # fileSim = open("C:\Users\Administrator\Desktop\s.txt",'a+')
   # fileSim.write('\n')
   # fileSim.write(str(all_distance))
   # fileSim.write('\n')
   # fileSim.write(str(t))
   # fileSim.write('\n')
   # fileSim.close()
   # print all_distance
   # print t
   # print sort_by_value(getALLSim(0.1,all_distance))
   # log.start_log()
   # f = log.write_log()
   # print >>f,"cc:",cc
"""
     k = getAllDis('lc_风湿科')
     for t in k:
         print 'index:',t[0]
         print 'name:',type(t[1])
"""
