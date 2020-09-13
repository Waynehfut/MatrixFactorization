# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:57:03 2017

@author: Administrator
"""
from __future__ import division
from confact import *
import numpy as np
import log
import math
import sys
sys.path.append("E:\\Pycharm_Workspace\\lyqystj")
import baidu_api.map_utils as map

scort = []
tt = []
length = 0
cal = 0


def getResult(pre_top, disease,distance):
    """
    得到最终结果
    :param pre_top:前k个医生 [[doc_id,doc_name,hos_name,score]] list
    :param disease: 疾病
    :return:
    """
    global length
    global tt
    global scort  # 排序的所有情况
    global cal
    scort = []
    tt = []
    length = 0
    cal = 0
    pre_top,pz_list = filter_top(pre_top,distance)#对pre_top进行过滤(距离过远的舍去)，并返回车程信息

    f = log.write_log()
    lt = len(pre_top)
    length = lt
    tt = range(lt)
    hvar(range(lt))#更新scort，得到排序的所有情况
    s_g = []
    hos_dic = gethosdic(pre_top)  # 各个医院的数量
    for s in scort:
        s_g.append(dh_weight(s, pre_top, hos_dic,pz_list))
    i, grade = getmax(s_g)
    # 输出最终结果
    print >> f, "疾病：", disease
    print >> f, ("%-20s%-20s" % ("姓名", "医院"))
    for doc in scort[i]:
        print >> f, ("%-20s%-20s" % (pre_top[doc][1].encode('utf-8'), pre_top[doc][2].encode('utf-8')))
        # log.close_log()

"""
返回top中各个医院的数量，以dic形式返回,{"hos_name":num}
"""
def gethosdic(top):
    dic = {}
    t = list(top)
    print "top:", top
    hos = 0
    while hos < len(t):
        name = t[hos][2]
        t.pop(hos)
        i = 1
        if (len(t) == 0):
            dic[name] = i
            break;
        print "name:", name
        j = 0
        while j < len(t):
            print 't[j][2]', t[j][2]
            print "j:", j
            if (t[j][2] == name):
                i += 1
                print "===:", t[j][2]
                t.pop(j)
                j = j - 1
                if (len(t) == 0):
                    dic[name] = i
                    break;
            j += 1
        dic[name] = i
    print "----------------------hos_dict：", dic
    return dic

"""
返回最大值
"""
def getmax(gs):
    i = 0
    max = gs[0]
    for k in range(len(gs)):
        if (gs[k] > max):
            max = gs[k]
            i = k
    return i, max

"""
得到sorted这一排序的医院多样性权重
"""
def dh_weight(scorted, top, hos_dic,pz_list):
    """

    :param scorted: 其中一种排列
    :param top: 前k个医生 [[doc_id,doc_name,hos_name,score]] list
    :param hos_dic: 医院中各个医院的数量
    :param pz_list: 各个医院的车程
    :return:
    """
    sum = 0
    temp = list(top)
    temp_pz = list(pz_list)
    hos_dic1 = dict(hos_dic)
    d_w = list()
    h_w = list()
    pz_w = list()
    i = 0
    while i < len(top):
        #按scorted的顺序来计算
        # 医生权重
        sc = top[scorted[i]][3]
        doc = sc / getdocs(temp)
        d_w.append(doc)
        # 医院权重
        hos_name = top[scorted[i]][2]
        hos = hos_dic1[hos_name] / gethoss(hos_dic1)
        h_w.append(hos)
        # 患者与医院之间车程的权重
        pz_w = getDriving_w(temp_pz)
        pz_w.append(pz_w)

        hos_dic1[hos_name] -= 1
        if (len(temp) == 1):
            break
        temp.pop(0)
        temp_pz.pop(0)
        i += 1
        # sum += doc*
    # 医生权重
    for i in d_w:
        # 医院权重
        for z in h_w:
            #车程
            for pz in pz_w:
                sum += i * z*pz
    return sum

def filter_top(ori,pre_top,distance):
    """
    过滤并返回医院序列和车程序列
    :param ori: 人的坐标 （纬，经）
    :param pre_top:医院序列 [[doc_id,doc_name,hos_name,score]]
    :param distance: 过滤的距离条件
    :return:
    """
    pz_list = []
    temp_top = list(pre_top)
    for i in len(pre_top):
        dis = map.getDistance(ori, pre_top[2][i])[0]#距离
        if(dis >= distance):
            temp_top.pop(i)
        else:
            pz_list.append(map.getDistance(ori, pre_top[2][i])[1])#时间
    return temp_top, pz_list

def getDriving_w(temp_pz):
    """
    返回车程权重
    :param temp_pz:车程数列 list
    :return:车程权重
    """
    pz_max = np.array(temp_pz).max()
    temp = temp_pz[0]
    w_pz = (1-temp/pz_max)*math.exp(-temp/pz_max)
    return w_pz

"""
para:num top_k的长度，len(top_k)
得到所有的排序情况
"""
def hvar(num):
    global scort
    global tt
    global length
    global cal
    for i in range(len(num)):
        temp = list(num)
        print
        tt[length - len(num)] = num[i]
        if (len(num) > 1):
            temp.pop(i)
            hvar(temp)
        else:
            scort.append(list(tt))
            cal = cal + 1

"""
为排序做准备
供hvar()调用
"""
def getarray(num):
    t = list()
    for i in range(num):
        t.append(i)
    return t

"""
准备计算医院多样性的数据
para:top_k[[doc_id,score]]
return ：[[doc_id,doc_name,hos_name,score]]
"""
def pre_data(top_k):
    # f = log.write_log()
    pre_top = []
    sql = "select name,yiyuan from doc_msg3 where id = '{0}'"
    db = DatabaseConnection()
    cur = db.dbConnect()
    print "top_k", top_k
    for k in top_k:
        temp = []
        cur.execute(sql.format(k[0]))
        t = cur.fetchone()
        temp.append(k[0])
        temp.append(t[0])
        temp.append(t[1])
        temp.append(k[1])
        pre_top.append(temp)
    cur.close()
    # print >>f,"前k个：",pre_top
    return pre_top

"""
得到排名前k个医生及id,以[[doc_id,score]]式返回,
供pre_data()调用
"""
def getTopK(k, disease, mitrax, table_name):
    f = log.write_log()
    rank = -1
    # rows用来计算是第几行
    rows = 0
    score = {}
    sql = "select * from {0}"
    sql = sql.format(table_name)
    db = DatabaseConnection()
    cur = db.dbConnect()
    cur.execute(sql)
    ids = cur.fetchall()
    # 得到疾病disease在矩阵中的第几列
    tempi = 0
    for name in cur.description:
        if (tempi > 1):
            if name[0] == disease:
                rank = rank + 1
                break;
            rank = rank + 1
        tempi = tempi + 1
    cur.close()
    # 得到疾病disease所在矩阵中的那一列数据及相应的位置信息,以dic形式保存
    for id in ids:
        score[id[0]] = mitrax[rows][rank]
        rows = rows + 1
    # print "rank:",rank
    # print "sorted:",sort_by_value(score)[:k]
    print >> f, "顺序"
    print >> f, ("%-20s%-20s" % ("姓名", "医院"))
    items = score.items()
    backitems = [[v[0], v[1]] for v in items]
    s = sort_test(pre_data(backitems))
    for doc in s:
        print >> f, ("%-20s%-20s" % (doc[1].encode("utf-8"), doc[2].encode("utf-8")))
    return sort_by_value(score)[:k]

"""
dic中根据value降序排序，以[[,]]形式返回
"""
def sort_by_value(t):
    items = t.items()
    backitems = [[v[0], v[1]] for v in items]
    tt = sorted(backitems, lambda x, y: cmp(x[1], y[1]), reverse=True)
    return tt

"""
测试
"""
def sort_test(t):
    tt = sorted(t, lambda x, y: cmp(x[3], y[3]), reverse=True)
    return tt

"""
计算医生评分和
"""
def getdocs(docs):
    sum = 0
    for i in docs:
        sum += i[3]
    return sum

"""
计算医院总数
"""
def gethoss(hos_dic):
    sum = 0
    for i in hos_dic:
        sum += hos_dic[i]
    return sum



if __name__ == '__main__':
    # tt = range(3)
    # length = 3
    # hvar(range(3))
    # print scort
    x = [0.251,0.313,0.299,0.355,0.371,0.396,0.398]
    y = [0.3002,0.3632,0.4144,0.5032,0.6229,0.9283,1.4098]
    aver_x = []
    aver_y = []
    x2 = []
    for i in x:
        t = i- 0.340428571
        aver_x.append(t)
        x2.append(math.pow(t,2))
    for i in y:
        t = i- 0.648857143
        aver_y.append(t)
    print aver_x
    print aver_y
    print x2



