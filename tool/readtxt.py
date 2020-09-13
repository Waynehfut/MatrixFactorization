# -*- coding: utf-8 -*-
"""
Created on 2017/10/21 23:17
@file: readtxt.py
@author: Administrator
"""
import os
import  numpy as np
# 一列n行，逐行读取
def load_file_to_array1(file_name, rows, cols):
    array = np.ndarray(shape=(rows, cols), dtype=int, order='C')
    data_file = open(file_name)
    data_lines = data_file.readlines()
    data_file.close()

    idx = 0
    for data in data_lines:
        print type(data)
        print float(data)
        array[idx%rows][idx/cols] = float(data)
        idx = idx + 1

    return array


# txt中的数据本身就按 mxn 排列的矩阵
def load_file_to_array(file_name):
    array = np.loadtxt(file_name, dtype=np.float)

    return array


# 直接将矩阵写入txt
def write_array_to_file(file_name, array):
    np.savetxt(file_name, array, fmt="%d", delimiter=' ', newline='\n')

if __name__ == '__main__':
    t = open("..",'w')
    write_array_to_file(t,np.array([[1,2,3],[1,2,3]]))


