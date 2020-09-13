# -*- coding: utf-8 -*-
"""
Created on 2018/2/2 9:33
@file: start_system_diversity.py
@author: Administrator
"""
from __future__ import division
from system_diversity import system_diversity
import mmr
import time
import log
import tool.readtxt as dealtxt
from tool.math_method import get_sim_matrix
import greedy_algorithm as greedy
import recommend_diversity as re_div
import tool.math_method as mathn
import tool.File_utils as fu
import tool.ULog as ul
import vns


def caculate_for_diversity(table_name, ratio, r=0.0004, top_k=20, greedy_Lambda=0.6):
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
    if table_name[3:] == '神经内科':
        sql = 'select  *  from seven20_university_b'
        peoples = recommend_server.get_university_sql(table_name, sql)  # peoples:[[name,latlng]...]
    else:
        sql = 'select  *  from seven20_university_a'
        peoples = recommend_server.get_university_sql(table_name, sql)  # peoples:[[name,latlng]...]
    # peoples = recommend_server.get_university(table_name)#peoples:[[name,latlng]...]
    random_disease = mathn.get_random_sort(diseases)

    save_random_disease = []#用于存储中间数据
    save_random_people = []  # 用于存储中间数据
    original_list = []
    original_list_matrix_index = []
    two_list = []
    two_list_matrix_index = []
    greedy2_list = []
    greedy2_list_matrix_index = []
    swap2_list = []
    swap2_list_matrix_index = []
    dum_list = []
    dum_list_matrix_index = []
    mmr_list = []
    mmr_list_matrix_index = []
    vns_list = []
    vns_list_matrix_index = []

    random_diss = random_disease[:20]
    for chosen_disease in random_diss:
        un_peoples = mathn.get_random_sort(peoples)[:100]
        save_random_people.append(un_peoples)  # 存储中间数据
        for chosen_people in un_peoples:
            # 添加车程信息，并排除掉超出指定车程范围的医院的医生, doc_info：[[doc_id,doc_name,hos_name,rank,hos_locat,duration]]
            # people_hospital_duration{"hos_name",duration}
            doc_info_un2, people_hospital_duration = recommend_server.filter_by_sql_duration(chosen_people, doc_info_un)
            # doc_info_un2, people_hospital_duration = recommend_server.filter_by_duration(chosen_people, doc_info_un)
            if len(doc_info_un2) < top_k:
                ul.write_log('../matrix/systme_diversity_wrong_log.txt', chosen_people.encode('utf-8'))
            # print "医生数量:", len(doc_info_un2)
            # 得到预测填充后的评分,{"hos_id":point}
            forecast_socre = recommend_server.matrix_score_by_disease(chosen_disease, table_name, matrix)
            # print "填充矩阵评分:", forecast_socre
            # 添加评分，得到对应疾病最终的医生信息, doc_info：[[doc_id,doc_name,hos_name,rank,hos_locat,duration,socre]]
            doc_info = recommend_server.add_score(doc_info_un2, forecast_socre)
            # print "医生数量:", len(doc_info)
            # ls_sort:[index]按weight降序排列后的,doc_info:[[doc_id,doc_name,hos_name,rank,hos_locat,duration,socre,utility]]
            ls_sort, doc_info = recommend_server.weighth_with_duration(doc_info)
            # print "按weight降序医生数量:", len(ls_sort)

            # doc_id_dict:{"doc_id":index}
            # doc_id_dict = greedy.get_doc_id_dict(table_name)
            doc_id_dict, doc_info_matrix_dict, doc_matrix_info_dict = greedy.get_doc_index_dict(table_name, doc_info)
            doc_list = get_doc_info_list_m(doc_info_matrix_dict)

            sim_matrix = get_sim_matrix(matrix)

            # print "origin====================================origin"
            recommend_list_original = ls_sort[:top_k]
            recommend_list_original_index = greedy.sort_by_matrix(recommend_list_original, doc_id_dict, doc_info)
            original_list.append(recommend_list_original)
            original_list_matrix_index.append(recommend_list_original_index)


            # print "two====================================two"
            recommend_list_two, recommend_list_two_index = greedy.greedy_two(ls_sort, doc_info, doc_id_dict, sim_matrix,
                                                                             r, top_k)
            two_list.append(recommend_list_two)
            two_list_matrix_index.append(recommend_list_two_index)

            # print "ls_sort数量:", len(ls_sort)
            recommend_list_greedy2, recommend_list_greedy2_index = greedy.greedy_b2(ls_sort, doc_info, doc_id_dict,
                                                                            doc_info_matrix_dict, doc_matrix_info_dict,
                                                                            sim_matrix, r, top_k)
            greedy2_list.append(recommend_list_greedy2)
            greedy2_list_matrix_index.append(recommend_list_greedy2_index)

            # print "swap_b2====================================swap_b2"
            recommend_list_swap2, recommend_list_swap2_index = greedy.swap_b2(ls_sort, doc_info, doc_id_dict,
                                                                          doc_info_matrix_dict, doc_matrix_info_dict,
                                                                          sim_matrix, r, top_k)
            swap2_list.append(recommend_list_swap2)
            swap2_list_matrix_index.append(recommend_list_swap2_index)

            recommend_list_dum, recommend_list_dum_index = greedy.dum(ls_sort, doc_info, doc_id_dict,
                                                                          sim_matrix, top_k)
            dum_list.append(recommend_list_dum)
            dum_list_matrix_index.append(recommend_list_dum_index)

            # print "MMR====================================MMR"
            recommend_list_mmr, recommend_list_mmr_index = mmr.MMR(doc_info, doc_id_dict, sim_matrix, greedy_Lambda,
                                                                   top_k)
            mmr_list.append(recommend_list_mmr)
            mmr_list_matrix_index.append(recommend_list_mmr_index)
            # print "VNS====================================VNS"
            recommend_list_vns, recommend_list_vns_index = vns.vns(doc_info, doc_id_dict, sim_matrix, top_k)
            vns_list.append(recommend_list_vns)
            vns_list_matrix_index.append(recommend_list_vns_index)

    # start结果输出
    #存储中间数据
    fu.savetxt_li("../matrix/" + table_name[3:].decode('utf-8') + "/save_random_disease" + str(ratio) + ".txt",
               random_diss,chinese=True)  # 输出符合条件的医生矩阵 save_random_people
    fu.savetxt_three_dia("../matrix/" + table_name[3:].decode('utf-8') + "/save_random_people" + str(ratio) + ".txt",
               save_random_people,chinese=True)
    # fu.savetxt(
    #     "../matrix/" + table_name[3:].decode('utf-8') + "/original_recommend_matrix_index_" + str(ratio) + ".txt",
    #     original_list_matrix_index)
    # fu.savetxt("../matrix/" + table_name[3:].decode('utf-8') + "/one_recommend_matrix_index_" + str(ratio) + ".txt",
    #            one_list_matrix_index)
    # np.savetxt("../matrix/" + table_name[3:].decode('utf-8') + "/two_recommend_matrix_index_" + str(ratio) + ".txt",
    #            np.array(two_list_matrix_index, dtype=int),
    #            fmt='%d')
    # fu.savetxt("../matrix/" + table_name[3:].decode('utf-8') + "/mmr_recommend_matrix_index_" + str(ratio) + ".txt",
    #            mmr_list_matrix_index)
    # fu.savetxt("../matrix/" + table_name[3:].decode('utf-8') + "/vns_recommend_matrix_index_" + str(ratio) + ".txt",
    #            vns_list_matrix_index)

    start_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    # 计算系统多样性
    original_diversity = system_diversity(original_list_matrix_index, table_name)
    two_diversity = system_diversity(two_list_matrix_index, table_name)
    mmr_diversity = system_diversity(mmr_list_matrix_index, table_name)
    vns_diversity = system_diversity(vns_list_matrix_index, table_name)
    greedy2_diversity = system_diversity(greedy2_list_matrix_index, table_name)
    swap2_diversity = system_diversity(swap2_list_matrix_index,table_name)
    dum_diversity = system_diversity(dum_list_matrix_index, table_name)

    log.start_log(start_time,
                  "../matrix/" + table_name[3:].decode('utf-8') + "/" + "推荐排序结果.txt".decode('utf-8'))
    f = log.write_log()

    print >> f, "recommend_list_original:", recommend_list_original
    for i in range(len(recommend_list_original)):
        # print "int(recommend_list[i])",recommend_list_one[i]
        print >> f, ("%-25s%-25s" % (doc_info[int(recommend_list_original[i])][2].encode('utf-8'),
                                     doc_info[int(recommend_list_original[i])][1].encode('utf-8')))
    print >> f, "=================================================="
    # print >> f, "recommend_list_one:", recommend_list_one
    # for i in range(len(recommend_list_one)):
    #     # print "int(recommend_list[i])",recommend_list_one[i]
    #     print >> f, ("%-25s%-25s" % (doc_info[int(recommend_list_one[i])][2].encode('utf-8'),
    #                                  doc_info[int(recommend_list_one[i])][1].encode('utf-8')))
    # print >> f, "=================================================="
    # print >> f, "recommend_list_two:", recommend_list_two
    # for j in range(len(recommend_list_two)):
    #     # print "int(recommend_list[i])",recommend_list_two[i]
    #     print >> f, ("%-25s%-20s" % (doc_info[int(recommend_list_two[j])][2].encode('utf-8'),
    #                                  doc_info[int(recommend_list_two[j])][1].encode('utf-8')))
    print >> f, "=================================================="
    print >> f, "recommend_list_mmr:", recommend_list_mmr
    for i in range(len(recommend_list_mmr)):
        # print "int(recommend_list[i])",recommend_list_one[i]
        print >> f, ("%-25s%-25s" % (doc_info[int(recommend_list_mmr[i])][2].encode('utf-8'),
                                     doc_info[int(recommend_list_mmr[i])][1].encode('utf-8')))
    print >> f, "=================================================="
    # print >> f, "recommend_list_vns:", recommend_list_vns
    # for i in range(len(recommend_list_vns)):
    #     # print "int(recommend_list[i])",recommend_list_one[i]
    #     print >> f, ("%-25s%-25s" % (doc_info[int(recommend_list_vns[i])][2].encode('utf-8'),
    #                                  doc_info[int(recommend_list_vns[i])][1].encode('utf-8')))
    # print >> f, "=================================================="
    print >> f, "recommend_list_swap2:", recommend_list_swap2
    for i in range(len(recommend_list_swap2)):
        # print "int(recommend_list[i])",recommend_list_one[i]
        print >> f, ("%-25s%-25s" % (doc_info[int(recommend_list_swap2[i])][2].encode('utf-8'),
                                     doc_info[int(recommend_list_swap2[i])][1].encode('utf-8')))
    print >> f, "=================================================="

    print (("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            ratio, original_diversity, two_diversity,greedy2_diversity,swap2_diversity,dum_diversity, mmr_diversity, vns_diversity)))
    print >> f, ("%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s" % (
        ratio, original_diversity, two_diversity, greedy2_diversity, swap2_diversity, dum_diversity, mmr_diversity,
        vns_diversity))
    log.close_log()
    # end结果输出
    return original_diversity, two_diversity, greedy2_diversity, swap2_diversity,dum_diversity, mmr_diversity, vns_diversity


def start_sys_diversity(keshis, top_k):
    ratios = ['0.50', '0.55', '0.60', '0.65', '0.70', '0.75', '0.80', '0.85', '0.90',
              '0.95']
    excel_path = '..'
    file_path = '../matrix/system_diversity_result.txt'
    ul.write_log(file_path, ("%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s" % ('ratio', 'original', 'two', 'greedy2','swap2','dum','mmr', 'vns')))
    #ratio, original_diversity, one_diversity, two_diversity, greedy2_diversity, swap2_diversity, dum_diversity, mmr_diversity, vns_diversity
    title_list = ['ratio', 'Original', 'DivGreedy', 'DUM', 'DivSwap', 'SWAP', 'MMR', 'VNS']
    for keshi in range(len(keshis)):
        content_matrix = []
        excel_path = '../matrix/' + keshis[keshi][3:].decode('utf-8')+ '_system_diversity_result_.xls'
        ul.write_log(file_path,
                     "=============================%s============================" % (str(keshis[keshi][3:])))
        # table_name = keshis[keshi]
        for ratio in ratios[:3]:
            start_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            print "start_time_:", start_time
            original_diversity, two_diversity, greedy2_diversity, swap2_diversity, dum_diversity, mmr_diversity, vns_diversity= caculate_for_diversity(
                keshis[keshi], ratio, 0.0004, top_k, greedy_Lambda=0.6)
            end_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            print "end_time_:", end_time
            ul.write_log(file_path, ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            ratio, original_diversity, two_diversity,greedy2_diversity,swap2_diversity,dum_diversity, mmr_diversity, vns_diversity)))
            # li = [ratio, original_diversity,greedy2_diversity,dum_diversity,two_diversity,swap2_diversity, vns_diversity,mmr_diversity]
            li = [ratio, original_diversity, greedy2_diversity, dum_diversity, two_diversity,
                  swap2_diversity, mmr_diversity, vns_diversity]
            content_matrix.append(li)
        # exu.write_into(title_list, content_matrix, excel_path)

def get_doc_info_list_m(doc_info_matrix):
    li = []
    for value in doc_info_matrix.values():
        li.append(value)
    return li

if __name__ == '__main__':
    keshis = ["tp_内分泌科","tp_神经内科"]

    start_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    print "start_time:", start_time
    start_sys_diversity(keshis, 20)
    end_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    print "end_time:", end_time
    # if keshis[0][3:] == '神经内科':
    #     print "yes"
