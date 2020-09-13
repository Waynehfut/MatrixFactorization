# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:57:03 2017

@author: Administrator
"""
from __future__ import division
import log
import math
import tool.readtxt as rtxt
"""
验证矩阵预测的准确性
"""
def validate(t,original_matrix,changed_zero):
    f = log.write_log()
    #原始矩阵
    ma = original_matrix
    #改变过值在矩阵中的位置[[i,j]]
    cma = changed_zero
    num = len(cma)
    # print "cma",cma
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
    print >>f,"验证结果为"
    print >>f,("MAE:%15s  RMSE:%15s"%(str(MAE),str(RMSE)))
    print ("验证结果为:MAE:%15s  RMSE:%15s" % (str(MAE), str(RMSE)))
    return MAE,RMSE

"""
x平方
"""
def sf(x):
    return x*x
"""
读取txt中的值进行计算
"""
def validate_by_txt(org_filename,pre_filename):
    #原始矩阵
    ma = rtxt.load_file_to_array(org_filename)
    #改变过值的矩阵
    cma = locat()
    #预测出的矩阵
    t = rtxt.load_file_to_array(pre_filename)
    print "cma",cma
    dif = []
    for k in cma:
        dif.append(math.fabs(ma[k[0]][k[1]] - t[k[0]][k[1]]))
    #平均绝对误差
    MAS = sum(dif)/len(cma)
    #均方根误差/标准差
    RMSE = math.sqrt(sum(map(sf,dif))/len(cma))
    print "验证结果为"
    print ("MAE:%15s  RMSE:%15s"%(str(MAS),str(RMSE)))

"""
返回改变的值的位置
"""
def locat():
    changed_zero = []
    changedFile = open("../data/deal_file.txt", "r")
    iter_file = iter(changedFile)
    i = 0
    j = 0
    for line in iter_file:
        for ls in line.strip('\n').split(" "):
            if ls == '-2.0':
                changed_zero.append([i,j])
            j += 1
        i += 1
        j = 0
    return changed_zero

#余弦相似度计算
def cos(vector1,vector2):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a,b in zip(vector1,vector2):
        dot_product += a*b
        normA += a**2
        normB += b**2
    if normA == 0.0 or normB==0.0:
        return None
    else:
        return dot_product / ((normA*normB)**0.5)

if __name__ == "__main__":
    # org_filename = ""
    # pre_filename = ""
    # validate_by_txt(org_filename,pre_filename)
    v1 = [1,2,3,4,5]
    v2 = [2,5,1,3,6]
    print cos(v1, v2)
