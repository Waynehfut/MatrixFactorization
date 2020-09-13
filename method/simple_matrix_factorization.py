# -*- coding: utf-8 -*-
"""
Created on 2018/1/30 9:30
@file: simple_matrix_factorization.py
@author: Administrator
"""
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import doc_matrix as dm
import figure
import doctor_dis as dsu
import disease_dis as dsv
import matplotlib.pyplot as plt
import tool.ULog as ul
import matrix_factorization as de
import math

judge_uv = [0, 0]

def matrix_factorization(C, U, V, lamdas, steps, lr):
    """
    矩阵分解
    """
    X = []
    Y = []
    asv = []
    asu = []

    log = ul.ULog("../matrix/simple_matrix_factorization/log.txt")
    f = log.get_log()
    step = 0
    loss1, def_v= getloss(C, U, V, lamdas)
    print 'loss1:', loss1
    while step <= steps:
        print "开始"
        # print >> f, 'step:', step
        U, V = gardient(C, U, V, def_v, lamdas, lr)
        loss2, def_v= getloss(C, U, V, lamdas)
        # 用于显示梯度下降的效果
        if (step > 100):
            X.append(step)
            Y.append(loss2)
        print "X:", X
        print "Y:", Y
        # if(step%1000==0 and step>0):
        #     TT = np.dot(U, V.transpose())
        #     print >>f, 'step:', step
        #     print >>f,"loss:",loss2
        #     print >>f, TT
        #     print >>f, '======================================================'
        if (np.abs(loss1 - loss2) < 0.0001 or loss2 < 0.0004):
            print "small"
            break;
        print "loss1:", loss1
        # if(loss1<loss2):
        #     break
        loss1 = loss2
        step = step + 1
        print 'loss2:', loss2
        print "steps:", step
    print "steps:", step - 1
    print '完成！！！！！！！！！！！'
    TT = np.dot(U, V.transpose())
    print >> f, 'step:', step - 1
    print >> f, "loss:", loss2
    # print >> f, TT
    print >> f, '======================================================'
    print >> f, '迭代次数(step):', step
    log.close_log()
    print  "loss:", loss2
    return TT,X,Y,loss2


def showgard(x, y, title, file_path):
    """
    显示梯度下降情况
    """
    print "图"
    figure.paint1(x, y, title, file_path)

def gardient(C, U, V, def_v, lamdas, lr):
    """
    梯度下降
    """
    # C, U, V, dif_v, lamdas, lr
    dia = C.shape
    di = dia[0]
    dj = dia[1]
    # tempu,tempv 临时值
    tempu = np.array(U)
    tempv = np.array(V)
    i = 0
    ii = 0
    j = 0
    # 判断是否计算V[j]部分
    sj = 0
    for i in range(di):
        for j in range(dj):
            # U[i]的梯度下降
            if (C[i][j] > 0):
                U[i] = U[i] + lr * (1 * def_v[i][j] * tempv[j])
            # V[j]的梯度下降
            if (sj == 0):
                for ii in range(di):
                    if (C[ii][j] > 0):
                        V[j] = V[j] + lr * (1 * def_v[ii][j] * tempu[ii])
                # V[j] = V[j] - lr * (beta * all_sim_v[j] + lamdas[1] * tempv[j])
                V[j] = V[j] - lr * lamdas[1] * tempv[j]#原始
        sj = 1
        # U[i] = U[i] - lr * (alpha * all_sim_u[i] + lamdas[0] * tempu[i])
        U[i] = U[i] - lr * lamdas[0] * tempu[i]#原始
    return U, V


def getloss(C, U, V, lamdas):
    """
    损失函数
    """
    # f = log.write_log()

    # C, U, V, lamdas
    # global judge_uv
    # # # 公式二三部分所需
    # # all_sim_v = []
    # # all_sim_u = []

    loss = 0
    dia = C.shape
    dj = dia[1]  # 列
    di = dia[0]  # 行
    def_v = [[0 for ki in range(dj)] for kj in range(di)]
    # # sj用来判断是否执行Sim_V部分的计算
    # sj = 0
    for i in range(di):
        # print >> f, "loss_sum:", loss
        tempu = 0.0
        for j in range(dj):
            # 误差公式第一部分
            def_v[i][j] = C[i][j] - np.dot(U[i], V[j])
            if (C[i][j] > 0):
                # print "0.5 *def_v[i][j]*def_v[i][j]:",0.5 * def_v[i][j]*def_v[i][j]
                loss = loss + 0.5 * def_v[i][j] * def_v[i][j]
                # print >> f, "误差公式第一部分loss:", loss
            # start误差公式第三部分,simlamda为疾病相似度中公式的参数
            # if sj == 0:
            #     if (judge_uv[1] == 0):
            #         Sim_v = dsv.getTopSim_v(simlamda, j, sk, table_name)
            #         asv.append(Sim_v)
            #     else:
            #         Sim_v = asv[j]
            #     tempv = 0.0
            #     for svi in range(len(Sim_v)):
            #         # tv = Sim_v[svi][1] * np.linalg.norm((V[j] - V[Sim_v[svi][0]]))
            #         tempv = tempv + Sim_v[svi][1] * (V[j] - V[Sim_v[svi][0]])
            #         t1 = 0.5 * beta * Sim_v[svi][1] * np.linalg.norm((V[j] - V[Sim_v[svi][0]]))
            #         loss = loss + t1
            #     all_sim_v.append(tempv)
            # end误差公式第三部分
        # start误差公式第二部分
        # if (judge_uv[0] == 0):
        #     Sim_u = dsu.getTopSim_u(table_name, i, sk)
        #     asu.append(Sim_u)
        # else:
        #     Sim_u = asu[i]
        # for sui in range(len(Sim_u)):
        #     # tu = Sim_u[sui][1] * np.linalg.norm((U[i]-U[Sim_u[sui][0]]))
        #     tempu = tempu + Sim_u[sui][1] * (U[i] - U[Sim_u[sui][0]])
        #     t2 = 0.5 * alpha * Sim_u[sui][1] * np.linalg.norm((U[i] - U[Sim_u[sui][0]]))
        #     loss = loss + t2
        # all_sim_u.append(tempu)
        # end误差公式第二部分
    #     sj = 1
    #     judge_uv[1] = 1
    # judge_uv[0] = 1

    # 误差公式第四部分
    # loss = loss + 0.5 * lamdas[0] * np.square(np.linalg.norm(U))
    t3 = 0.5 * lamdas[0] * normal_form(U)
    loss = loss + t3
    # print >> f, "0.5 * lamdas[0] * normal_form(U)", t3
    # 误差公式第五部分
    t4 = 0.5 * lamdas[1] * normal_form(V)
    loss = loss + t4
    # print >> f, "0.5 * lamdas[1] * normal_form(V)", t4
    # print >> f, "=========================================================="
    return loss, def_v


def normal_form(uv_mat):
    """
    计算矩阵中所有行的二范式的和
    """
    nf_sum = 0.0
    for i in uv_mat:
        # nf_sum += np.square(np.linalg.norm(uv_mat))
        nf_sum += np.linalg.norm(uv_mat)
    return nf_sum


def norma_matrix(m, o):
    """
    将矩阵中小于0的数变为0，对原始矩阵进行填充的矩阵
    :param m:预测矩阵
    :param o:原始矩阵
    :return: 第一个返回的是变0的，第二个返回的是原先矩阵进行填充的矩阵 ,第三个代表预测的值为负数的个数
    """
    num = 0
    matrix0 = np.array(m)
    for i in range(len(matrix0)):
        for j in range(len(matrix0[0])):
            if (matrix0[i][j] < 0):
                matrix0[i][j] = 0
                num += 1
            if (o[i][j] == 0):
                o[i][j] = matrix0[i][j]
    return matrix0, o,num


def validate(t,original_matrix,changed_zero):
    """
    验证矩阵预测的准确性,计算RMSE，MAE
    """
    #原始矩阵
    ma = original_matrix
    #改变过值在矩阵中的位置[[i,j]]
    cma = changed_zero
    num = len(cma)
    print "cma",cma
    dif = []
    var = 0
    for k in cma:
        if(t[k[0]][k[1]]<=0):
            num -=1
        else:
            dif.append(math.fabs(ma[k[0]][k[1]] - t[k[0]][k[1]]))
    #平均绝对误差
    MAE = sum(dif)/num
    #均方根误差/标准差
    RMSE = math.sqrt(sum(map(sf,dif))/num)
    return MAE,RMSE

def sf(x):
    return x*x

def start_simple_matrix_factorization():
    # keshis = ["内分泌科", "神经内科", "神经外科", "泌尿外科"]
    keshis = ["内分泌科", "神经内科"]
    ratios = ['0.50', '0.55', '0.60', '0.65', '0.70', '0.75', '0.80', '0.85', '0.90',
              '0.95']
    file_path = "../matrix/simple_matrix_factorization/RMSE_MAE.txt"
    ul.write_log(file_path, "ratio         RMSE           MAE")
    for keshi in keshis:
        ul.write_log(file_path, "=============="+ keshi +"===============")
        keshi = 'tp_' + keshi
        for ratio in ratios:
            C, orignal_matrix, changed_zero = dm.get_matrix_by_exist(keshi,ratio)
            C = np.array(C)
            d = C.shape
            U = np.random.rand(d[0], 5)
            V = np.random.rand(d[1], 5)
            # lambdas = [0.005, 0.005]
            lambdas = [0.05, 0.001]
            matrix, x, y, loss = matrix_factorization(C, U, V, lambdas, 3000,0.005)
            print "开始验证"
            matrix0, pre_or_mat, num = de.norma_matrix(matrix, orignal_matrix)
            MAE, RMSE = validate(matrix, orignal_matrix, changed_zero)
            # print ("验证结果为:MAE:%15s  RMSE:%15s" % (str(MAE), str(RMSE)))
            ul.write_log(file_path,('%s   %20s   %20s' % (ratio,RMSE,MAE)))

if __name__ == '__main__':

    # C, U, V, lamdas, steps, beta, simlamda, lr, sk, table_name
    # C, U, V, lamdas, steps, alpha, beta, simlamda, lr, sk, table_name
    start_simple_matrix_factorization()
