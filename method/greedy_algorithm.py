# -*- coding: utf-8 -*-
"""
Created on 2018/1/24 21:55
@file: greedy_algorithms.py
@author: Administrator
"""
from __future__ import division
from confact import *
import random

def swap_b2(ls_sort, doc_info, doc_id_dict, doc_info_matrix_dict, doc_matrix_info_dict, sim_matrix, r, top_k):
    """
    置换算法二，返回一维数组，包含doc_info对应的index
    :param ls_sort: [index...]
    :param doc_info:
    :param doc_id_dict:
    :param doc_info_matrix_dict:{doc_info_index:matrix_index}
    :param doc_matrix_info_dict:{matrix_index:doc_info_index}
    :param hos_type_sum:
    :param sim_matrix:
    :param r: 阈值
    :param top_k: 取前k个医生
    :return:
    """
    recommend_list = ls_sort[:top_k]
    # 医院总数
    hos_type_sum = static_type_sum(doc_info, 2)
    #获取候选集
    candidate_list = list(ls_sort[top_k:])
    hos_sum = len(hos_type_sum)
    #判断是否连续达到平稳状态，即多样性的数值达到稳定
    steady_time = 0
    judge_i = 0
    prefore_diversity = 0
    present_diversity = 0
    while len(candidate_list) != 0 and steady_time < 7:
        if judge_i == 1:
            prefore_diversity = present_diversity
            recommend_matrix = get_matrix_recommend_list(recommend_list, doc_info_matrix_dict)
            k = max_candidate(recommend_list,candidate_list,sim_matrix,doc_info_matrix_dict,doc_info)
            swap_index = get_max_sim(k, recommend_matrix, doc_info_matrix_dict, doc_matrix_info_dict, sim_matrix)
            origin_index = recommend_list[swap_index]
            recommend_list[swap_index] = candidate_list[k]
            present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        elif judge_i == 2:
            prefore_diversity = prefore_diversity
            recommend_matrix = get_matrix_recommend_list(recommend_list, doc_info_matrix_dict)
            k = max_candidate(recommend_list,candidate_list,sim_matrix,doc_info_matrix_dict,doc_info)
            swap_index = get_max_sim(k, recommend_matrix, doc_info_matrix_dict, doc_matrix_info_dict, sim_matrix)
            origin_index = recommend_list[swap_index]
            recommend_list[swap_index] = candidate_list[k]
            present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        else:
            prefore_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
            recommend_matrix = get_matrix_recommend_list(recommend_list, doc_info_matrix_dict)
            k = max_candidate(recommend_list,candidate_list,sim_matrix,doc_info_matrix_dict,doc_info)
            swap_index = get_max_sim(k, recommend_matrix, doc_info_matrix_dict, doc_matrix_info_dict, sim_matrix)
            origin_index = recommend_list[swap_index]
            recommend_list[swap_index] = candidate_list[k]
            present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        # prefore_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        # random_num = random.randint(0, (top_k - 1))
        # origin_index = recommend_list[random_num]
        # recommend_list[random_num] = ls_sort_copy[0]
        # present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
            # 置换条件
        diff = present_diversity - prefore_diversity

        # print "prefore_diversity", prefore_diversity
        # print "present_diversity", present_diversity
        # print "present_diversity-prefore_diversity:",diff
        if diff > 0:
            steady_time = 0
            judge_i = 1
        else:
            judge_i = 2
            recommend_list[swap_index] = origin_index
            steady_time += 1
        candidate_list.pop(0)
    # print "steady_time:",steady_time
    recommend_list_as_index = sort_by_matrix(recommend_list, doc_id_dict, doc_info)
    return recommend_list,recommend_list_as_index

def greedy_b2(ls_sort, doc_info, doc_id_dict, doc_info_matrix_dict,doc_matrix_info_dict, sim_matrix, r, top_k):
    """
    贪心算法一，返回一维数组，包含doc_info对应的index
    doc_info:[[doc_id,doc_name,hos_name,rank,hos_locat,duration,socre,utility]]
    :param ls_sort:[index...]
    :param doc_info:
    :param doc_id_dict:
    :param doc_matrix_d1ict:{doc_info_index:matrix_index}
    :param hos_type_sum:
    :param sim_matrix:相识度矩阵
    :param r: 阈值
    :param top_k: 取前k个医生
    :return: [index,...,index]
    """
    candidate = list(ls_sort)
    length = len(candidate)
    # 医院总数
    hos_type_sum = static_type_sum(doc_info, 2)
    #记录的是doc_info 对应的index
    recommend_list = []
    #先添加第一个,第二个
    recommend_list.append(candidate[0])
    candidate.pop(0)
    recommend_list.append(candidate[1])
    candidate.pop(1)
    i = 2
    hos_sum = len(hos_type_sum)
    judge_i = 0
    prefore_diversity = 0
    present_diversity = 0
    while i < length:
        if judge_i == 1:
            prefore_diversity = present_diversity
            recommend_matrix = get_matrix_recommend_list(recommend_list, doc_info_matrix_dict)
            k = max_candidate(recommend_matrix,candidate,sim_matrix,doc_info_matrix_dict,doc_info)
            recommend_list.append(candidate[k])
            present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        elif judge_i ==2:
            prefore_diversity = prefore_diversity
            recommend_matrix = get_matrix_recommend_list(recommend_list, doc_info_matrix_dict)
            k = max_candidate(recommend_matrix, candidate, sim_matrix, doc_info_matrix_dict, doc_info)
            recommend_list.append(candidate[k])
            present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        else:
            prefore_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
            recommend_matrix = get_matrix_recommend_list(recommend_list, doc_info_matrix_dict)
            k = max_candidate(recommend_matrix, candidate, sim_matrix, doc_info_matrix_dict, doc_info)
            recommend_list.append(candidate[k])
            present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        #添加条件
        diff = present_diversity-prefore_diversity
        # print "prefore_diversity", prefore_diversity
        # print "present_diversity", present_diversity
        # print "present_diversity-prefore_diversity:",diff
        if diff > 0:
            judge_i = 1
            candidate.pop(k)
            pass
        else:
            judge_i = 2
            recommend_list.pop(len(recommend_list) - 1)
            candidate.pop(k)
        i += 1
        if len(recommend_list) == top_k:
            break
    recommend_list_as_index = sort_by_matrix(recommend_list, doc_id_dict, doc_info)
    return recommend_list,recommend_list_as_index

def dum(ls_sort, doc_info, doc_id_dict, sim_matrix, top_k):
    """
    贪心算法，返回一维数组，包含doc_info对应的index
    :param ls_sort:[index...]
    :param doc_info:
    :param doc_id_dict:
    :param hos_type_sum:
    :param sim_matrix:相识度矩阵
    :param top_k: 取前k个医生
    :return: [index,...,index]
    """
    length = len(ls_sort)
    # 医院总数
    hos_type_sum = static_type_sum(doc_info, 2)
    #记录的是doc_info 对应的index
    recommend_list = []
    #先添加第一个,第二个
    recommend_list.append(ls_sort[0])
    recommend_list.append(ls_sort[1])
    i = 2
    hos_sum = len(hos_type_sum)
    judge_i = 0
    prefore_diversity = 0
    present_diversity = 0
    while i < length:
        if judge_i == 1:
            prefore_diversity = present_diversity
            recommend_list.append(ls_sort[i])
            present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        elif judge_i ==2:
            prefore_diversity = prefore_diversity
            recommend_list.append(ls_sort[i])
            present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        else:
            prefore_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
            recommend_list.append(ls_sort[i])
            present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        #添加条件
        diff = present_diversity-prefore_diversity
        # print "prefore_diversity", prefore_diversity
        # print "present_diversity", present_diversity
        # print "present_diversity-prefore_diversity:",diff
        if diff > 0:
            judge_i = 1
            pass
        else:
            judge_i = 2
            recommend_list.pop(len(recommend_list) - 1)
        i += 1
        if len(recommend_list) == top_k:
            break
    recommend_list_as_index = sort_by_matrix(recommend_list, doc_id_dict, doc_info)
    return recommend_list,recommend_list_as_index

def greedy_one(ls_sort, doc_info, doc_id_dict, sim_matrix, r, top_k):
    """
    贪心算法一，返回一维数组，包含doc_info对应的index
    :param ls_sort:[index...]
    :param doc_info:
    :param doc_id_dict:
    :param hos_type_sum:
    :param sim_matrix:相识度矩阵
    :param r: 阈值
    :param top_k: 取前k个医生
    :return: [index,...,index]
    """
    length = len(ls_sort)
    # 医院总数
    hos_type_sum = static_type_sum(doc_info, 2)
    #记录的是doc_info 对应的index
    recommend_list = []
    #先添加第一个,第二个
    recommend_list.append(ls_sort[0])
    recommend_list.append(ls_sort[1])
    i = 2
    hos_sum = len(hos_type_sum)
    judge_i = 0
    prefore_diversity = 0
    present_diversity = 0
    while i < length:
        if judge_i == 1:
            prefore_diversity = present_diversity
            recommend_list.append(ls_sort[i])
            present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        elif judge_i ==2:
            prefore_diversity = prefore_diversity
            recommend_list.append(ls_sort[i])
            present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        else:
            prefore_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
            recommend_list.append(ls_sort[i])
            present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        #添加条件
        diff = present_diversity-prefore_diversity
        # print "prefore_diversity", prefore_diversity
        # print "present_diversity", present_diversity
        # print "present_diversity-prefore_diversity:",diff
        if diff > r:
            judge_i = 1
            pass
        else:
            judge_i = 2
            recommend_list.pop(len(recommend_list) - 1)
        i += 1
        if len(recommend_list) == top_k:
            break
    recommend_list_as_index = sort_by_matrix(recommend_list, doc_id_dict, doc_info)
    return recommend_list,recommend_list_as_index

def greedy_two(ls_sort, doc_info, doc_id_dict, sim_matrix, r, top_k):
    """
    置换算法二，返回一维数组，包含doc_info对应的index
    :param ls_sort: [index...]
    :param doc_info:
    :param doc_id_dict:
    :param hos_type_sum:
    :param sim_matrix:
    :param r: 阈值
    :param top_k: 取前k个医生
    :return:
    """
    recommend_list = ls_sort[:top_k]
    # 医院总数
    hos_type_sum = static_type_sum(doc_info, 2)
    ls_sort_copy = list(ls_sort[top_k:])
    hos_sum = len(hos_type_sum)
    #判断是否连续达到平稳状态，即多样性的数值达到稳定
    steady_time = 0
    judge_i = 0
    prefore_diversity = 0
    present_diversity = 0
    while len(ls_sort_copy) != 0 and steady_time < 7:
        # if judge_i == 1:
        #     prefore_diversity = present_diversity
        #     random_num = random.randint(0, (top_k - 1))
        #     origin_index = recommend_list[random_num]
        #     recommend_list[random_num] = ls_sort_copy[0]
        #     present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        # elif judge_i == 2:
        #     prefore_diversity = prefore_diversity
        #     random_num = random.randint(0, (top_k - 1))
        #     origin_index = recommend_list[random_num]
        #     recommend_list[random_num] = ls_sort_copy[0]
        #     present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        # else:
        #     prefore_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        #     random_num = random.randint(0, (top_k - 1))
        #     origin_index = recommend_list[random_num]
        #     recommend_list[random_num] = ls_sort_copy[0]
        #     present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        prefore_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
        random_num = random.randint(0, (top_k - 1))
        origin_index = recommend_list[random_num]
        recommend_list[random_num] = ls_sort_copy[0]
        present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
            # 置换条件
        diff = present_diversity - prefore_diversity

        # print "prefore_diversity", prefore_diversity
        # print "present_diversity", present_diversity
        # print "present_diversity-prefore_diversity:",diff
        if diff > r:
            steady_time = 0
            judge_i = 1
        else:
            judge_i = 2
            recommend_list[random_num] = origin_index
            steady_time += 1
        ls_sort_copy.pop(0)
    # print "steady_time:",steady_time
    recommend_list_as_index = sort_by_matrix(recommend_list, doc_id_dict, doc_info)
    return recommend_list,recommend_list_as_index

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

    zs = z_score(temp, sim_matrix)
    cr = cover_rate(doc_recommend, doc_info, hos_sum)
    # print "z_score:",zs
    # print "cover_rate:",cr
    diversity = pow(zs * cr, 0.5)

    # if len(doc_recommend)==1:
    #     diversity = 0
    # else:
    #     # print "sim_matrix:",len(sim_matrix)
    #     zs = z_score(temp, sim_matrix)
    #     cr = cover_rate(doc_recommend, doc_info, hos_sum)
    #     # print "z_score:",zs
    #     # print "cover_rate:",cr
    #     diversity = pow(zs * cr, 0.5)
    return diversity

def sort_by_matrix_dict(doc_id_dict,doc_info):
    """
    将doc_recommend中的index与matrix中的对应起来以dict形式返回
    :param doc_recommend:[index...]
    :param doc_id_dict:{"doc_id":index}
    :param doc_info:
    :return:{index:matrix_index}
    """
    temp = {}
    i = 0
    len_doc_info = len(doc_info)
    while i < len_doc_info:
        temp[i] = doc_id_dict[doc_info[i][0]]
        i += 1
    return temp

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

def max_candidate(recommend_matrix,candidate_list,sim_matrix,doc_info_matrix_dict,doc_info):
    """
    返回候选集中多样性与效用综合性最大的index,与candidate
    :param recommend_matrix_id:推荐列表，其中的值与matrix对应
    :param candidate:
    :param sim_matrix:
    :param doc_id_dict:
    :param doc_info:
    :return:
    """
    li = []
    for i in range(len(candidate_list)):
        index = doc_info_matrix_dict[candidate_list[i]]
        # aver_unsim = get_aver_unsim(index,recommend_matrix,sim_matrix)
        utility = doc_info[candidate_list[i]][7]
        # d = aver_unsim * 0.5 + utility * 0.5
        d = utility
        li.append(d)
    result = max_index(li)
    return result

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

def get_doc_index_dict(table_name,doc_info):
    """
    生成doc_index 与数据库表中doc_id对应位置的index,并返回
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
    i = 0
    doc_info_matrix_dict = {}
    doc_matrix_info_dict = {}
    for row in result:
        doc_id_dict[row[0]] = index
        index += 1
    for doc in doc_info:
        doc_info_matrix_dict[i] = doc_id_dict[doc[0]]
        doc_matrix_info_dict[doc_id_dict[doc[0]]] = i
        i += 1
    return doc_id_dict,doc_info_matrix_dict,doc_matrix_info_dict

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

def get_aver_unsim(index, recommend_matrix_list, sim_matrix):
    """
    返回指定医生index与temp中医生的不相似性的平均值
    :param index:
    :param recommend_matrix_list:
    :param sim_matrix:
    :return:
    """
    sum_sim = 0
    n = len(recommend_matrix_list)
    for i in recommend_matrix_list:
        sum_sim += sim_matrix[index][i]
    aver_unsim = (n-sum_sim)/n
    return aver_unsim

def max_index(li):
    """
    返回li列表中最大值的index
    :param li:
    :return:
    """
    i = 0
    temp = li[0]
    for j in range(len(li)):
        if li[j] > temp:
            i = j
            temp = li[j]
    return i

def get_matrix_recommend_list(candidate,doc_info_matrix_dict):
    """
    将candidate中的index与matrix中的对应起来
    :param candidate:
    :param doc_matrix_id_dict:
    :return:
    """
    li = []
    for k in candidate:
        li.append(doc_info_matrix_dict[k])
    return li

def get_max_sim(k,recommend_matrix,doc_info_matrix_dict,doc_matrix_info_dict,sim_matrix):
    """
    获取候选集中与医生k(matrix)最相似的医生index(doc_info)
    :param k:
    :param recommend_matrix:
    :param doc_matrix_dict:
    :param sim_matrix:
    :return:
    """
    #获取matrix对应的值
    i = doc_info_matrix_dict[k]
    mindex = 0
    msim = sim_matrix[i][recommend_matrix[mindex]]
    j = 0
    for k in recommend_matrix:
        temp = sim_matrix[i][k]
        if msim < temp:
           msim = temp
           mindex = j
        j += 1
    return mindex