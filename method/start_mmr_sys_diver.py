# -*- coding: utf-8 -*-
"""
Created on 2018/2/2 19:30
@file: start_mmr_sys_diver.py
@author: Administrator
"""
from __future__ import division
from system_diversity import system_diversity
import mmr
import numpy as np
import time
import log
import tool.readtxt as dealtxt
from tool.math_method import get_sim_matrix
import greedy_algorithm as greedy
import recommend_diversity as re_div
import tool.math_method as mathn
import tool.File_utils as fu

def caculate_for_diversity(table_name, ratio, top_k=20,greedy_Lambda = 0.6,r = 0.001):
    """
    多样性实验
    :param table_name:
    :param ratio:
    :param r:
    :param top_k:
    :return:
    """
    # 上海交大，合工大(老区)，
    # people = ['31.031583,121.442614','31.849273,117.302611','40.011006,116.338897']
    # diseases = ['高血压','','']
    # 获取对应比率的预测矩阵
    matrix = dealtxt.load_file_to_array(
        "../matrix/" + table_name[3:].decode('utf-8') + "/result/pre_" + str(ratio) + ".txt");
    recommend_server = re_div.Recommend_Server()
    final_hos_rank = recommend_server.filter_hos_by_sorted(table_name)
    # 加上医院的最终排名信息，得到的医生信息，但不包含预测填充后的评分 doc_info：[[doc_id,doc_name,hos_name,rank,hos_locat]]
    doc_info_un = recommend_server.get_doc_info(table_name, final_hos_rank)

    # start循环开始
    diseases = recommend_server.get_disease(table_name)
    peoples = recommend_server.get_university(table_name)#peoples:[[name,latlng]...]
    random_disease = mathn.get_random_sort(diseases)
    mmr_list = []
    mmr_list_matrix_index = []
    two_list = []
    two_list_matrix_index = []

    for chosen_disease in diseases[:5]:
        un_peoples = mathn.get_random_sort(peoples)
        for chosen_people in un_peoples[:5]:
            # 添加车程信息，并排除掉超出指定车程范围的医院的医生, doc_info：[[doc_id,doc_name,hos_name,rank,hos_locat,duration]]
            # people_hospital_duration{"hos_name",duration}
            doc_info_un2, people_hospital_duration = recommend_server.filter_by_sql_duration(chosen_people, doc_info_un)
            # doc_info_un2, people_hospital_duration = recommend_server.filter_by_duration(chosen_people, doc_info_un)
            print "医生数量:", len(doc_info_un2)
            # 得到预测填充后的评分,{"hos_id":point}
            forecast_socre = recommend_server.matrix_score_by_disease(chosen_disease, table_name, matrix)
            print "填充矩阵评分:", forecast_socre
            # 添加评分，得到对应疾病最终的医生信息, doc_info：[[doc_id,doc_name,hos_name,rank,hos_locat,duration,socre]]
            doc_info = recommend_server.add_score(doc_info_un2, forecast_socre)
            print "医生数量:", len(doc_info)
            # ls_sort:[index]按weight降序排列后的
            ls_sort = recommend_server.weighth_with_duration(doc_info)
            print "按weight降序医生数量:", len(ls_sort)
            # doc_id_dict:{"doc_id":index}
            doc_id_dict = greedy.get_doc_id_dict(table_name)
            sim_matrix = get_sim_matrix(matrix)
            print "ls_sort数量:", len(ls_sort)
            print "MMR====================================MMR"
            recommend_list_mmr, recommend_list_mmr_index = mmr.MMR(doc_info,doc_id_dict, sim_matrix,greedy_Lambda,top_k)
            print "recommend_list_mmr",recommend_list_mmr
            print "recommend_list_mmr_index",recommend_list_mmr_index
            mmr_list.append(recommend_list_mmr)
            mmr_list_matrix_index.append(recommend_list_mmr_index)
            print "two====================================two"
            recommend_list_two, recommend_list_two_index = greedy.greedy_two(ls_sort, doc_info, doc_id_dict, sim_matrix, r, top_k)
            two_list.append(recommend_list_two)
            two_list_matrix_index.append(recommend_list_two_index)
            # end循环结束

    # # 添加车程信息，并排除掉超出指定车程范围的医院的医生, doc_info：[[doc_id,doc_name,hos_name,rank,hos_locat,duration]]
    # # people_hospital_duration{"hos_name",duration}
    # doc_info_un2, people_hospital_duration = recommend_server.filter_by_duration(people, doc_info_un, 4)
    # print "医生数量:", len(doc_info_un2)
    # # 得到预测填充后的评分,{"hos_id":point}
    # forecast_socre = recommend_server.matrix_score_by_disease(disease, table_name, matrix)
    # print "填充矩阵评分:", forecast_socre
    # # 添加评分，得到对应疾病最终的医生信息, doc_info：[[doc_id,doc_name,hos_name,rank,hos_locat,duration,socre]]
    # doc_info = recommend_server.add_score(doc_info_un2, forecast_socre)
    # print "医生数量:", len(doc_info)
    # # ls_sort:[index]按weight降序排列后的
    # ls_sort = recommend_server.weighth_with_duration(doc_info)
    # print "按weight降序医生数量:", len(ls_sort)
    # # doc_id_dict:{"doc_id":index}
    # doc_id_dict = greedy.get_doc_id_dict(table_name)
    # sim_matrix = get_sim_matrix(matrix)
    # # 医院总数
    # hos_type_sum = recommend_server.static_type_sum(doc_info, 2)
    # # 阈值
    # r = 0.0004
    # # top_k
    # k = 20
    # print "ls_sort数量:", len(ls_sort)
    # recommend_list_one,recommend_list_two_index = greedy.greedy_one(ls_sort, doc_info, doc_id_dict, hos_type_sum, sim_matrix, r, k)
    # print "two====================================two"
    # recommend_list_two,recommend_list_two_index = greedy.greedy_two(ls_sort, doc_info, doc_id_dict, hos_type_sum, sim_matrix, r, k)
    # # end循环结束

    # start结果输出
    fu.savetxt("../matrix/" + table_name[3:].decode('utf-8') + "/mmr_recommend_" + str(ratio) + ".txt",
               mmr_list)
    fu.savetxt("../matrix/" + table_name[3:].decode('utf-8') + "/mmr_recommend_matrix_index_" + str(ratio) + ".txt",
               mmr_list_matrix_index)
    np.savetxt("../matrix/" + table_name[3:].decode('utf-8') + "/two_recommend_" + str(ratio) + ".txt",
               np.array(two_list,dtype = int),
               fmt='%d')
    np.savetxt("../matrix/" + table_name[3:].decode('utf-8') + "/two_recommend_matrix_index_" + str(ratio) + ".txt",
               np.array(two_list_matrix_index,dtype = int),
               fmt='%d')
    start_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    mmr_diversity = system_diversity(mmr_list_matrix_index, table_name)
    two_diversity = system_diversity(two_list_matrix_index, table_name)

    log.start_log(start_time,
                  "../matrix/" + table_name[3:].decode('utf-8') + "/" + "推荐排序结果.txt".decode('utf-8'))
    f = log.write_log()
    print >> f, "recommend_list_one:", recommend_list_mmr
    for i in range(len(recommend_list_mmr)):
        # print "int(recommend_list[i])",recommend_list_one[i]
        print >> f, ("%-25s%-25s" % (doc_info[int(recommend_list_mmr[i])][2].encode('utf-8'),
                                     doc_info[int(recommend_list_mmr[i])][1].encode('utf-8')))
    print >> f, "=================================================="
    print >> f, "recommend_list_two:", recommend_list_two
    for j in range(len(recommend_list_two)):
        # print "int(recommend_list[i])",recommend_list_two[i]
        print >> f, ("%-25s%-20s" % (doc_info[int(recommend_list_two[j])][2].encode('utf-8'),
                                     doc_info[int(recommend_list_two[j])][1].encode('utf-8')))
    # print >> f, ("diversity:%-20s" % (two_diversity))
    # print ("diversity:%-20s" % (two_diversity))
    # print >> f, ("diversity:%-20s" % (one_diversity))
    # print ("diversity:%-20s" % (one_diversity))
    print ("diversity:%-20s%-20s" % (mmr_diversity, two_diversity))
    print >> f, ("diversity:%-20s%-20s" % (mmr_diversity,two_diversity))
    log.close_log()
    # end结果输出
    return mmr_diversity, two_diversity

if __name__ == '__main__':
    table_name = 'tp_神经内科'
    ratio = '0.80'
    caculate_for_diversity(table_name, ratio, top_k=20,greedy_Lambda = 0.6)