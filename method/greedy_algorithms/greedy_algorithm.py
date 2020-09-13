# -*- coding: utf-8 -*-
"""
Created on 2018/1/24 21:55
@file: greedy_algorithms.py
@author: Administrator
"""
from __future__ import division
import random

def greedy_one(ls_sort,doc_info,doc_id_dict,hos_type_sum,sim_matrix,r,k):
    """
    贪心算法一，返回一维数组，包含doc_info对应的index
    :param ls_sort:[index...]
    :param doc_info:
    :param sim_matrix:相识度矩阵
    :param r: 阈值
    :param k: 取前k个医生
    :return: [index,...,index]
    """
    length = len(ls_sort)
    #记录的是doc_info 对应的index
    doc_recommend = []
    #先添加第一个,第二个
    doc_recommend.append(ls_sort[0])
    doc_recommend.append(ls_sort[1])
    i = 2
    hos_sum = len(hos_type_sum)
    while i < length:
        prefore_diversity = single_diversity(doc_recommend,sim_matrix,doc_id_dict,doc_info,hos_sum)
        doc_recommend.append(ls_sort[i])
        present_diversity = single_diversity(doc_recommend,sim_matrix,doc_id_dict,doc_info,hos_sum)
        #添加条件
        if (present_diversity-prefore_diversity)> r:
            pass
        else:
            doc_recommend.pop(len(doc_recommend)-1)
        if len(doc_recommend) == k:
            break
    return doc_recommend

def greedy_two(ls_sort,doc_info,doc_id_dict,hos_type_sum,sim_matrix,r,k):
    """
    置换算法二，返回一维数组，包含doc_info对应的index
    :param ls_sort: [index...]
    :param doc_info:
    :param doc_id_dict:
    :param hos_type_sum:
    :param sim_matrix:
    :param r: 阈值
    :param k: 取前k个医生
    :return:
    """
    recommend_list = ls_sort[:k]
    ls_sort_copy = list(ls_sort[k:])
    hos_sum = len(hos_type_sum)
    #判断是否连续达到平稳状态，即多样性的数值达到稳定
    steady_time = 0
    while len(ls_sort_copy) != 0 or steady_time < 4:
        prefore_diversity = single_diversity(recommend_list,sim_matrix,doc_id_dict,doc_info,hos_sum)
        random_num = random.randint(0, k)
        origin_index = recommend_list[random_num]
        recommend_list[random_num] = ls_sort_copy[0]
        present_diversity = single_diversity(recommend_list,sim_matrix,doc_id_dict,doc_info,hos_sum)
        #置换条件
        if (present_diversity-prefore_diversity)> r:
            recommend_list[random_num] = origin_index
            steady_time += 1
        else:
            steady_time = 0
            pass
        ls_sort_copy.pop(0)
    return recommend_list

def single_diversity(doc_recommend,sim_matrix,doc_id_dict,doc_info,hos_sum):
    """
    计算单个个体推荐的多样性
    :param doc_recommend:
    :param sim_matrix: 相似度矩阵
    :param doc_info: 医生信息
    :return:
    """
    temp = sort_by_matrix(doc_recommend,doc_id_dict,doc_info)
    c = z_score(temp,sim_matrix)*cover_rate(doc_recommend,doc_info,hos_sum)
    diversity = pow(c,0.5)
    return diversity

def sort_by_matrix(doc_recommend,doc_id_dict,doc_info):
    """
    将doc_recommend中的index与sim_matrix中的对应起来
    :param doc_recommend:[index...]
    :param doc_id_dict:{"doc_id":id}
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
                break
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
        d.add(doc_info[doc])
    result = len(d)/hos_type_sum
    return result



