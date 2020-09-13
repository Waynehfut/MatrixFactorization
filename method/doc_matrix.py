# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:57:03 2017

@author: Administrator
"""
from __future__ import division
from confact import *
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import tool.File_utils as df

or_mat = []
# 记录有值的位置
val_loc = []
# 存储被抽空的值的位置
changed_zero = []


# 将表内容变成矩阵，or读取矩阵
def get_Matrix_from_lc_tp(lc_table_name, tp_table_name, ratio,judge):
    or_mat = []
    val_loc = []

    if judge == 0:
        # start 生成原始矩阵
        sql1 = 'select * from {0}'
        sql1 = sql1.format(lc_table_name)
        sql2 = 'select * from {0}'
        sql2 = sql2.format(tp_table_name)
        db = DatabaseConnection()
        cur = db.dbConnect()
        # 执行sql1语句
        cur.execute(sql1)
        result1 = cur.fetchall()
        # 执行sql2语句
        cur.execute(sql2)
        result2 = cur.fetchall()
        cur.close()

        doc_num = len(result1)
        doc_num1 = len(result2)
        if doc_num != doc_num1:
            return "erro";
        r = 0
        while r < doc_num:
            matrix_row_value = []
            row1 = result1[r]
            row2 = result2[r]
            # print "row1", len(row1)
            # h = 2
            # print range(2, len(row1))
            for num in range(2, len(row1)):
                val = 0
                if (row1[num] != 0 or row2[num] != 0):
                    # 好评与问诊量权重为各位0.5
                    val = row1[num]* 0.5 + row2[num]* 0.5
                    val_loc.append([r, num - 2])
                    matrix_row_value.append(val)
                else:
                    matrix_row_value.append(val)
                    # h += 1
            r += 1
            or_mat.append(matrix_row_value)
        or_mat = np.array(or_mat)
        #end 生成原始矩阵

        # 区间缩放法
        min_max = MinMaxScaler()
        or_mat = min_max.fit_transform(or_mat)
        orignal_matrix = np.array(or_mat)
        # end
        file_Name = "../matrix/" + tp_table_name[3:].decode('utf-8') + "/or_mat.txt"
        df.FileFile(file_Name)
        np.savetxt(file_Name, or_mat, fmt='%.8f')

        dig_matrix0, dig_matrix_real, changed_zero = chmatrix_or(tp_table_name[3:], val_loc, or_mat, float(ratio), judge)
        # 抽取的值的位置改为-2，并输出到dig_matrix_ratio.txt
        np.savetxt("../matrix/" + tp_table_name[3:].decode('utf-8') + "/resource/" + str(ratio) + ".txt",
                   dig_matrix_real,
                   fmt='%.8f')
        return dig_matrix0, orignal_matrix, list(changed_zero)
    else:
        or_mat = np.loadtxt("../matrix/" + tp_table_name[3:].decode('utf-8') + "/or_mat.txt", dtype=np.float)
        or_mat = np.array(or_mat)
        dig_matrix = np.loadtxt("../matrix/" + tp_table_name[3:].decode('utf-8') + "/resource/" + str(ratio) + ".txt", dtype=np.float)
        dig_matrix0 ,changed_zero =chmatrix(or_mat, dig_matrix)
        # 抽取的值的位置改为-2，并输出到dig_matrix_ratio.txt
        return dig_matrix0, or_mat, list(changed_zero)


# 将表内容变成矩阵,or读取矩阵
def getMatrix(table_name, ratio,judge):
    or_mat = []
    val_loc = []
    if judge == 0:
        # global or_mat
        or_mat = []
        changed_zero = []

        sql = 'select * from {0}'
        sql = sql.format(table_name)
        db = DatabaseConnection()
        cur = db.dbConnect()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        i = 1
        r = 0
        for row in result:
            asun = []
            i = 1
            h = 0
            for num in row:
                if i > 2:
                    if (num > 0):
                        val_loc.append([r, h])
                    asun.append(num)
                    h += 1
                i = i + 1
            r += 1
            or_mat.append(asun)
        # Z-Scores
        # sc = StandardScaler()
        # sc.fit(or_mat)
        # or_mat = sc.transform(or_mat)
        # end
        # 区间缩放法
        min_max = MinMaxScaler()
        or_mat = min_max.fit_transform(or_mat)
        orignal_matrix = np.array(or_mat)
        # end
        file_Name = "../matrix/" + table_name[3:].decode('utf-8') + "/or_mat.txt"
        df.FileFile(file_Name)
        np.savetxt(file_Name, orignal_matrix, fmt='%.8f')
        # print "type:",type(or_mat)
        # dig_matrix:挖取的值变0，dig_matrix_real:挖取的值变-2
        dig_matrix, dig_matrix_real, changed_zero = chmatrix_or(table_name[3:], val_loc, orignal_matrix, float(ratio), 0)
        # 抽取的值的位置改为-2，并输出到dig_matrix_ratio.txt
        np.savetxt("../matrix/" + table_name[3:].decode('utf-8') + "/resource/dig_matrix_" + str(ratio) + ".txt",
                   dig_matrix_real,
                   fmt='%.8f')
        n,m = or_mat.shape
        print n,m
    else:
        orignal_matrix = np.loadtxt("../matrix/" + table_name[3:].decode('utf-8') + "/or_mat.txt", dtype=np.float)
        orignal_matrix = np.array(orignal_matrix)
        dig_matrix = np.loadtxt("../matrix/" + table_name[3:].decode('utf-8') + "/resource/" + str(ratio) + ".txt", dtype=np.float)
        dig_matrix ,changed_zero =chmatrix(orignal_matrix, dig_matrix)
        # 抽取的值的位置改为-2，并输出到dig_matrix_ratio.txt
        return dig_matrix, orignal_matrix, list(changed_zero)
    return dig_matrix, orignal_matrix, list(changed_zero)


"""
随机从矩阵中抽取若干个有值的出来
"""


def chmatrix_or(table_name, val_loc,or_mat,ratio,judge):
    """
    返回被挖去过值的矩阵及
    :param file_name:
    :param val_loc:
    :param or_mat:
    :param ratio:
    :return:
    """
    changed_zero = []
    if judge == 1:
        # start改过的,从现有的挖取过值的矩阵进行处理
        # print table_name.decode("utf-8")
        changedFile = open("../matrix/" + table_name.decode("utf-8") + "/resource/" + str(ratio) + ".txt","r")
        iter_file = iter(changedFile)
        i = 0
        j = 0
        for line in iter_file:
            for ls in line.strip('\n').split(" "):
                if ls == '-2.0':
                    changed_zero.append([i, j])
                j += 1
            i += 1
            j = 0
        changedFile.close()
        dig_matrix0 = np.array(or_mat)
        # dig_matrix_real 用于存储矩阵的，-2代表该处值已被挖去
        dig_matrix_real = np.array(dig_matrix0)
        for k in range(len(changed_zero)):
            dig_matrix0[changed_zero[k][0]][changed_zero[k][1]] = 0.0
            dig_matrix_real[changed_zero[k][0]][changed_zero[k][1]] = -2.0
        # 改过的end
    else:
        # 原来start
        i = round(len(val_loc) * (1 - ratio))
        dig_matrix0 = list(or_mat)
        dig_matrix_real = np.array(dig_matrix0)
        # 随机选出i个有值的数，供验证矩阵分解
        val = np.random.randint(0, len(val_loc), int(i))
        for k in val:
            changed_zero.append(val_loc[k])
            dig_matrix0[val_loc[k][0]][val_loc[k][1]] = 0
            dig_matrix_real[val_loc[k][0]][val_loc[k][1]] = -2.0
            # 原来end
    return np.array(dig_matrix0), np.array(dig_matrix_real),list(changed_zero)

def chmatrix(or_mat,dig_matrix):
    """
    记录被挖取的位置，并返回记录和将挖取的位置变0后的矩阵
    :param or_mat:
    :param dig_matrix:
    :return:
    """
    changed_zero = []
    dig_matrix0 = np.array(or_mat)
    # dig_matrix_real 用于存储矩阵的，-2代表该处值已被挖去
    dig_matrix_real = np.array(dig_matrix)
    # 随机选出i个有值的数，供验证矩阵分解
    i,j = dig_matrix.shape
    # print i,j
    for row in range(i):
        for column in range(j):
            if dig_matrix[row][column] == -2:
                li = []
                li.append(row)
                li.append(column)
                changed_zero.append(li)
                dig_matrix0[row][column] = 0
    # 原来end
    return dig_matrix0, list(changed_zero)

"""
将扣掉地方的值变为-2
"""


# def change_file_output():
#     global or_mat
#     global changed_zero
#     or_mat_for_change = np.array(or_mat)
#     for k in range(len(changed_zero)):
#         or_mat_for_change[changed_zero[k][0]][changed_zero[k][1]] = 0
#     return or_mat_for_change


# 标准化 x/max
def getNor(array):
    array1 = np.array(array, dtype=float)
    tt = [i / np.max(i) for i in array.T]
    return np.array(tt, dtype=float)

def get_density_matrix(table_name):
    """
    计算矩阵密度
    :param table_name:
    :return:
    """
    or_mat = np.loadtxt("../matrix/" + table_name.decode('utf-8') + "/or_mat.txt", dtype=np.float)
    n,m = or_mat.shape
    num = 0
    for i in range(n):
        for j in range(m):
            if or_mat[i][j] > 0:
                num += 1
    return num/(n*m)

def get_matrix_by_exist(tp_table_name,ratio):
    """
    从已处理过的的矩阵中获取新的矩阵
    :param tp_table_name:
    :param ratio:
    :return:
    """
    or_mat = np.loadtxt("../matrix/" + tp_table_name[3:].decode('utf-8') + "/or_mat.txt", dtype=np.float)
    or_mat = np.array(or_mat)
    dig_matrix = np.loadtxt("../matrix/" + tp_table_name[3:].decode('utf-8') + "/resource/" + str(ratio) + ".txt",
                            dtype=np.float)
    dig_matrix0, changed_zero = chmatrix(or_mat, dig_matrix)
    # 抽取的值的位置改为-2，并输出到dig_matrix_ratio.txt
    return dig_matrix0, or_mat, list(changed_zero)

if __name__ == '__main__':
    # t = np.zeros([2,4])
    # print "t",t
    # np.savetxt("../log/testFile.txt",t,fmt='%.6f')


    # changedFile = open("../data/test.txt", "r")
    # print type(changedFile.readlines()[0]);
    # iter_file = iter(changedFile)
    # i = 0
    # j = 0
    # for line in iter_file:
    #     for ls in line.strip('\n').split(" "):
    #         if ls == '-2':
    #             changed_zero.append([i, j])
    #         j += 1
    #     i += 1
    #     j = 0
    # print changed_zero


    # changed_zero  # t = getMatrix('tp_风湿科')
    # l = [[1,2],[1,3],[2,9]]
    # g = np.array(l)
    # di = g.shape
    # dif_v = [[0 for ki in range(di[1])] for kj in range(di[0])]
    # print dif_v
    # print len(l)
    # print len(l[0])
    # for k in di:
    #     print k
    # print changed_zero

    # ratios = [0.05, 0.1, 0.15, 0.2, 0.25, 0.30, 0.35, 0.4, 0.45, 0.5, 0.55, 0.60, 0.65, 0.70, 0.75, 0.8, 0.85, 0.9,
    #               0.95]
    # table_names = ['神经外科','神经内科','泌尿外科','内分泌科']
    # for name in range(len(table_names)):
    #     for i in range(len(ratios)):
    #         lc_table_name = 'lc_' + table_names[name]
    #         tp_table_name = 'tp_' + table_names[name]
    #         dig_matrix, or_matrix, changed_zero = get_Matrix_from_lc_tp(lc_table_name, tp_table_name, ratios[i],0)
    #         file_Name = "../matrix/" + table_names[name].decode('utf-8') + "/or_mat.txt"
    #         df.FileFile(file_Name)
    #         n,m = or_matrix.shape
    #         print "%s:  行：%s;列：%s"%(table_names[name],n,m)
    #         np.savetxt(file_Name, or_matrix, fmt='%.8f')
    # print 'finish====================================='


    table_names = ['神经内科','内分泌科']
    for name in range(len(table_names)):
        print get_density_matrix(table_names[name])


    # table_names = ['lc_神经内科', 'lc_内分泌科']
    # for keshi in table_names:
    #     print "keshi",keshi
    #     getMatrix(keshi, '0.50', 0)
