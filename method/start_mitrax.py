# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:57:03 2017

@author: Administrator
"""
from __future__ import division
from tool.math_method import get_sim_matrix
import matrix_factorization as de
import doctor_var as dv
import numpy as np
import doc_matrix as dm
import validator as vali
import time
import log
import threadpool
import figure as fig
import tool.readtxt as dealtxt
import greedy_algorithm as greedy
import recommend_diversity as re_div
import tool.math_method as mathn
import figure
import simple_matrix_factorization as simple_mat
import tool.ULog as ul


def getresult(l, table_name, lambdas, ab, simlambda, lr, step, sim_k, ratio):
    MAE = 0
    RMSE = 0
    alpha = ab[0]
    beta = ab[1]
    start_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    log.start_log(start_time,
                  "../matrix/" + table_name.decode('utf-8') + "/" + "矩阵分解结果.txt".decode('utf-8'))
    f = log.write_log()

    lc_table_name = 'lc_' + table_name
    tp_table_name = 'tp_' + table_name
    # start预测部分
    # # 得到的矩阵是挖取过值的矩阵
    # C, original_matrix, changed_zero = dm.getMatrix(tp_table_name, ratio)
    C, original_matrix, changed_zero = dm.get_Matrix_from_lc_tp(lc_table_name, tp_table_name, ratio, 1)
    # C = np.array(C)
    d = C.shape
    U = np.random.rand(d[0], l)
    V = np.random.rand(d[1], l)
    print "开始矩阵分解"
    matrix, X, Y, loss = de.matrix_factorization(C, U, V, lambdas, step, alpha, beta, simlambda, lr, sim_k,
                                                 tp_table_name)
    # 开始验证
    print "开始验证"
    matrix0, pre_or_mat, num = de.norma_matrix(matrix, original_matrix)
    MAE, RMSE = vali.validate(matrix, original_matrix, changed_zero)
    # #end
    # end预测部分

    file_path = "../matrix/" + table_name.decode('utf-8')
    t = str(ratio) + "_" + str(num) + "_" + start_time + ".txt"
    # start将矩阵分解后的矩阵保存
    np.savetxt(file_path + "/matrix_factorization/matrix_factorization_" + str(ratio) + ".txt",
               matrix, fmt='%.8f')
    # end将矩阵分解后的矩阵保存
    # start将原矩阵经预测填充后的矩阵保存
    # filematrix0 = open(file_path + "/result/pre_" + str(ratio) + "." + "txt", 'w');
    # filematrix0.close()
    np.savetxt(file_path + "/result/pre_" + str(ratio) + ".txt", pre_or_mat, fmt='%.8f')
    # end 将原矩阵经预测填充后的矩阵保存
    # start将矩阵分解后的矩阵(处理过的，负数变0)保存
    # filematrix1 = open(file_path + "/out/" + t.decode('utf-8'), 'w');
    # filematrix1.close()
    np.savetxt(file_path + "/out/" + t.decode('utf-8'), matrix0, fmt='%.8f')
    # end 将矩阵分解后的矩阵(处理过的，负数变0)保存
    # end


    # k, disease, mitrax, table_name
    # top_k = dv.getTopK(k, disease, matrix, table_name)
    # 筛选医院，得到与目标人物处在同一个城市的医院
    # pre_top = dv.pre_data(top_k)
    # 筛选医院
    # matrix = dealtxt.load_file_to_array("../matrix/" + table_name.decode('utf-8') + "/result/pre_" + str(ratio) + ".txt");
    # filter_hos = dv.filter_hos_By_sorted100(table_name,matrix,disease,people_locat)
    # dv.getResult(pre_top,disease)
    # dv.getResult1(disease,matrix,table_name,city,people_locat)
    end_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    print >> f, "开始时间：", start_time
    print >> f, "结束时间：", end_time
    # 显示梯度下降情况
    title = 'lr:{0} alpha:{1} beta:{2} step:{3} lambdas:{4} sim:{5} sim_k:{6}'
    title = title.format(lr, ab[0], ab[1], step, lambdas, simlambda, sim_k)
    print >> f, "参数：", title
    figure_path = "../matrix/" + table_name.decode('utf-8') + "/figure/" + str(ratio) + "_" + end_time + ".jpg"
    figure.paint1(X, Y, title, figure_path)
    log.close_log()
    return MAE, RMSE, loss

def getresult_lc_or_tp(l, table_name, lambdas, ab, simlambda, lr, step, sim_k, ratio):
    MAE = 0
    RMSE = 0
    alpha = ab[0]
    beta = ab[1]
    start_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    log.start_log(start_time,
                  "../matrix/" + table_name[3:].decode('utf-8') + "/" + "矩阵分解结果.txt".decode('utf-8'))
    f = log.write_log()

    # start预测部分
    # # 得到的矩阵是挖取过值的矩阵
    C, original_matrix, changed_zero = dm.getMatrix(table_name, ratio,1)
    # C, original_matrix, changed_zero = dm.get_Matrix_from_lc_tp(lc_table_name, tp_table_name, ratio, 1)
    # C = np.array(C)
    d = C.shape
    U = np.random.rand(d[0], l)
    V = np.random.rand(d[1], l)
    print "开始矩阵分解"
    matrix, X, Y, loss = de.matrix_factorization(C, U, V, lambdas, step, alpha, beta, simlambda, lr, sim_k,
                                                 table_name)
    # 开始验证
    print "开始验证"
    matrix0, pre_or_mat, num = de.norma_matrix(matrix, original_matrix)
    MAE, RMSE = vali.validate(matrix, original_matrix, changed_zero)
    # #end
    # end预测部分

    file_path = "../matrix/" + table_name[3:].decode('utf-8')
    t = str(ratio) + "_" + str(num) + "_" + start_time + ".txt"
    # start将矩阵分解后的矩阵保存
    np.savetxt(file_path + "/matrix_factorization/matrix_factorization_" + str(ratio) + ".txt",
               matrix, fmt='%.8f')
    # end将矩阵分解后的矩阵保存
    # start将原矩阵经预测填充后的矩阵保存
    # filematrix0 = open(file_path + "/result/pre_" + str(ratio) + "." + "txt", 'w');
    # filematrix0.close()
    np.savetxt(file_path + "/result/pre_" + str(ratio) + ".txt", pre_or_mat, fmt='%.8f')
    # end 将原矩阵经预测填充后的矩阵保存
    # start将矩阵分解后的矩阵(处理过的，负数变0)保存
    # filematrix1 = open(file_path + "/out/" + t.decode('utf-8'), 'w');
    # filematrix1.close()
    np.savetxt(file_path + "/out/" + t.decode('utf-8'), matrix0, fmt='%.8f')
    end_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    print >> f, "开始时间：", start_time
    print >> f, "结束时间：", end_time
    # 显示梯度下降情况
    title = 'lr:{0} alpha:{1} beta:{2} step:{3} lambdas:{4} sim:{5} sim_k:{6}'
    title = title.format(lr, ab[0], ab[1], step, lambdas, simlambda, sim_k)
    print >> f, "参数：", title
    figure_path = "../matrix/" + table_name[3:].decode('utf-8') + "/figure/" + str(ratio) + "_" + end_time + ".jpg"
    figure.paint1(X, Y, title, figure_path)
    log.close_log()
    return MAE, RMSE, loss

def inputMatrix(or_matrix, pre_matrix):
    i = 0
    j = 0
    iter_file = iter(or_matrix);
    for line in iter_file:
        for ls in line.strip('\n').split(" "):
            if ls == 0:
                or_matrix = pre_matrix[i][j]
            j += 1
        i += 1
        j = 0
    return or_matrix


def inputPre(or_matrix, pre_matrix):
    i = 0
    j = 0
    iter_file = iter(or_matrix);
    for line in iter_file:
        for ls in line.strip('\n').split(" "):
            if ls == 0:
                or_matrix = pre_matrix[i][j]
            j += 1
        i += 1
        j = 0
    return or_matrix


def startE():
    ratios = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    pool = threadpool.ThreadPool(1)
    requests = threadpool.makeRequests(start_matrix, ratios)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    print "finish!!!!"


def start_matrix(l, ratio, alpha, beta, lambda_u, lambda_v, simlambda, learn_rate, table_name, sim_k, step =5000):
    # time.sleep(180)
    # step = 6000
    lr = learn_rate
    # simlambda = g
    # alpha,beta
    ab = [alpha, beta]
    # ab = [0, 0]
    lambdas = [lambda_u, lambda_v]
    #融合的
    # MAE, RMSE, loss = getresult(l, table_name, lambdas, ab, simlambda, lr, step, sim_k, ratio)
    #lc 或者是 tp
    MAE, RMSE, loss = getresult_lc_or_tp(l, table_name, lambdas, ab, simlambda, lr, step, sim_k, ratio)
    return MAE, RMSE, loss


def start_sample_matrix(ratio, lambdas, lr, table_name, l):
    MAE = 0
    RMSE = 0
    start_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    log.start_log(start_time,
                  "../matrix/" + table_name.decode('utf-8') + "/" + "MF矩阵分解结果.txt".decode('utf-8'))
    f = log.write_log()

    lc_table_name = 'lc_' + table_name
    tp_table_name = 'tp_' + table_name
    # start预测部分
    # # 得到的矩阵是挖取过值的矩阵
    # C, original_matrix, changed_zero = dm.getMatrix(table_name, ratio)
    C, original_matrix, changed_zero = dm.get_Matrix_from_lc_tp(lc_table_name, tp_table_name, ratio, 1)
    # C = np.array(C)
    d = C.shape
    U = np.random.rand(d[0], l)
    V = np.random.rand(d[1], l)
    print "开始矩阵分解"
    matrix, X, Y = simple_mat.matrix_factorization(C, U, V, lambdas, step, lr)
    # 开始验证
    print "开始验证"
    matrix0, pre_or_mat, num = de.norma_matrix(matrix, original_matrix)
    MAE, RMSE = vali.validate(matrix, original_matrix, changed_zero)
    # #end
    # end预测部分
    file_path = "../matrix/" + table_name.decode('utf-8')
    t = str(ratio) + "_" + str(num) + "_" + start_time + ".txt"
    # start将矩阵分解后的矩阵保存
    np.savetxt(file_path + "/matrix_factorization/MF_matrix_factorization_" + str(ratio) + ".txt",
               matrix, fmt='%.8f')
    # end将矩阵分解后的矩阵保存
    # start将原矩阵经预测填充后的矩阵保存
    np.savetxt(file_path + "/result/MF_pre_" + str(ratio) + ".txt", pre_or_mat, fmt='%.8f')
    # end 将原矩阵经预测填充后的矩阵保存
    # start将矩阵分解后的矩阵(处理过的，负数变0)保存
    np.savetxt(file_path + "/out/MF_" + t.decode('utf-8'), matrix0, fmt='%.8f')
    # end 将矩阵分解后的矩阵(处理过的，负数变0)保存
    # end
    end_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    print >> f, "开始时间：", start_time
    print >> f, "结束时间：", end_time
    # 显示梯度下降情况
    title = 'lr:{0} alpha:{1} beta:{2} step:{3} lambdas:{4} sim:{5}'
    title = title.format(lr, ab[0], ab[1], step, lambdas, simlambda)
    print >> f, "参数：", title
    figure_path = "../matrix/" + table_name.decode('utf-8') + "/figure/MF_" + str(ratio) + "_" + start_time + ".jpg"
    figure.paint1(X, Y, title, figure_path)
    log.close_log()
    return MAE, RMSE


def stratFor():
    ratios = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]

    pool = threadpool.ThreadPool(1)
    requests = threadpool.makeRequests(start_matrix, ratios[0:5])
    [pool.putRequest(req) for req in requests]
    pool.wait()
    print "finish!!!!"


def start_optimize_parameter(keshi):
    """
    参数调优
    :return:
    """
    # 调参start
    file_path = "../matrix/optimize_parameters_log.txt"
    f = open("../matrix/optimize_parameters.txt", 'a')
    print >> f, "开始"
    learn_rate = 0.005
    alphas = [0.005, 0.01, 0.05, 0.1]  # 以去掉0.01
    betas = [0.005, 0.01, 0.05, 0.1]
    # lambdas = [0.001, 0.005, 0.01, 0.05, 0.1, 0.25, 0.5]
    lambdas_u = [0.001, 0.005, 0.01, 0.05]
    lambdas_v = [0.001, 0.005, 0.01, 0.05]
    # simlambdas = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1]
    simlambdas = [0.001, 0.005]
    k = [15]
    lis = []
    rm_loss = 0
    min_RMSE = 20
    min_MAE = 0
    min_alpha = 0
    min_beta = 0
    min_simlambdas = 0
    min_lambda_u = 0
    min_lambda_v = 0

    min_loss = 10000
    loss_RMSE = 20
    loss_MAE = 0
    loss_alpha = 0
    loss_beta = 0
    loss_simlambdas = 0
    loss_lambda_u = 0
    loss_lambda_v = 0
    num = 0
    for alpha in alphas:
        for beta in betas:
            for u in lambdas_u:
                for v in lambdas_v:
                    for sim in simlambdas:
                        if num <= 226:
                            # print (
                            #     "k:%5s  alpha%5s  beta:%5s  lambda_u:%5s  lambda_v:%5s simlambdas:%5s" % (
                            #         k[0], alpha, beta, u, v, sim))
                            pass
                        else:
                            # ratio = 0.75
                            print >> f, "=========================================="
                            print ("第%s次" % num)
                            MAE, RMSE, loss = start_matrix(5, '0.75', alpha, beta, u, v, sim, learn_rate, keshi,
                                                           sim_k=15)
                            ul.write_log(file_path, ("第%s次" % num))
                            print >> f, "LOSS:", loss
                            print >> f, ("MAE:%15s  RMSE:%15s" % (str(MAE), str(RMSE)))
                            print >> f, (
                            "k:%5s  alpha%5s  beta:%5s  lambda_u:%5s  lambda_v:%5s simlambdas:%5s" % (
                                k[0], alpha, beta, u, v, sim))
                            print >> f, "=========================================="
                            if (min_RMSE > RMSE):
                                rm_loss = loss
                                min_RMSE = RMSE
                                min_MAE = MAE
                                min_alpha = alpha
                                min_beta = beta
                                min_lambda_u = u
                                min_lambda_v = v
                                min_simlambdas = sim
                            if (min_loss > loss):
                                min_loss = loss
                                loss_RMSE = RMSE
                                loss_MAE = MAE
                                loss_alpha = alpha
                                loss_beta = beta
                                loss_lambda_u = u
                                loss_lambda_v = v
                                loss_simlambdas = sim
                        num += 1
    print >> f, ("rm_loss: %15s" % str(rm_loss))
    print >> f, ("min: MAE:%15s  RMSE:%15s" % (str(min_MAE), str(min_RMSE)))
    print ("min: MAE:%15s  RMSE:%15s" % (str(min_MAE), str(min_RMSE)))
    print >> f, ("k:%10s  alpha%10s  beta:%10s  lambda_u:%10s  lambda_v:%10s simlambdas:%10s" % (
    k[0], min_alpha, min_beta, min_lambda_u, min_lambda_v, min_simlambdas))
    print >> f, ("min_loss: %15s" % str(min_loss))
    print >> f, ("min: loss_MAE:%15s  loss_RMSE:%15s" % (str(loss_RMSE), str(loss_MAE)))
    print ("min: loss_MAE:%15s  loss_RMSE:%15s" % (str(loss_RMSE), str(loss_MAE)))
    print >> f, ("=loss=: k:%10s  alpha%10s  beta:%10s  lambda_u:%10s  lambda_v:%10s simlambdas:%10s" % (
    k[0], loss_alpha, loss_beta, loss_lambda_u, loss_lambda_v, loss_simlambdas))
    f.close()
    # end调参结束


def pre_accuracy():
    # start MAE,RMSE
    # keshis = ["内分泌科","神经内科","神经外科","泌尿外科"]
    # keshis = ["lc_内分泌科","lc_神经内科"]
    keshis = ["tp_内分泌科"]
    # ratios = ['0.05', '0.10', '0.15', '0.20', '0.25', '0.30', '0.35', '0.40', '0.45', '0.50', '0.55', '0.60', '0.65', '0.70', '0.75', '0.80', '0.85', '0.90',
    #               '0.95']
    ratios = ['0.50', '0.55', '0.60', '0.65', '0.70', '0.75', '0.80', '0.85', '0.90',
              '0.95']
    f = open("../matrix/RMSE_MAE.txt", 'a')
    print >> f, ("%-20s%-20s%-20s" % ('ratio', "RMSE", "MAE"))
    ul.write_log("../matrix/reRMSE_MAE.txt", ("%-20s%-20s%-20s" % ('ratio', "RMSE", "MAE")))
    for keshi in range(len(keshis)):
        ul.write_log("../matrix/reRMSE_MAE.txt", ("=====================%s===================" % (str(keshis[keshi]))))
        print >> f, ("=====================%s===================" % (str(keshis[keshi])))
        for i in range(len(ratios)):
            MAE1, RMSE1, loss = start_matrix(5, ratios[i], 0.5, 0.5, 0.005, 0.005, 0.001, 0.005, keshis[keshi],
                                             sim_k=15)
            # MAE1, RMSE1, loss = start_matrix(5, ratios[i], 0.5, 0.5, 0.01, 0.05, 0.001, 0.004, keshis[keshi],
            #                                  sim_k=15)
            # MAE1, RMSE1, loss = start_matrix(5, ratios[i], 0.005, 0.005, 0.05, 0.001, 0.001, 0.01, keshis[keshi],
            #                                  sim_k=15)
            print "rate:", ratios[i]
            print "loss:", loss
            ul.write_log("../matrix/reRMSE_MAE.txt",("%-20s%-20s%-20s" % (ratios[i], RMSE1, MAE1)))
            print >> f, ("%-20s%-20s%-20s" % (ratios[i], RMSE1, MAE1))
            # print "rate:",i
            # MAE1, RMSE1 = start_matrix(5, i, 0.5, 0.005, 0.001, 0.004, keshis[keshi],sim_k=15)
            # MAE1, RMSE1 = start_sample_matrix(i, 0.005, 0.004, keshis[keshi], 5)
            # print >> f, ("%-20s%-20s%-20s" % (i, RMSE1, MAE1))

            # MAE1, RMSE1 = start_matrix(i, 0.5, 0.005, 0.001)
            # MAE1, RMSE1 = start_matrix(i, 0.25, 0.05, 0.01)
            # l, ratio, a, b, g, learn_rate, topk, table_name, sk)
            # MAE1, RMSE1 = start_matrix(5, i, 0.5, 0.005, 0.001, 0.004, keshis[keshi],sim_k=15)
            # MAE1, RMSE1 = start_sample_matrix(i, 0.005, 0.004, keshis[keshi], 5)
            # print >> f, ("%-20s%-20s%-20s" % (i, RMSE1, MAE1))
    f.close()
    # #end


def caculate_for_diversity(table_name, ratio, r=0.0004, top_k=20):
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
    one_list = []
    one_list_matrix_index = []
    two_list = []
    two_list_matrix_index = []

    for chosen_disease in diseases[:3]:
        un_peoples = mathn.get_random_sort(peoples)
        for chosen_people in un_peoples[:3]:
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
            # # 阈值
            # r = 0.0004
            # # top_k
            # top_k = 20
            print "ls_sort数量:", len(ls_sort)
            recommend_list_one, recommend_list_one_index = greedy.greedy_one(ls_sort, doc_info, doc_id_dict, sim_matrix, r, top_k)
            one_list.append(recommend_list_one)
            one_list_matrix_index.append(recommend_list_one_index)
            print "two====================================two"
            recommend_list_two, recommend_list_two_index = greedy.greedy_two(ls_sort, doc_info, doc_id_dict, sim_matrix, r, top_k)
            two_list.append(recommend_list_two)
            two_list_matrix_index.append(recommend_list_two_index)
            print "MMR====================================MMR"
            recommend_list_two, recommend_list_two_index = MMR(doc_info,doc_id_dict, sim_matrix,0.6,top_k)
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
    np.savetxt("../matrix/" + table_name[3:].decode('utf-8') + "/one_recommend_" + str(ratio) + ".txt",
               np.array(one_list, dtype=int),
               fmt='%d')
    np.savetxt("../matrix/" + table_name[3:].decode('utf-8') + "/one_recommend_matrix_index_" + str(ratio) + ".txt",
               np.array(one_list_matrix_index, dtype=int),
               fmt='%d')
    np.savetxt("../matrix/" + table_name[3:].decode('utf-8') + "/two_recommend_" + str(ratio) + ".txt",
               np.array(two_list, dtype=int),
               fmt='%d')
    np.savetxt("../matrix/" + table_name[3:].decode('utf-8') + "/two_recommend_matrix_index_" + str(ratio) + ".txt",
               np.array(two_list_matrix_index, dtype=int),
               fmt='%d')
    start_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    one_diversity = system_diversity(one_list_matrix_index, table_name)
    two_diversity = system_diversity(two_list_matrix_index, table_name)

    log.start_log(start_time,
                  "../matrix/" + table_name[3:].decode('utf-8') + "/" + "推荐排序结果.txt".decode('utf-8'))
    f = log.write_log()
    print >> f, "recommend_list_one:", recommend_list_one
    for i in range(len(recommend_list_one)):
        # print "int(recommend_list[i])",recommend_list_one[i]
        print >> f, ("%-25s%-25s" % (doc_info[int(recommend_list_one[i])][2].encode('utf-8'),
                                     doc_info[int(recommend_list_one[i])][1].encode('utf-8')))
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
    print ("diversity:%-20s%-20s" % (one_diversity, two_diversity))
    print >> f, ("diversity:%-20s%-20s" % (one_diversity,two_diversity))
    log.close_log()
    # end结果输出
    return one_diversity, two_diversity


if __name__ == '__main__':
    # startE()
    # time.sleep(10600)



    # MAE, RMSE = start_matrix(0.05, 0.5, 0.05, 0.001)
    # print MAE,RMSE
    # x = []
    # y1 = []
    # y2 = []
    # tm = [0.1423187982903377, 0.12170930598264713, 0.12436463427452792, 0.1309869519767888, 0.13253821215943046, 0.12660759825166432, 0.12576953619637937, 0.12736417365673083, 0.1090778395738729, 0.1298813180232628, 0.10579509162427145, 0.13181384838182872, 0.11095931836282363, 0.12562845913781553, 0.12751584806768523, 0.1319234158052972, 0.1237583491623371, 0.12646009955992504, 0.11014865511583674]
    # tr = [0.23994886686367817, 0.21161008574895532, 0.22428842780314823, 0.24070659909225633, 0.2319276971516087, 0.2176662824649559, 0.22618426976487302, 0.24166652043407538, 0.17975279069391134, 0.22951380306087574, 0.16253741726093535, 0.2323039019685365, 0.20712475847444747, 0.21951707066312373, 0.2022699423321347, 0.23881708857919892, 0.2394945254365543, 0.2368231740957932, 0.22346351545874465]
    #
    # fig_x = []
    # fig_y = []
    # for i in range(19):
    #     x.append(0.05*(i+1))
    #     MAE1, RMSE1 = start_matrix(0.05*(i+1), 0.5, 0.005, 0.001)
    #     MAE2, RMSE2 = start_matrix(0.05 * (i + 1), 0.5, 0.005, 0.001)
    #     MAE = (MAE1 + MAE2 + tm[i])/3
    #     RMSE = (RMSE1 + RMSE2 + tr[i])/3
    #     y1.append(MAE)
    #     y2.append(RMSE)
    # fig_x.append(x)
    # fig_x.append(x)
    # fig_y.append(y1)
    # fig_y.append(y2)
    # print x
    # print y1
    # print y2
    # fig.paints(fig_x,fig_y,'dig_ratio',"E:/Pycharm_Workspace/lyqystj/matrix/ratio.png",'ratio','value')
    # print "Finish!!!!!!!!!"


    # start 预测排序

    # end

    # f = open('../matrix/' + '神经外科'.decode('utf-8') + "/" + "rel_" + '神经外科'.decode('utf-8')+".txt",'a')
    # ratios = [3,5,8,10,15,20]
    # print >> f, ("%-20s%-20s%-20s" % ('ratio',"RMSE", "MAE"))
    # # MAE1, RMSE1 = start_matrix(0.05 * (5 + 1), 0.5, 0.005, 0.001)
    # # print >> f, ("%-20s%-20s%-20s" % (0.05 * (5 + 1), RMSE1, MAE1))
    # for i in ratios:
    #     if(i>0):
    #         print i
    #         # MAE1, RMSE1 = start_matrix(i, 0.5, 0.005, 0.001)
    #         MAE2, RMSE2 = start_matrix(i, 0.25, 0.05, 0.01)
    #         # MAE1, RMSE1 = start_matrix(i, 0.5, 0.005, 0.001)
    #         print >> f, ("%-20s%-20s%-20s" % (i, (RMSE1+RMSE2)/2, (MAE1+MAE2)/2))
    # f.close()






    # table_name = "tp_内分泌科"
    # disease = '糖尿病'
    # table_name = "tp_泌尿外科"
    # disease = '附睾炎'
    # table_name = "tp_神经外科"  # 174*45
    # disease = '舌咽神经痛'
    # people = '31.817716,117.252518'
    # # # disease = '脑肿瘤'
    # # table_name = "tp_神经内科"
    # # disease = '高血压'
    # step = 6000
    # lr = 0.005
    # simlambda = 0.005#0.001
    # # ab = [0.5, 0.5]#0.1不如0.5
    # ab = [0.002, 0.003]
    # # lambdas = [0.005, 0.005]#0.05 没变化
    # lambdas = [0.125, 0.125]
    # # 取前k个人5, 10, 15, 20
    # sk = 5
    # # 取前k个人5,10,15,20
    # k = 5
    # l = 5  # 之前是13
    # # 挖掉剩余比例
    # ratio = 0.05
    # # C, U, V, lambdas, 10000, 0.002, 0.002, 0.001, 0.001, 5, 'tp_风湿科'
    # getresult(l, disease, table_name, lambdas, ab, simlambda, lr, step, sk, k, people, ratio)
    # start_matrix(0.5, 0.5, 0.005, 0.001)
    # print "全部完成====================="

    # table_name = '内分泌科'
    # step = 5000
    # lr = 0.005
    # simlambda = 0.001  # 0.001
    # ab = [0.5, 0.5]  # 0.1不如0.5
    # # ab = [0.002, 0.003]
    # lambdas = [0.005, 0.005]  # 0.05 没变化
    # # lambdas = [0.125, 0.125]
    # # 取前sk个人5, 10, 15, 20
    # sk = 15
    # # l分别为矩阵U、V的列和行
    # l = 5  # 之前是5
    # # 挖掉剩余比例
    # ratio = '0.80'
    # C, U, V, lambdas, 10000, 0.002, 0.002, 0.001, 0.001, 5, 'tp_风湿科'
    # start_sample_matrix(ratio, lambdas, lr, table_name, l)
    # lr:0.004
    # alpha:0.005
    # beta:0.005
    # step:3000
    # lambdas:[0.01, 0.001]
    # sim:0.001
    # sim_k:15
    # start_matrix(5, '0.75', 0.005, 0.005, 0.01, 0.001, 0.001, 0.005, "神经外科", 15,4000)
    # start_matrix(5, '0.75', 0.005, 0.005, 0.01, 0.001, 0.001, 0.005, "神经外科", 20,4000)



    # # pre_accuracy()
    # start_optimize_parameter('神经外科')
    pre_accuracy()
    # #start多样性
    # #上海交      大，合工大(老区)，
    # people = ['31.031583,121.442614','31.849273,117.302611','40.011006,116.338897']
    # diseases = ['高血压','','']
    # caculate_for_diversity(diseases[0],'tp_神经内科',"40.818264,111.697127",0.65)
    # # print recommend_list
    # # for i in recommend_list:
    # #     print i
    # #end多样性
