# -*- coding: utf-8 -*-
"""
Created on 2018/2/4 20:03
@file: vns.py
@author: Administrator
"""
from __future__ import division
from confact import *
import random
import tool.ULog as ul
def vns(doc_info, doc_id_dict, sim_matrix, top_k):
    # 医院总数
    hos_type_sum = static_type_sum(doc_info, 2)
    i = 2
    hos_sum = len(hos_type_sum)
    doc_list = range(len(doc_info))
    # 记录的是doc_info 对应的index
    recommend_list = random.sample(doc_list, top_k)
    n = 0
    while n < top_k:
        random_i = random.randint(0,top_k-1)
        doc_index = recommend_list[random_i]
        doc = doc_id_dict[doc_info[doc_index][0]]
        # # 将recommend_list中的index转换成与matrix对应
        # chosen_doc = sort_by_matrix(recommend_list, doc_id_dict, doc_info)
        # 按顺序返回最不相似的list集合，第一个是最不相似的,index与doc对应
        unsim_list = get_unsim_set(doc,recommend_list,sim_matrix,doc_info,doc_id_dict,top_k)
        for j in unsim_list:
            prefore_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
            recommend_list[random_i] = j
            present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
            #置换条件
            if prefore_diversity > present_diversity:
                recommend_list[random_i] = doc_index
            else:
                break
        n += 1
    recommend_list_as_index = sort_by_matrix(recommend_list, doc_id_dict, doc_info)
    return recommend_list, recommend_list_as_index

def single_diversity(doc_recommend,sim_matrix,doc_id_dict,doc_info,hos_sum):
    """
    计算单个个体推荐的多样性
    :type sim_matrix: object
    :param doc_recommend:
    :param sim_matrix: 相似度矩阵
    :param doc_info: 医生信息
    :return:
    """
    temp = sort_by_matrix(doc_recommend,doc_id_dict,doc_info)
    n,m = sim_matrix.shape
    # print "sim_matrix:",len(sim_matrix)
    zs = z_score(temp, sim_matrix)
    cr = cover_rate(doc_recommend,doc_info,hos_sum)
    # print "z_score:",zs
    # print "cover_rate:",cr
    diversity = pow(zs*cr,0.5)
    return diversity

def get_unsim_set(doc,chosen_doc,sim_matrix,doc_info,doc_id_dict,top_k):
    """
    # 按顺序返回最不相似的list集合，第一个是最不相似的,index与doc对应
    :param doc:index,index与matrix对应
    :param chosen_doc:[index...]index与doc对应
    :param sim_matrix:
    :param doc_info:
    :param sim_matrix:
    :param doc_id_dict:
    :return:[index...]
    """
    temp_um_sim = sim_matrix[doc]
    len_doc_info = len(doc_info)
    um_sim = []
    for doc_index in range(len_doc_info):
        li = []
        if doc_index not in chosen_doc:
            li.append(doc_index)
            li.append(temp_um_sim[doc_id_dict[doc_info[doc_index][0]]])
            um_sim.append(li)
    um_sim_list = range(len(um_sim))
    #返回[[index,sim]]
    # um_sim_lists = create_lists_unsim(um_sim,um_sim_list)
    # new_unsim_lists = []
    # for unsim_l in um_sim_lists:
    #     if unsim_l[0] not in chosen_doc:
    #         new_unsim_lists.append(unsim_l)
    sorted_list = sorted(um_sim, lambda x, y: cmp(x[1], y[1]), reverse=False)[:top_k]
    if 2*top_k <= len_doc_info:
        sorted_list = sorted_list[:top_k]
    else:
        t = len_doc_info - top_k
        sorted_list = sorted_list[:t]
    result = []
    for unsim in sorted_list:
        result.append(unsim[0])
    return result

def create_lists_unsim(um_sim,um_sim_list):
    """
    将um_sim 装换为[[index,sim]],index与matrix中的对应
    :param um_sim:
    :param um_sim_list:
    :return:[[index,sim]]
    """
    result = []
    for i in um_sim_list:
        li = []
        li.append(i)
        li.append(um_sim[i])
        result.append(li)
    print result
    return result

def sort_by_matrix(doc_recommend,doc_id_dict,doc_info):
    """
    将doc_recommend中的index与matrix中的对应起来
    :param doc_recommend:[index...]
    :param doc_id_dict:{"doc_id":index}
    :param doc_info:
    :return:[index_id]
    """
    temp = []
    for doc in doc_recommend:
        temp.append(doc_id_dict[doc_info[doc][0]])
    return temp

def z_score(temp,sim_matrix):
    """
    返回列表的z-score的值
    :param temp: [index...],与sim_matrix中相对应
    :param sim_matrix:相识度矩阵
    :return:
    """
    sum = 0
    for i in temp:
        for j in temp:
            if i < j:
                sum += sim_matrix[i][j]
            else:
                pass
    k = len(temp)
    result = 1-2*sum/(k*(k-1))
    return result

def cover_rate(doc_recommend,doc_info,hos_type_sum):
    """
    返回医院覆盖率
    :param doc_recommend:[index...]
    :param doc_info:
    :param hos_type_sum:医院总数
    :return:
    """
    d = set()
    for doc in doc_recommend:
        # print "=======",doc
        # print "=======---",doc_info[doc][2]
        d.add(doc_info[doc][2])
    result = len(d)/hos_type_sum
    return result

def get_doc_id_dict(table_name):
    """
    生成doc_id 与数据库表中doc_id对应位置的index,并返回
    :param table_name:表名
    :return:doc_id_dict:{"id":index}
    """
    doc_id_dict = {}
    sql = 'select * from {0}'
    sql = sql.format(table_name)
    db = DatabaseConnection()
    cur = db.dbConnect()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    index = 0
    for row in result:
        doc_id_dict[row[0]] = index
        index += 1
    return doc_id_dict

def static_type_sum(info,index):
    """
    返回info中按指定的index内容统计的分类数量，以dic形式返回,{"type":num}
    :param info: 包含医院名信息的二维数组
    :param index: 医院名在第二维中的位置
    :return: :{"type":num}
    """
    dic = {}
    t = list(info)
    hos = 0
    while hos < len(t):
        name = t[hos][index]
        t.pop(hos)
        i = 1
        if (len(t) == 0):
            dic[name] = i
            break;
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
    return dic
