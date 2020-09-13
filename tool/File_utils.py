# -*- coding: utf-8 -*-
"""
Created on 2017/11/6 17:45
@file: File_utils.py
@author: Administrator
"""
import os

#创建文件夹
def FileMkdir(file_path):
    if not os.path.isdir(file_path):
        os.mkdir(file_path)
#创建文件
def FileFile(file_path):
    if not os.path.isfile(file_path):
        f = open(file_path ,"w")
        f.close()

def savetxt(file_path,matrix,way = 'w', chinese=False):
    """
    将matrix保存到指定文件txt中，即使每行列数不相等
    :param file_path:
    :param matrix:
    :param way:
    :return:
    """
    f = open(file_path,way)
    if chinese:
        for i in range(len(matrix)):
            st = ''
            for j in range(len(matrix[i])):
                if j != len(matrix[i]) - 1:
                    st = st + str(matrix[i][j]) + ' '
                else:
                    st = st + str(matrix[i][j])
            print >> f, st.decode('utf-8')
    else:
        for i in range(len(matrix)):
            st = ''
            for j in range(len(matrix[i])):
                if j != len(matrix[i]) - 1:
                    st = st + str(matrix[i][j])+ ' '
                else:
                    st = st + str(matrix[i][j])
            print >> f, st
    f.close()

def savetxt_three_dia(file_path,matrix,way = 'w', chinese=False):
    """
    将matrix(三维)保存到指定文件txt中，即使每行列数不相等
    :param file_path:
    :param matrix:
    :param way:
    :return:
    """
    f = open(file_path,way)
    print 'chinese:',chinese
    if chinese:
        for i in range(len(matrix)):
            st = ''
            for j in range(len(matrix[i])):
                if j != len(matrix[i]) - 1:
                    st = st + matrix[i][j][0]+ '\t'
                else:
                    st = st + matrix[i][j][0]
            print >> f, st.encode('utf-8')
    else:
        for i in range(len(matrix)):
            st = ''
            for j in range(len(matrix[i])):
                if j != len(matrix[i]) - 1:
                    st = st + str(matrix[i][j][0]) + '\t'
                    print "save:", st
                else:
                    st = st + str(matrix[i][j][0])
                    print "save:", st
            print >> f, st
    f.close()

def savetxt_str(file_path,content,way = 'w',chinese = False):
    """
    将content保存到指定文件txt中
    :param file_path:
    :param matrix:
    :param way:
    :param chinese:
    :return:
    """
    f = open(file_path,way)
    if chinese:
        print >> f, content
    else:
        print >>f, content.decode('utf-8')
    f.close()

def savetxt_li(file_path,li,way = 'w',chinese = False):
    """
    将content保存到指定文件txt中
    :param file_path:
    :param matrix:
    :param way:
    :param chinese:
    :return:
    """
    f = open(file_path,way)
    str = ''
    if chinese:
        for i in li:
            str = str + i + '\t'
        print >> f, str
    else:
        for i in li:
            str = str + i + '\t'
        print >>f, str.decode('utf-8')
    f.close()

if __name__ == "__main__":
    # FileFile("../data/5.txt")
    a = [[1,2],[1,2,3],[1,2,4,5]]
    savetxt('D:/test.txt',a)