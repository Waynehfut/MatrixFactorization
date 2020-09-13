# -*- coding: utf-8 -*-
"""
Created on 2018/2/1 14:40
@file: mmr.py
@author: Administrator
"""
from __future__ import division
import tool.math_method as mathm
import math
import tool.sorted_utils as sorted


def MMR(doc_info,doc_id_dict, sim_matrix,greedy_Lambda,top_k):
    """
    doc_info:[[doc_id,doc_name,hos_name,rank,hos_locat,duration,socre]]
    :param doc_info:医生信息
    :return:[index,...,index]
    """
    # # 总评分
    # c_sum = mathm.get_sum_by_index(doc_info, 6)
    # 得到对应列的最大值
    c_max = mathm.get_max_by_index(doc_info, 6)
        # 医院最低排名
    hos_lowest = mathm.get_maxormin_by_index(doc_info, 3, "max")
        # 最远车程
    max_duration = mathm.get_maxormin_by_index(doc_info, 5, "max")
    # hos_dic:医院数量信息
    hos_dic = static_type_sum(doc_info,2)
    hos_sum = len(hos_dic)
    temp_doc_info = list(doc_info)
    recommend_list = []
    add_set = set()
    for k in range(top_k):
        ls = []
        i = 0
        if len(add_set) == len(doc_info):
            break
        while i < len(doc_info):
            if i in add_set:
                pass
            else:
                li = []
                w_c = doc_info[i][6] / c_max
                w_h = int(hos_dic[doc_info[i][2]]) / hos_sum * (-doc_info[i][3] / (hos_lowest + 1) + 1)
                temp_d = doc_info[i][5] / (max_duration + 1)
                w_d = (1 - temp_d) * math.exp(-(doc_info[i][5] / max_duration))
                # ls_sort[doc_info[i][0]] = w_c * w_h * w_d
                utility = w_c * w_h * w_d
                if len(recommend_list) == 1 or len(recommend_list) == 0:
                    div_dif = 0
                else:
                    prefore_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
                    recommend_list.append(i)
                    present_diversity = single_diversity(recommend_list, sim_matrix, doc_id_dict, doc_info, hos_sum)
                    recommend_list.pop(len(recommend_list)-1)
                    div_dif = present_diversity - prefore_diversity
                fx = (1 - greedy_Lambda) * utility + greedy_Lambda * div_dif
                li.append(i)
                li.append(fx)
                ls.append(li)

            i += 1
        # 降序,取最大的
        # print "ls:",len(ls)
        max_doc_fx = sorted.sort_by_index(ls,1)[0]
        add_set.add(max_doc_fx[0])
        recommend_list.append(max_doc_fx[0])
    # print "recommend_list:",recommend_list
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
    if len(doc_recommend) == 0 or len(doc_recommend) == 1:
        diversity = 0
    else:
        temp = sort_by_matrix(doc_recommend, doc_id_dict, doc_info)
        n, m = sim_matrix.shape
        # print "sim_matrix:",len(sim_matrix)
        zs = z_score(temp, sim_matrix)
        cr = cover_rate(doc_recommend, doc_info, hos_sum)
        diversity = pow(zs * cr, 0.5)
    return diversity


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
        d.add(doc_info[doc][2])
    result = len(d)/hos_type_sum
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


def sort_by_matrix(doc_recommend,doc_id_dict,doc_info):
    """
    将doc_recommend中的index与matrix中的对应起来
    :param doc_recommend:[index...]
    :param doc_id_dict:{"doc_id":index}
    :param doc_info:
    :return:[index_id]
    """
    # for doc in doc_info:
    #     print doc[0]
    temp = []
    for doc in doc_recommend:
        temp.append(doc_id_dict[doc_info[doc][0]])
    return temp


def static_type_sum(info, index):
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
    # for key, values in dic.items():
    #     print "k:", key
    #     print "v:", values
    # print "----------------------hos_dict：", dic
    return dic
