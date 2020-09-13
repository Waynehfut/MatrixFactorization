# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:57:03 2017

@author: Administrator
"""
from __future__ import division
import numpy as np
import doc_matrix as dm
import figure
import doctor_dis as dsu
import disease_dis as dsv
import matplotlib.pyplot as plt
import log

X = []
Y = []
asv = []
asu = []
judge_uv = [0, 0]
"""
矩阵分解
"""


def matrix_factorization(C, U, V, lamdas, steps, alpha, beta, simlamda, lr, sk, table_name):
    global X
    global Y
    global asv
    global asu
    global judge_uv
    X = []
    Y = []
    asv = []
    asu = []
    judge_uv = [0, 0]


    # log.start_log()
    f = log.write_log()
    step = 0
    loss1, def_v, all_sim_u, all_sim_v = getloss(C, U, V, alpha, beta, lamdas, sk, table_name, simlamda)
    print 'loss1:', loss1
    while step <= steps:
        print "开始"
        # print >> f, 'step:', step
        U, V = gardient(C, U, V, def_v, all_sim_u, all_sim_v, alpha, beta, lamdas, lr)
        loss2, def_v, all_sim_u, all_sim_v = getloss(C, U, V, alpha, beta, lamdas, sk, table_name, simlamda)
        # 用于显示梯度下降的效果
        if (step > 100):
            X.append(step)
            Y.append(loss2)
        # print "X:", X
        # print "Y:", Y
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
    # print '完成！！！！！！！！！！！'
    TT = np.dot(U, V.transpose())
    print >> f, '======================================================'
    print >> f, '迭代次数(step):', step - 1
    print >> f, "loss:", loss2
    # print >> f, TT
    return TT,X,Y,loss2


"""
显示梯度下降情况
"""


def showgard(title, file_path):
    global X
    global Y
    print "图"
    figure.paint1(X, Y, title, file_path)


"""
梯度下降
"""


def gardient(C, U, V, def_v, all_sim_u, all_sim_v, alpha, beta, lamdas, lr):
    # C, U, V, dif_v, all_sim_u, all_sim_v, alpha, beta, lamdas, lr
    # C, U, V, dif_v, all_sim_v, beta, lamdas, lr
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
                V[j] = V[j] - lr * (beta * all_sim_v[j] + lamdas[1] * tempv[j])
                # V[j] = V[j] - lr * lamdas[1] * tempv[j]
        sj = 1
        U[i] = U[i] - lr * (alpha * all_sim_u[i] + lamdas[0] * tempu[i])
        # U[i] = U[i] - lr * lamdas[0] * tempu[i]
    return U, V


"""
损失函数
"""


def getloss(C, U, V, alpha, beta, lamdas, sk, table_name, simlamda):
    # f = log.write_log()

    # C, U, V, alpha, beta, lamdas, sk, table_name, simlamda
    global asu
    global asv
    global judge_uv
    # 公式二三部分所需
    all_sim_v = []
    all_sim_u = []

    loss = 0
    dia = C.shape
    dj = dia[1]  # 列
    di = dia[0]  # 行
    def_v = [[0 for ki in range(dj)] for kj in range(di)]
    # sj用来判断是否执行Sim_V部分的计算
    sj = 0
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
            # 误差公式第三部分,simlamda为疾病相似度中公式的参数
            if sj == 0:
                if (judge_uv[1] == 0):
                    Sim_v = dsv.getTopSim_v(simlamda, j, sk, table_name)
                    asv.append(Sim_v)
                else:
                    Sim_v = asv[j]
                tempv = 0.0
                for svi in range(len(Sim_v)):
                    # tv = Sim_v[svi][1] * np.linalg.norm((V[j] - V[Sim_v[svi][0]]))
                    tempv = tempv + Sim_v[svi][1] * (V[j] - V[Sim_v[svi][0]])
                    # print "Sim_v[svi][1]:", Sim_v[svi][1]
                    # print "V[j]:", V[j]
                    # print "V[Sim_v[svi][0]]",V[Sim_v[svi][0]]
                    # print "np.linalg.norm((V[j] - V[Sim_v[svi][0]])):", np.linalg.norm((V[j] - V[Sim_v[svi][0]]))
                    t1 = 0.5 * beta * Sim_v[svi][1] * np.linalg.norm((V[j] - V[Sim_v[svi][0]]))
                    loss = loss + t1
                    # print "0.5 * beta * Sim_v[svi][1] * np.linalg.norm((V[j] - V[Sim_v[svi][0]])):", t1
                all_sim_v.append(tempv)
        # 误差公式第二部分
        if (judge_uv[0] == 0):
            Sim_u = dsu.getTopSim_u(table_name, i, sk)
            asu.append(Sim_u)
        else:
            Sim_u = asu[i]
        for sui in range(len(Sim_u)):
            # tu = Sim_u[sui][1] * np.linalg.norm((U[i]-U[Sim_u[sui][0]]))
            tempu = tempu + Sim_u[sui][1] * (U[i] - U[Sim_u[sui][0]])
            t2 = 0.5 * alpha * Sim_u[sui][1] * np.linalg.norm((U[i] - U[Sim_u[sui][0]]))
            loss = loss + t2
            # print "Sim_v[svi][1]:", Sim_v[svi][1]
            # if U[i][0] == U[Sim_u[sui][0]][0]:
                # print "U[i]:", U[i]
                # print "U[Sim_u[sui][0]]", U[Sim_u[sui][0]]
            # print "U[i]:", U[i]
            # print "U[Sim_u[sui][0]]",U[Sim_u[sui][0]]
            # print "0.5 * alpha * Sim_u[sui][1] * np.linalg.norm((U[i]-U[Sim_u[sui][0]])):",t2
        all_sim_u.append(tempu)
        sj = 1
        judge_uv[1] = 1
    judge_uv[0] = 1
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
    return loss, def_v, all_sim_u, all_sim_v


"""
计算矩阵中所有行的二范式的和
"""


def normal_form(uv_mat):
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


if __name__ == '__main__':
    C = dm.getMatrix('tp_风湿科')
    C = np.array(C)
    d = C.shape
    U = np.random.rand(d[0], 13)
    V = np.random.rand(d[1], 13)
    lambdas = [0.02, 0.03]
    matrix_factorization(C, U, V, lambdas, 10000, 0.002, 0.002, 0.001, 0.001, 5, 'tp_风湿科')
    # C, U, V, lamdas, steps, beta, simlamda, lr, sk, table_name
    # C, U, V, lamdas, steps, alpha, beta, simlamda, lr, sk, table_name
