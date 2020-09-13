# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:57:03 2017

@author: Administrator
"""
from __future__ import division
from disease_dis import getTopSim_v
from doctor_dis import getTopSim_u
import numpy as np
import figure
import matplotlib.pyplot as plt
import log
X = []
Y = []
"""
矩阵分解
"""
def matrix_factorization(C, U, V, alpha, beta, lamdas, steps, lr,sk):
    global X
    global Y
    X = []
    Y = []
    f = log.write_log()
    step = 0
    loss1, def_v, all_sim_u, all_sim_v = getloss(C, U, V, alpha, beta, lamdas,sk)
    while step<=steps:
        U, V = gardient(C, U, V, def_v, all_sim_u, all_sim_v, alpha, beta, lamdas, lr)
        loss2, def_v, all_sim_u, all_sim_v = getloss(C, U, V, alpha, beta, lamdas,sk)
        #用于显示梯度下降的效果
        X.append(step)
        Y.append(loss2)
        if(step%250==0):
            figure.paint1(X,Y)
            print >>f,'loss:',loss1
        if(loss1-loss2<0.001):
            break;
        loss1 = loss2
        step = step +1
"""
梯度下降
"""
def gardient(C, U, V, dif_v, all_sim_u, all_sim_v, alpha, beta, lamdas, lr):
    dia = C.shape
    di = dia[0]
    dj = dia[1]
    # tempu,tempv 临时值
    tempu = U
    tempv = V
    i = 0
    ii = 0
    j = 0
    #判断是否计算V[j]部分
    sj = 0
    for i in range(di):
        for j in range(dj):
            #U[i]的梯度下降
            if(C[i][j]!=0):
                U[i] = U[i] + lr * (1 * dif_v[i][j] * tempv[j])
            # V[j]的梯度下降
            if (sj == 0):
                for ii in range(di):
                    if (C[ii][j] != 0):
                        V[j] = V[j] + lr * (1 * dif_v[ii][j] * tempu[ii])
                V[j] = V[j] - lr * (beta * all_sim_v[j] + lamdas[1] * tempv[j])
        U[i] = U[i] - lr * (alpha * all_sim_u[i] + lamdas[0] * tempu[i])
        sj == 1
    return U,V

"""
损失函数
"""
def getloss(C, U, V, alpha, beta, lamdas,sk,table_name,simlamda):
    loss = 0
    all_sim_u = []
    all_sim_v = []
    #tu,tv,tempu,tempv用于存储临时的数据
    tu = 0
    tv = 0
    tempu = 0
    tempv = 0

    dia = C.shape
    dj = dia[1]#列
    di = dia[0]#行
    dif_v = [[0 for ki in range(dj)] for kj in range(di)]
#sj用来判断是否执行Sim_V部分的计算
    sj = 0
    for i in range(di):
        for j in range(dj):
            # 误差公式第一部分
            dif_v[i][j] = C[i][j]-np.dot(U[i], V[j])
            if(C[i][j]!=0):
                loss = loss + 0.5 * np.square(dif_v[i][j])
            # 误差公式第三部分
            if sj == 0:
                Sim_v = getTopSim_v(simlamda,j, sk,table_name)
                for svi in range(len(Sim_v)):
                    tv = Sim_v[svi][1] * np.linalg.norm((V[j] - V[Sim_v[svi][0]]))
                    tempv = tempv + tv
                    loss = loss + 0.5 * beta * tv
                all_sim_v.append(tempv)
        # 误差公式第二部分
        Sim_u = getTopSim_u(i,sk)
        for sui in range(len(Sim_u)):
            tu = Sim_u[sui][1] * np.linalg.norm((U[i]-U[Sim_u[sui][0]]))
            tempu = tempu + tu
            loss = loss + 0.5 * alpha * tu
        all_sim_u.append(tempu)
        sj = 1
    # 误差公式第四部分
    loss = loss + 0.5 * lamdas[0] * np.square(np.linalg.norm(U))
    # 误差公式第五部分
    loss = loss + 0.5 * lamdas[1] * np.square(np.linalg.norm(V))
    return loss,dif_v,all_sim_u,all_sim_v

