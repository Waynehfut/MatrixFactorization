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
import baidu_api.map_utils as bdm
import tool.math_method as mathm

hos_rank = {'9': 1, '8': 2, '7': 3, '6': 4, '5': 5, '4': 6, '3': 7, '2': 8, '1': 9}
scort = []
tt = []
length = 0
cal = 0
or_matrix = []
"""
计算权重，排序并返回
返回：[[doc_id,doc_name,hos_name,score,rank,hos_locat,dis]]
"""


def getResult1(disease, matrix, table_name, city, people_locat):
    """
    得到最终结果
    :param matrix:预测的矩阵
    :param disease: 疾病
    :return:
    """
    global hos_rank
    global scort
    global tt
    global length
    global cal
    hos_rank = {'9': 1, '8': 2, '7': 3, '6': 4, '5': 5, '4': 6, '3': 7, '2': 8, '1': 9}
    scort = []
    tt = []
    length = 0
    cal = 0

    # doc_info：[[doc_id,doc_name,hos_name,score,rank,hos_locat]]
    doc_info = filter_hos_By_sorted100(table_name, matrix, disease, city)
    # 筛选指定距离以内的医院的医生
    doc_filter = filter_by_distance(doc_info, people_locat)

    #未多样性前的排序
    f = log.write_log()
    print "预测后顺序======================================================="
    for doc in doc_filter:
        print ("%-20s%-20s" % (doc[1].encode('utf-8'), doc[2].encode('utf-8')))


    print "完成筛选指定距离以内的医院"
    last_result = get_weight(doc_filter)

    # 输出最终结果
    f = log.write_log()
    print >> f, "疾病：", disease
    print >> f, ("%-20s%-20s" % ("姓名", "医院"))
    for doc in last_result:
        print >> f, ("%-20s%-20s" % (doc[1].encode('utf-8'), doc[2].encode('utf-8')))

    return last_result


def getResult(pre_top, disease):
    """
    得到最终结果
    :param pre_top:前k个矩阵 [[doc_id,doc_name,hos_name,score]]
    :param disease: 疾病
    :return:
    """
    global length
    global tt
    global scort  # 排序的所有情况
    f = log.write_log()
    lt = len(pre_top)
    length = lt
    tt = range(lt)
    hvar(range(lt))
    s_g = []
    hos_dic = gethosdic(pre_top, 2)  # 各个医院的数量
    for s in scort:
        s_g.append(dh_weight(s, pre_top, hos_dic))
    i, grade = getmax(s_g)
    # 输出最终结果
    print >> f, "疾病：", disease
    print >> f, ("%-20s%-20s" % ("姓名", "医院"))
    for doc in scort[i]:
        print >> f, ("%-20s%-20s" % (pre_top[doc][1].encode('utf-8'), pre_top[doc][2].encode('utf-8')))
        # log.close_log()


"""
计算权重及返回
doc_filter:[[doc_id,doc_name,hos_name,score,rank,hos_locat,dis]]
返回：[[doc_id,doc_name,hos_name,score,rank,hos_locat,dis]]
"""


def get_weight(doc_filter):
    # 总评分
    c_sum = mathm.get_sum_by_index(doc_filter, 3)
    # 医院最低排名
    hos_lowest = mathm.get_maxormin_by_index(doc_filter, 4, "max")
    # 最远路程
    dis_max = mathm.get_maxormin_by_index(doc_filter, 6, "max")
    ls_sort = {}
    i = 0
    while i < len(doc_filter):
        w_c = doc_filter[i][3] / c_sum
        w_h = -doc_filter[i][4] / (hos_lowest + 1) + 1
        temp_d = doc_filter[i][6] / (dis_max + 1)
        w_d = (1 - temp_d) * math.exp(-temp_d)
        ls_sort[doc_filter[i][0]] = w_c * w_h * w_d

        # ls_sort[doc_filter[i][0]] = w_c * w_h
        i += 1
    i = 0
    ls_sorted = sort_by_value(ls_sort)
    # hos_dic = gethosdic(doc_filter, 2)
    # 排序
    doc_filter_sorted = sorted_by_sorted(doc_filter, ls_sorted)
    while i < len(doc_filter_sorted):
        hos_dic_sum = gethoss(hos_dic)
        ls_sorted[i][1] = ls_sorted[i][1] * hos_dic[doc_filter_sorted[i][2]] / hos_dic_sum
        hos_dic[doc_filter_sorted[i][2]] -= 1
        i += 1
    ls_sorted = sort_desc(ls_sorted)
    re = sorted_by_sorted(doc_filter, ls_sorted)
    return re


"""
返回按指定顺序排doc_info的顺序
"""
def sorted_by_sorted(doc_info, ls_sorte):
    docs = []
    for doc_l in ls_sorte:
        for i in doc_info:
            if i[0] == doc_l[0]:
                docs.append(i)
    return docs


"""
返回docs形式的指定距离内的医院的医生
return:[[doc_id,doc_name,hos_name,score,rank,hos_locat,dis]]
"""


def filter_by_distance(docs, people_locat):
    temp = list(docs)
    i = 0
    print "医生总数：", len(docs)
    for doc in temp:
        # print "people_locat:", people_locat
        # print "doc:", doc
        # 人的坐标，医院名
        dis = bdm.getDistance(people_locat, doc[5], 1)
        # 指定医院的距离
        if dis[0] > 20000:
            temp.pop(i)
        temp[i].append(dis[0] / 1000)
        i += 1
    return temp


"""
返回top中各个医院的数量，以dic形式返回,{"hos_name":num}
"""


def gethosdic(top, index):
    dic = {}
    t = list(top)
    print "top:", top
    hos = 0
    while hos < len(t):
        name = t[hos][index]
        t.pop(hos)
        i = 1
        if (len(t) == 0):
            dic[name] = i
            break;
        print "name:", name
        j = 0
        while j < len(t):
            print 't[j][index]', t[j][index]
            print "j:", j
            if (t[j][index] == name):
                i += 1
                print "===:", t[j][index]
                t.pop(j)
                j = j - 1
                if (len(t) == 0):
                    dic[name] = i
                    break;
            j += 1
        dic[name] = i
    for key,values in dic.items():
        print "k:", key
        print "v:", values
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
得到改组数据的权重
"""


def dh_weight1(doc_info, hos_dic):
    return tt


"""
得到sorted这一排序的医院多样性权重
"""


def dh_weight(scorted, top, hos_dic):
    sum = 0
    temp = list(top)
    hos_dic1 = dict(hos_dic)
    d_w = list()
    h_w = list()
    i = 0
    while i < len(top):
        # 医生权重
        sc = top[scorted[i]][3]
        doc = sc / getdocs(temp)
        d_w.append(doc)
        # 医院权重
        hos_name = top[scorted[i]][2]
        print 'hos_name:', hos_name
        # hos_sort:{hos_name:score}

        # hos_sorted_100 = hos_sort[hos_name]/getMax_hos(hos_sort)
        # hos = hos_dic1[hos_name]/gethoss(hos_dic1)*(hos_sorted_100+1)*math.exp(hos_sorted_100)
        # h_w.append(hos)
        # 患者与医院之间车程的权重 drivings:{hos_name:distance}
        # p_d_time = drivings[hos_ame]/getMax_Driving_w(drivings)
        # p_d_time = drivings[hos_ame]/getMax_Driving_w(drivings)*(1+p_d_time)*math.exp(p_d_time)

        hos_dic1[hos_name] -= 1
        if (len(temp) == 1):
            break
        temp.pop(0)
        i += 1
        # sum += doc*
    # 医生权重
    for i in d_w:
        # 医院权重
        for z in h_w:
            sum += i * z
    return sum


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
    s = sort_desc(pre_data(backitems))
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
以[[doc_id,doc_name,hos_name,score,rank,locat]]返回
"""


def filter_hos_By_sorted100(table_name, matrix, disease, city):
    global hos_rank
    # column用来计算是第几行
    column = 0
    # 矩阵的第几列
    row = -1
    # score {'id':'score'}
    score = {}
    # 医生信息
    doc_info = []
    # 记录不在排名内的医生信息
    doc_info_n_in_sorted = []

    # sql1 = "select b.yiyuan,b.score,b.lnglat,a.* from {0} a,doc_msg3 b where a.id = b.id and b.city like %%%%%s%%%%%"%city
    sql1 = "select b.yiyuan,b.score,b.lnglat,a.* from {0} a,doc_msg3 b where a.id = b.id and b.city = \'{1}\'"
    # sql2 = "SELECT s.id,s.hos_name from doc_msg3 a,hos_scort s,{0} t where a.yiyuan = s.hos_name  and a.city LIKE '%"+"{1}"+"%'and a.id = t.id"
    sql2 = "SELECT s.id,s.hos_name from hos_scort s where s.id < 21"
    sql3 = "select * from {0}"
    db = DatabaseConnection()
    cur = db.dbConnect('lyqystj')
    sql1 = sql1.format(table_name, city)
    cur.execute(sql1)

    docs = cur.fetchall()
    # 得到对应列的疾病信息
    sql3 = sql3.format(table_name)
    cur.execute(sql3)
    ids = cur.fetchall()
    # 得到疾病disease在矩阵中的第几列
    tempi = 0
    for name in cur.description:
        row = row + 1
        if (tempi > 3):
            if name[0] == disease:
                print "row=================================:",row
                print "name=================================:", name[0]
                break;
        tempi = tempi + 1
    # end

    for id in ids:
        score[id[0]] = matrix[column][row]
        column = column + 1

    #start测试
    sql4 = "select  d.yiyuan,s.* from doc_msg3 d,{0} s where d.id = s.id and d.city = \'{1}\'"
    sql4 = sql4.format(table_name,city)
    cur.execute(sql4)
    docss = cur.fetchall()
    for doc in docss:
        doc_temp = []
        doc_temp.append(doc[2])
        doc_temp.append(doc[0])
        doc_temp.append(doc[8])
        or_matrix.append(doc_temp)
        tt = sorted(or_matrix, lambda x, y: cmp(x[2], y[2]), reverse=True)
    print "原始顺序======================================================="
    for doc in tt:
        print ("%-20s%-20s%-100s" % (doc[0].encode('utf-8'), doc[1].encode('utf-8'),doc[2]))
    # end

    # 开始筛选,筛选条件：city，100排名内医院中的医生
    sql2 = sql2.format(table_name)
    cur.execute(sql2)
    include_hos_name = cur.fetchall()
    li = []
    for doc in docs:
        # doc_id
        li.append(doc[3])
        # doc_name
        li.append(doc[4])
        # hos_name
        li.append(doc[0])
        # score
        li.append(score[doc[3]])
        for name in include_hos_name:
            if doc[0] == name[1]:
                # rank
                li.append(name[0])
                # hos 坐标
                li.append(doc[2])
                doc_info.append(li)
                break
            else:
                # print 'doc[1]:',doc[1]
                # print "hos_rank[doc[1]]:",hos_rank[str(doc[1])]
                # rank
                li.append(hos_rank[str(doc[1])])
                # hos 坐标
                li.append(doc[2])
                doc_info_n_in_sorted.append(li)
                break
        li = []
    cur.close()
    doc_len = len(doc_info)
    for doc in doc_info_n_in_sorted:
        doc[4] = doc_len + doc[4]
        doc_info.append(doc)

    return doc_info


"""
降序排列
t:[[,]]
"""


def sort_desc(t):
    tt = sorted(t, lambda x, y: cmp(x[1], y[1]), reverse=True)
    return tt


"""
计算指定列的总和
"""


def get_max_by_index(score, i):
    sum = 0
    for doc in score:
        sum = sum + doc[i]
    return sum


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
    if 'd12345' in ("d12345", "ddd"):
        print "success"
    else:
        print "false"
    tt = range(3)
    length = 3
    hvar(range(3))
    tt = np.ndarray((2, 5))
    print tt
