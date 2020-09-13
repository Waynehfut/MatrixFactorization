# -*- coding: utf-8 -*-
"""
Created on 2018/1/25 19:56
@file: system_diversity.py
@author: Administrator
"""
from __future__ import division
import math
from confact import *
import tool.ULog as ul

def system_diversity(recommend_lists_matrix_index,table_name):
    """
    计算系统多样性，熵
    :param recommend_lists_matrix_index:[[index...],[index...]]
    :param table_name:
    :return:
    """
    sql = "select a.id,b.yiyuan from {0} a, doc_msg3 b where a.id = b.id"
    db = DatabaseConnection()
    cur = db.dbConnect()
    sql = sql.format(table_name)
    cur.execute(sql)
    docs = cur.fetchall()
    cur.close()

    length = len(recommend_lists_matrix_index)
    print "recommend_lists_matrix_index:",length
    all_list = []
    list_dict = []
    i = 1
    result = 0
    u = 0
    for recommend_list in recommend_lists_matrix_index:
        new_list = []
        u += len(recommend_list)
        for index in recommend_list:
            li = []
            li.append(index)
            #添加医院名
            li.append(docs[index][1])
            new_list.append(li)
            all_list.append(li)
        #method1
        dict_hos = static_type_sum(new_list,1)
        #dict_hos:{"hos_name":num}
        list_dict.append(dict_hos)
        #method1
    all_type = static_type_sum(all_list,1)
    # print "len(list_dict)",len(list_dict)
    hos_sum = 0
    for key,value in all_type.items():
        recom_num = 0
        for d in list_dict:
            if d.has_key(key):
                recom_num += 1
        # print "recom_num / u:",recom_num / u
        # print "math.log(recom_num / u, 2):",math.log(recom_num / u, 2)
        # print "(recom_num / u) * math.log(recom_num / u, 2):",(recom_num / u) * math.log(recom_num / u, 2)
        result += (recom_num / u) * math.log(recom_num / u, 2)
        # ul.write_log('../matrix/systme_diversity_erro_log.txt', str(result))
    return round(-result,11)

def static_type_sum(info, index):
    """
    返回info中按指定的index内容统计的分类数量，以dic形式返回,{"type":num}
    :rtype: object
    :param info: 包含医院名信息的二维数组
    :param index: 医院名在第二维中的位置
    :return: :{"type":num}
    """
    dic = {}
    t = list(info)
    # print "top:", info
    hos = 0
    while hos < len(t):
        name = t[hos][index]
        t.pop(hos)
        i = 1
        if (len(t) == 0):
            dic[name] = i
            break;
        # print "name:", name
        j = 0
        while j < len(t):
            if (t[j][index] == name):
                i += 1
                t.pop(j)
                j = j - 1
                if (len(t) == 0):
                    dic[name] = i
                    break;
            j += 1
        dic[name] = i
    # for key, values in dic.items():
    #     print "k:", key
    #     print "v:", values
    # print "----------------------hos_dict：", dic
    return dic

if __name__ == '__main__':
    print 'test'