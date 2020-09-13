# -*- coding: utf-8 -*-
"""
Created on 2018/2/14 13:01
@file: excel_utils.py
@author: Administrator
"""
from xlutils.copy import copy
import xlrd
import xlwt
import os

def get_excel(file_path,excel_sheet):
    """
    获取excel中指定主题的内容对象
    :param file_path:
    :param excel_sheet:
    :return:
    """
    data = xlrd.open_workbook(file_path)
    if type(excel_sheet) == type(0):
        table = data.sheet_by_index(excel_sheet)  # 通过索引顺序获取
        # table = data.sheets()[excel_sheet]  # 通过索引顺序获取
    else:
        table = data.sheet_by_name(excel_sheet)  # 通过名称获取
    return table
def write_into(title_list,content_matrix,file_path):
    """
    保存content_matrix中的内容到新建的excel中
    :param title_list: 第一行标题
    :param content_matrix: 内容
    :param file_path: 文件位置
    :return:
    """
    #文件存在则删除
    if os.path.isfile(file_path):
        os.remove(file_path)
    # 新建一个excel文件
    file = xlwt.Workbook()
    # 新建一个sheet
    table = file.add_sheet('one', cell_overwrite_ok=True)
    for i in range(len(title_list)):
        table.write(0,i,title_list[i])
    for r in range(len(content_matrix)):
        for c in range(len(content_matrix[r])):
            table.write(r+1,c,content_matrix[r][c])
    # 保存文件
    file.save(file_path)

def write_add_matrix(title_list,content_matrix,file_path):
    if os.path.isfile(file_path) == False:
        file = xlwt.Workbook()
        table = file.add_sheet('one', cell_overwrite_ok=True)
        file.save(file_path)
    original = xlrd.open_workbook(file_path)
    rows = original.sheets()[0].nrows #获取原有的excel的行数
    new_excel = copy(original)# 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    table = new_excel.get_sheet(0)
    for i in range(len(title_list)):
        table.write(rows,i,title_list[i])
    for r in range(len(content_matrix)):
        for c in range(len(content_matrix[r])):
            table.write(rows+r+1,c,content_matrix[r][c])
    new_excel.save(file_path)

def write_matrix_by_sheet(title_list,content_matrix,file_path,excel_sheet = 'one',sheet_index = 0):
    if os.path.isfile(file_path) == False:
        file = xlwt.Workbook()
        new_excel = file.add_sheet(excel_sheet, cell_overwrite_ok=True)
        file.save(file_path)
        original = xlrd.open_workbook(file_path)
        rows = original.sheets()[0].nrows  # 获取原有的excel的行数
        new_excel = copy(original)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    else:
        original = xlrd.open_workbook(file_path)
        new_excel = copy(original)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
        new_excel.add_sheet(excel_sheet, cell_overwrite_ok=True)
    table = new_excel.get_sheet(sheet_index)
    for i in range(len(title_list)):
        table.write(0,i,title_list[i])
    for r in range(len(content_matrix)):
        for c in range(len(content_matrix[r])):
            table.write(r+1,c,content_matrix[r][c])
    new_excel.save(file_path)

def write_add(r,c,content,file_path):
    """
    向excel中的文件内容进行追加
    :param r:
    :param c:
    :param content:
    :param file_path:
    :return:
    """
    original = xlrd.open_workbook(file_path)
    rows = original.sheets()[0].nrows
    new_excel = copy(original)# 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    table = new_excel.get_sheet(0)
    table.write(rows + r,c,content)
    new_excel.save(file_path)# xlwt对象的保存方法，这时便覆盖掉了原来的excel

if __name__ == '__main__':
    write_add_matrix(['g','h','j'],[[1,2,3]],'../matrix/test.xls')