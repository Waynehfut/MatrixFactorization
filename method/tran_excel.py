# # -*- coding: utf-8 -*-
# """
# Created on 2018/2/15 21:15
# @file: tran_excel.py
# @author: Administrator
# """
# import string
# import tool.excel_utils as exu
# def tran_excel():
#     title_list = ['ratio', 'original_diversity', 'one_diversity', 'two_diversity', 'greedy2_diversity', 'swap2_diversity','dum_diversity','mmr_diversity','vns_diversity']
#     file_path = '../matrix/system_diversity_result.xls'
#     content_matrix = []
#     us_file = open('H:\\Untitled Folder\\7\\matrix\\system_diversity_result.txt', 'r')
#     us_lines = us_file.readlines()
#     us_line_index = 0
#     line_num = 0
#     while us_line_index < len(us_lines):
#         li = []
#         line = us_lines[us_line_index].strip('\n')
#         if string.find(line, 'ratio') >= 0:
#             pass
#         elif string.find(line, '=') >= 0:
#             pass
#         else:
#             print "line:", line
#             line_num += 1
#             # line_split = line.split(' ')
#             line_split = line.split('\t')
#             print 'len:',len(line_split)
#             for j in range(len(line_split)):
#                 if len(line_split[j]) == 0:
#                     pass
#                 else:
#                     print 'line_split[j]:',line_split[j]
#                     li.append(line_split[j])
#             print "li:",li
#             content_matrix.append(li)
#         if line_num == 10:
#             line_num = 0
#         us_line_index += 1
#     exu.write_add_matrix(title_list, content_matrix, file_path)
#
# def tran_excel_split(hour):
#     sheets = {'3':'three','5':'five','7':'seven'}
#     # title_list = ['ratio', 'original_diversity', 'one_diversity', 'two_diversity', 'greedy2_diversity', 'swap2_diversity','dum_diversity','mmr_diversity','vns_diversity']
#     title_list = ['ratio', 'Original','One', 'DivSwap',	'DivGreedy', 'SWAP', 'DUM', 'MMR', 'VNS']
#
#     file_path = '../matrix/'+ hour + 'system_diversity_result.xls'
#     content_matrix = []
#     us_file = open('H:\\Untitled Folder\\' + hour +'\\matrix\\system_diversity_result.txt', 'r')
#     us_lines = us_file.readlines()
#     us_line_index = 0
#     line_num = 0
#     keshi = 0
#     while us_line_index < len(us_lines):
#         li = []
#         line = us_lines[us_line_index].strip('\n')
#         if string.find(line, 'ratio') >= 0:
#             pass
#         elif string.find(line, '=') >= 0:
#             pass
#         else:
#             print "line:", line
#             line_num += 1
#             # line_split = line.split(' ')
#             line_split = line.split('\t')
#             print 'len:',len(line_split)
#             for j in range(len(line_split)):
#                 if len(line_split[j]) == 0:
#                     pass
#                 else:
#                     print 'line_split[j]:',line_split[j]
#                     li.append(round(float(line_split[j]),6))
#             print "li:",li
#             content_matrix.append(li)
#         if line_num == 10:
#             line_num = 0
#             if keshi == 0:
#                 keshi = 1
#                 sheet = sheets[hour] + '1'
#                 exu.write_matrix_by_sheet(title_list, content_matrix, file_path, sheet,0)
#                 content_matrix = []
#             else:
#                 sheet = sheets[hour] + '2'
#                 exu.write_matrix_by_sheet(title_list, content_matrix, file_path, sheet,1)
#         us_line_index += 1
#
# def split_space(li):
#     line = li.split(' ')
#     l = []
#     for i in range(len(line)):
#         if len(line[i]) == 0:
#             pass
#         else:
#             l.append(line[i])
#     return l
#
#
# if __name__ == '__main__':
#     # tran_excel()
#
#     hour = ['3','5','7']
#     for i in hour:
#         tran_excel_split(i)