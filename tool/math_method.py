# -*- coding: utf-8 -*-
"""
Created on 2017/12/5 21:33
@file: math_method.py
@author: Administrator
"""
from __future__ import division
import numpy as np
import random

def get_sum_by_index(score,i):
    """
    计算二维数组中指定列的总和
    :param score: [[,,...,]]
    :param i: 指定列
    :return: sum
    """
    sum = 0
    for doc in score:
        sum = sum + doc[i]
    return sum


def get_maxormin_by_index(col,i,sort):
    """
    计算二维数组中指定列的最大或最小值，sort:max/min
    :param col: [[,,...,]]
    :param i: 第几列
    :param sort: 选择方法的返回的值 max or min
    :return: max or min
    """
    k = col[0][i]
    if(sort == 'max'):
        for doc in col:
           if(k <= doc[i]):
               k = doc[i]
    else:
        for doc in col:
            if (k >= doc[i]):
                k = doc[i]
    return k


def get_sum_for_list(ls):
    """
    计算医生评分和
    :param docs: array or []
    :return: sum
    """
    sum = 0
    for i in ls:
        sum += i[3]
    return sum

def get_cos_sim(vector1,vector2):
    """
    计算两向量间的余弦相似度
    :param vector1:
    :param vector2:
    :return:
    """
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

def absolute_diversity(matrix):
    """
    计算绝对多样性
    :param matrix:
    :return:
    """
    #生成余弦相似度矩阵
    sim_matrix = get_sim_matrix(matrix)

    # 计算绝对多样性
    n = len(sim_matrix[0])
    sum = 0
    for i in range(n):
        for j in range(n):
            if(i != j):
                sum += (1-sim_matrix[i][j])
    return sum/((n-1)*n)

def get_sim_matrix(matrix):
    """
    生成余弦相似度矩阵
    :param matrix: 以行区分的行向量的组合
    :return: 余弦相似度矩阵
    """
    n,m = matrix.shape
    sim_matrix = np.zeros([n,n])
    for i in range(n):
        for j in range(n):
            sim_matrix[i][j] = get_cos_sim(matrix[i],matrix[j])
    return sim_matrix

def sim_std(matrix,di):
    """
    计算matrix中行与行之间相异性值标准差
    :param matrix:以行区分的行向量的组合
    :param di:绝对多样性
    :return:
    """
    n,m = matrix.shape
    sum = 0
    for i in range(n):
        for j in range(n):
            sum = (get_cos_sim(matrix[i],matrix[j])-di)**2
    sd = (sum/(n*(n-1)))**0.5
    return sd

def get_max_by_index(matrix, index):
    """
    返回矩阵中指定列中的最大值
    :param matrix:
    :param index:指定列序号
    :return:
    """
    li = []
    for row in matrix:
        li.append(row[index])
    return max(li)

def get_min_by_index(matrix, index):
    """
    返回矩阵中指定列中的最小值
    :param matrix:
    :param index:指定列序号
    :return:
    """
    li = []
    for row in matrix:
        li.append(row[index])
    return min(li)

def z_score(temp,sim_matrix):
    """
    返回列表的z-score的值
    :param temp: [index...],与sim_matrix中相对应
    :param sim_matrix:相识度矩阵
    :return:
    """
    sum = 0
    for i in temp:
        print "i:",i
        for j in temp:
            print "j:", j
            if i < j:
                print "sim_matrix[i][j]:",sim_matrix[i][j]
                sum += sim_matrix[i][j]
                print "sum:",sum
            else:
                pass
    k = len(temp)
    print "sssum:", sum
    print "2*sum/(k*(k-1)):", 2*sum/(k*(k-1))
    result = 1-2*sum/(k*(k-1))
    return result

def get_random_sort(li):
    """
    返回乱序过后的li,副本
    :param li:
    :return:
    """
    temp = list(li)
    length = len(temp)
    result = []
    i = 0
    while i < length:
        j = random.randint(0, (len(temp) - 1))
        result.append(temp[j])
        temp.pop(j)
        i += 1
    return result




if __name__ == '__main__':
    matrix = [[1,2,3,4,2],[2,1,3,4,9],[5,2,1,4,2],[5,12,1,4,5],[5,12,3,4,6]]
    matrix1 = [[1, 2, 3, 4], [2, 1, 3, 4], [5, 2, 1, 4], [5, 12, 1, 4], [5, 12, 3, 4]]
    matrix = np.array(matrix)
    matrix1 = np.array(matrix1)
    temp = [1,2,4]
    # print get_sim_matrix(matrix1)
    # print z_score(temp,get_sim_matrix(matrix))
    li = [[1,2],[12,3],[11,2],[2,1],[4,5],[6,5],[1,1],[9,5]]
    test = [1, 2, 3, 4]
    print get_random_sort(test)