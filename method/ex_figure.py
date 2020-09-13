# # -*- coding: utf-8 -*-
# from matplotlib.font_manager import FontProperties
# from matplotlib.ticker import MultipleLocator, FormatStrFormatter
# from xlutils.copy import copy
# import matplotlib.pyplot as plt
# import matplotlib as mapl
# import string
# import tool.excel_utils as exu
# import xlrd
# import numpy as np
# import xlwt
#
# def paint_ly(x, y, titel, file_path, xlable, yable, labels, yrange):
#     font = FontProperties(fname=r"C:\\WINDOWS\\Fonts\\simsun.ttc", size=14)  # C:\WINDOWS\Fonts
#     # mpl.rcParams['font.sans-serif'] = ['SimHei']
#     fig = plt.figure(1)
#     # colors = {'blue': 'blue', 'red': 'red', 'green': 'green', 'yellow': 'yellow'}
#     colors = ['blue', 'yellow', 'red', 'green', 'pink']
#     # ways = ["us", "MF","ipcc",'upcc','ip_up']
#     for i in range(len(x)):
#         print 'x[i]', len(x[i])
#         print 'y[i]', len(y[i])
#         print 'y[i]', y[i]
#         plt.plot(x[i], y[i], color=colors[i], linewidth=1.0, linestyle="-", alpha=1, label=labels[i].decode('utf-8'))
#         plt.legend(loc='upper right', bbox_to_anchor=(1, 1))
#     plt.title(titel, fontproperties=font)
#     xmajorFormatter = FormatStrFormatter('%1.2f')  # 设置x轴标签文本的格式
#     x_MultipleLocator = MultipleLocator(0.05)  # 设置x轴刻度间隔
#     plt.grid(True)  # 设置网络格点
#     plt.xlabel(xlable)  # 设置x轴标签
#     plt.ylabel(yable)  # 设置y轴标签
#     # plt.axis([0.5, 1, 0, 0.5])
#     plt.axis(yrange)
#     ax = plt.gca()
#     ax.xaxis.set_major_locator(x_MultipleLocator)  # 设置x轴刻度间隔
#     ax.xaxis.set_major_formatter(xmajorFormatter)  # 设置x轴标签文本的格式
#     ax.spines["right"].set_color("none")
#     ax.spines["top"].set_color("none")
#     # ax.spines["left"].set_position(("data",0))
#     # ax.spines["bottom"].set_position(("data",0))
#     # plt.show()
#     # ps.dump(fig,open('C:/Users/Administrator/Desktop/fig.pickle','wb'))
#     print "保存图片", file_path
#     plt.savefig(file_path + "_" + yable + '.png')
#     plt.close()
#
#
# def div_fig(x, y, titel, file_path, ncol, xlabel, ylabel, labels, yrange, interval = 0.05, legend_anchor=(1,1)):
#     # title_font = FontProperties(fname=r"C:\\WINDOWS\\Fonts\\simsun.ttc", size=32)  # C:\WINDOWS\Fonts
#     legend_font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 24, }
#     xlabel_font = {'family': 'Times New Roman', 'weight': 'bold', 'size': 33, }
#     ylabel_font = {'family': 'Times New Roman', 'weight': 'bold', 'size': 33, }
#     title_font = {'family': 'Times New Roman', 'weight': 'bold', 'verticalalignment':'bottom', 'size': 33, }
#
#     # 设置坐标轴刻度线朝向，in 向内
#     mapl.rcParams['xtick.direction'] = 'in'
#     mapl.rcParams['ytick.direction'] = 'in'
#
#     # plt.figure(num=1, figsize=[13, 10])
#     plt.figure(num=1, figsize=[12, 11])
#     colors = ['yellow', 'red', 'blue', 'green', 'black', 'cyan', 'pink', 'magenta']
#     markers = ['o', 'v', 's', 'p', '^', 'l', '+', 'x']
#     # ways = ["us", "MF","ipcc",'upcc','ip_up']
#     # print "len(x):",len(x)
#     # print "len(y):", len(y)
#     # print "labels:",labels
#     for i in range(len(x)):
#         # print 'x[i]', len(x[i])
#         # print 'y[i]', len(y[i])
#         # print 'y[i]', y[i]
#         plt.plot(x[i], y[i], color=colors[i], linewidth=4.0, markersize=15, marker=markers[i], alpha=1,
#                  label=labels[i].decode('utf-8'))
#         plt.legend(ncol=ncol, bbox_to_anchor=legend_anchor, prop=legend_font, fancybox=True,labelspacing=0.1)
#     plt.title(titel, fontdict=title_font)
#
#     plt.grid(True, color='gray', linestyle='--')  # 设置网络格点
#     plt.xlabel(xlabel, xlabel_font)  # 设置x轴标签
#     plt.ylabel(ylabel, ylabel_font)  # 设置y轴标签
#     # plt.axis([0.5, 1, 0, 0.5])
#     plt.axis(yrange)
#     ax = plt.gca()
#
#     # 设置x轴标签文本和x轴刻度间隔
#     xmajorLocator = MultipleLocator(0.05)  # 将x主刻度标签设置为0.1的倍数
#     xmajorFormatter = FormatStrFormatter('%1.2f')  # 设置x轴标签文本的格式
#     # xminorLocator = MultipleLocator(0.05)  # 将x轴次刻度标签设置为0.05的倍数
#
#     ymajorLocator = MultipleLocator(interval)  # 将y轴主刻度标签设置为1的倍数
#     ymajorFormatter = FormatStrFormatter('%1.2f')  # 设置y轴标签文本的格式
#     # yminorLocator = MultipleLocator(0.2)  # 将此y轴次刻度标签设置为0.2的倍数
#
#     # 设置主刻度标签的位置,标签文本的格式
#     ax.xaxis.set_major_locator(xmajorLocator)
#     ax.xaxis.set_major_formatter(xmajorFormatter)
#
#     ax.yaxis.set_major_locator(ymajorLocator)
#     ax.yaxis.set_major_formatter(ymajorFormatter)
#
#     # 显示次刻度标签的位置,没有标签文本
#     # ax.xaxis.set_minor_locator(xminorLocator)
#     # ax.yaxis.set_minor_locator(yminorLocator)
#
#     # ax.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
#     # ax.yaxis.grid(True, which='major')  # y坐标轴的网格使用次刻度
#
#     # xmajorFormatter = FormatStrFormatter('%1.2f')  # 设置x轴标签文本的格式
#     # x_MultipleLocator = MultipleLocator(0.05)  # 设置x轴刻度间隔
#     # ax.xaxis.set_major_locator(x_MultipleLocator)  #设置x轴刻度间隔
#     # ax.xaxis.set_major_formatter(xmajorFormatter)  # 设置x轴标签文本的格式
#
#     # 设置坐标刻度值的大小以及刻度值的字体
#     plt.tick_params(pad=17, labelsize=24)
#     labels = ax.get_xticklabels() + ax.get_yticklabels()
#     [label.set_fontname('Times New Roman') for label in labels]
#
#     # plt.show()
#     # ps.dump(fig,open('C:/Users/Administrator/Desktop/fig.pickle','wb'))
#     print "保存图片", file_path
#     fpath = file_path + '.tif'
#     plt.savefig(fpath, dpi=96,bbox_inches='tight')
#     plt.close()
#
#
# def rmse_mae_figure():
#     keshis = ["内分泌科", "神经内科", "神经外科", "泌尿外科"]
#     keshis = ["内分泌科", "神经内科"]
#     keshis_index = ['a', 'b', 'c', 'd']
#     ways = ["us", "MF", "ipcc", 'upcc', 'ip_up']
#     yrmse = [[0.5, 1, 0.15, 0.5], [0.5, 1, 0.15, 0.6]]
#     ymae = [[0.5, 1, 0.1, 0.35], [0.5, 1, 0.1, 0.4]]
#     # us
#     us_file = open('../matrix/RMSE_MAE.txt', 'r')
#     us_lines = us_file.readlines()
#     us_line_index = 0
#     # mf
#     mf_file = open('../matrix/simple_matrix_factorization/RMSE_MAE.txt', 'r')
#     mf_lines = mf_file.readlines()
#     mf_line_index = 0
#     x = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
#     X = [x, x, x, x, x]
#     Y_RMSE = []
#     Y_MAE = []
#     cal_num = 0
#     for i in range(len(keshis)):
#         other_file = open('D:\\lyq_sy\\' + keshis[i].decode('utf-8') + '\\RMSE_MAE.txt', 'r')
#         line_num = 0
#         RMSE = []
#         MAE = []
#         # 添加矩阵分解的结果
#         while us_line_index < len(us_lines):
#             line = us_lines[us_line_index].strip('\n')
#             # print "i:", i
#             if string.find(line, 'ratio') >= 0:
#                 pass
#             elif string.find(line, keshis_index[i]) < 0 or line_num != 0:
#                 if line_num < 10:
#                     line_num += 1
#                     line_split = line.split(' ')
#                     ratios = []
#                     k = 0  # 判断此时的值是ratio 还是 RMSE,MAE
#                     for j in range(len(line_split)):
#                         if len(line_split[j]) == 0:
#                             pass
#                         else:
#                             if k == 0:
#                                 ratios.append(line_split[j])
#                                 k += 1
#                             elif k == 1:
#                                 RMSE.append(line_split[j])
#                                 k += 1
#                             elif k == 2:
#                                 MAE.append(line_split[j])
#                 else:
#                     break
#             us_line_index += 1
#
#         Y_RMSE.append(RMSE)
#         Y_MAE.append(MAE)
#
#         RMSE = []
#         MAE = []
#         mf_line_num = 0
#         k = 0
#         # 添加矩阵分解的结果
#         while mf_line_index < len(mf_lines):
#             mf_line = mf_lines[mf_line_index].strip('\n')
#             # print "i:", i
#             if string.find(mf_line, 'ratio') >= 0:
#                 pass
#             elif string.find(mf_line, keshis_index[i]) < 0 or mf_line_num != 0:
#                 if mf_line_num < 10:
#                     mf_line_num += 1
#                     line_split = mf_line.split(' ')
#                     ratios = []
#                     k = 0  # 判断此时的值是ratio 还是 RMSE,MAE
#                     for j in range(len(line_split)):
#                         if len(line_split[j]) == 0:
#                             pass
#                         else:
#                             if k == 0:
#                                 ratios.append(line_split[j])
#                                 k += 1
#                             elif k == 1:
#                                 RMSE.append(line_split[j])
#                                 k += 1
#                             elif k == 2:
#                                 MAE.append(line_split[j])
#                 else:
#                     break
#             mf_line_index += 1
#
#         Y_RMSE.append(RMSE)
#         Y_MAE.append(MAE)
#
#         jav_RMSE = []
#         jav_MAE = []
#
#         jline_num = 0
#         # 判断此时的值是ipcc 还是 upcc,融合
#         for line in other_file.readlines():
#             line = line.strip('\n')
#             if string.find(line, 'T') >= 0:
#                 print "line", line
#                 pass
#             else:
#                 jline_split = line.split(' ')
#                 if jline_num < 10:
#                     jline_num += 1
#                     k = 0  # 判断此时的值是ratio 还是 RMSE,MAE
#                     for ji in range(len(jline_split)):
#                         if len(jline_split[ji]) == 0:
#                             pass
#                         else:
#                             if k == 0:
#                                 ratios.append(jline_split[ji])
#                                 k += 1
#                             elif k == 1:
#                                 jav_RMSE.append(jline_split[ji])
#                                 k += 1
#                             elif k == 2:
#                                 jav_MAE.append(jline_split[ji])
#                     if jline_num == 10:
#                         print 'jav_RMSE', jav_RMSE
#                         print 'len_jav_RMSE', len(jav_RMSE)
#                         print 'jav_MAE', jav_MAE
#                         print 'len_jav_MAE', len(jav_MAE)
#                         Y_RMSE.append(jav_RMSE)
#                         Y_MAE.append(jav_MAE)
#                         jav_RMSE = []
#                         jav_MAE = []
#                         # print 'Y_RMSE', Y_RMSE
#                         # print 'Y_MAE', Y_MAE
#                         jline_num = 0
#         print "i===========", i
#         file_path = '../matrix/' + keshis[i].decode('utf-8')
#         print 'Y_RMSE', len(Y_RMSE[0])
#         print 'Y_RMSE', len(Y_RMSE)
#         print 'Y_MAE', len(Y_MAE[0])
#         rmse_titile = keshis[i].decode('utf-8') + "_RMSE"
#         mae_titile = keshis[i].decode('utf-8') + '_MAE'
#         paint_ly(X, Y_RMSE, rmse_titile, file_path, 'ratio', 'RMSE', ways, yrmse[i])
#         paint_ly(X, Y_MAE, mae_titile, file_path, 'ratio', 'MAE', ways, ymae[i])
#         Y_RMSE = []
#         Y_MAE = []
#
#
# def sys_div_figure():
#     # keshis = ["内分泌科", "神经内科", "神经外科", "泌尿外科"]
#     keshis = ["内分泌科", "神经内科"]
#     keshis_index = ['a', 'b', 'c', 'd']
#     ways = ['original', 'greedy', 'swap', 'mmr', 'vns']
#     yranges = [[0.5, 1, 4, 5.5], [0.5, 1, 5, 6.5]]
#     # us
#     us_file = open('../matrix/system_diversity_result.txt', 'r')
#     us_lines = us_file.readlines()
#     us_line_index = 0
#     x = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
#     X = [x, x, x, x, x]
#
#     Y = []
#
#     line_num = 0
#     original_sys_div = []
#     one_sys_div = []
#     two_sys_div = []
#     mmr_sys_div = []
#     vns_sys_div = []
#     i = -1
#     # 添加矩阵分解的结果
#     while us_line_index < len(us_lines):
#         line = us_lines[us_line_index].strip('\n')
#         if string.find(line, 'ratio') >= 0:
#             print "us_line_index0", us_line_index
#             print "line0:", line
#             pass
#         elif string.find(line, '=') >= 0:
#             print "us_line_index1", us_line_index
#             print "line1:", line
#             i += 1
#         elif line_num < 10:
#             print "us_line_index2", us_line_index
#             print "line2:", line
#             line_num += 1
#             line_split = line.split(' ')
#             ratios = []
#             k = 0  # 判断此时的值是ratio 还是 original,one,two,mmr,vns
#             for j in range(len(line_split)):
#                 if len(line_split[j]) == 0:
#                     pass
#                 else:
#                     if k == 0:
#                         ratios.append(line_split[j])
#                         k += 1
#                     elif k == 1:
#                         original_sys_div.append(line_split[j])
#                         k += 1
#                     elif k == 2:
#                         one_sys_div.append(line_split[j])
#                         k += 1
#                     elif k == 3:
#                         two_sys_div.append(line_split[j])
#                         k += 1
#                     elif k == 4:
#                         mmr_sys_div.append(line_split[j])
#                         k += 1
#                     elif k == 5:
#                         vns_sys_div.append(line_split[j])
#         if line_num == 10:
#             Y.append(original_sys_div)
#             Y.append(one_sys_div)
#             Y.append(two_sys_div)
#             Y.append(mmr_sys_div)
#             Y.append(vns_sys_div)
#             # print "original_sys_div", original_sys_div
#             # print "one_sys_div", one_sys_div
#             # print "two_sys_div", two_sys_div
#             # print "mmr_sys_div", mmr_sys_div
#             # print "vns_sys_div", vns_sys_div
#             # print "X", len(X[0])
#             # print "Y", len(Y[2])
#             print "us_line_index3", us_line_index
#             print "line3:", line
#             file_path = '../matrix/' + "sys_div_" + keshis[i].decode('utf-8')
#             title = keshis[i].decode('utf-8') + '_system_diversity'
#             paint_ly(X, Y, title, file_path, 'ratio', 'system_diversity', ways, yranges[i])
#             Y = []
#             original_sys_div = []
#             one_sys_div = []
#             two_sys_div = []
#             mmr_sys_div = []
#             vns_sys_div = []
#             line_num = 0
#
#         us_line_index += 1
#
#
# def new_sys_div_figure():
#     save_path = '../matrix/figure_exp/'
#     hours = ['three', 'five', 'seven']
#     labels1 = ['Original','DivGreedy','DUM','MMR']
#     labels2 = ['Original','DivSwap','SWAP','VNS']
#     for hour in hours:
#         excel_sheet1 = hour + '1'
#         excel_sheet2 = hour + '2'
#         if hour == 'three':
#             yrange11 = [0.5, 0.95, 4.65, 5]#greedy
#             legend_anchor11 = (1,1)
#             yrange12 = [0.5, 0.95, 4.86, 5.02]#swap
#             legend_anchor12 = (1,1)
#             yrange21 = [0.5, 0.95, 4, 4.64]#greedy
#             legend_anchor21 = (1,1)
#             yrange22 = [0.5, 0.95, 4, 4.8]#swap
#             legend_anchor22 = (1,1)
#             interval = [0.05, 0.02, 0.08, 0.08]
#             file_path = '../matrix/3system_diversity_result.xls'
#             new_save_path = save_path + '3div'
#         elif hour == 'five':
#             yrange11 = [0.5, 0.95, 5.5, 5.75]#greedy
#             legend_anchor11 = (1,1)
#             yrange12 = [0.5, 0.95, 5.4, 5.95]#swap
#             legend_anchor12 = (1, 1)
#             yrange21 = [0.5, 0.95, 4.35, 4.95]#greedy
#             legend_anchor21 = (1,1)
#             yrange22 = [0.5, 0.95, 4.3, 5]#swap
#             legend_anchor22 = (1,0.16)
#             interval = [0.05, 0.1, 0.1, 0.1]
#             file_path = '../matrix/5system_diversity_result.xls'
#             new_save_path = save_path + '5div'
#         else:
#             yrange11 = [0.5, 0.95, 5.55, 5.85]#greedy
#             legend_anchor11 = (1,1)
#             yrange12 = [0.5, 0.95, 5.5, 6]#swap
#             legend_anchor12 = (1, 0.67)
#             yrange21 = [0.5, 0.95, 4.5, 5.1]#greedy
#             legend_anchor21 = (0.54,1)
#             yrange22 = [0.5, 0.95, 4.4, 5.2]#swap
#             legend_anchor22 = (1, 0.4)
#             interval = [0.05, 0.08, 0.1, 0.2]
#             file_path = '../matrix/7system_diversity_result.xls'
#             new_save_path = save_path + '7div'
#
#         save_path11 = new_save_path + '_Greedy' + '_endocrinology.xls'
#         save_path12 = new_save_path + '_Swap' + '_endocrinology.xls'
#         save_path21 = new_save_path + '_Greedy' + '_neurology.xls'
#         save_path22 = new_save_path + '_Swap' + '_neurology.xls'
#         one_figure(file_path, excel_sheet1, 'endocrinology-combine', save_path11, 2, labels1, yrange11, legend_anchor11, interval[0], 0)
#         one_figure(file_path, excel_sheet1, 'endocrinology-combine', save_path12, 2, labels2, yrange12, legend_anchor12, interval[1], 1)
#         one_figure(file_path, excel_sheet2, 'neurology-combine', save_path21, 2, labels1, yrange21, legend_anchor21, interval[2], 0)
#         one_figure(file_path, excel_sheet2, 'neurology-combine', save_path22, 2, labels2, yrange22, legend_anchor22, interval[3], 1)
#
#
# def one_figure(file_path, excel_sheet, titel, save_path, ncol, labels, yrange, legend_anchor, interval, jud):
#     table = exu.get_excel(file_path.decode('utf-8'), excel_sheet)
#     # ncols = table.ncols
#     x = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
#     col1 = [1,4,6,7]
#     col2 = [1,3,5,8]
#     X1 = [x, x, x, x]
#     X2 = [x, x, x, x]
#     Y = []
#     if jud == 0:
#         for i in col1:
#             Y.append(np.array(table.col_values(i))[1:])
#             # print np.array(table.col_values(i)[1:])
#         div_fig(X1, Y, titel, save_path, ncol, 'Matrix density', 'EnDiv', labels, yrange,
#                     legend_anchor=legend_anchor, interval=interval)
#
#     else:
#         for j in col2:
#             Y.append(np.array(table.col_values(j))[1:])
#         div_fig(X2, Y, titel, save_path, ncol, 'Matrix density', 'EnDiv', labels, yrange,
#                     legend_anchor=legend_anchor, interval=interval)
#
#
# def get_excel(file_path, excel_sheet):
#     """
#     获取excel中指定主题的内容对象
#     :param file_path:
#     :param excel_sheet:
#     :return:
#     """
#     data = xlrd.open_workbook(file_path)
#     if type(excel_sheet) == type(0):
#         table = data.sheet_by_index(excel_sheet)  # 通过索引顺序获取
#         # table = data.sheets()[excel_sheet]  # 通过索引顺序获取
#     else:
#         table = data.sheet_by_name(excel_sheet)  # 通过名称获取
#
# def pre_figure(file_path, excel_sheet,save_path, ncol=2, front_title='test'):
#     table = exu.get_excel(file_path,excel_sheet)
#     # labels = table.row_values(1)[1:6]
#     labels = [u'UPCC', u'IPCC', u'WSRec', u'MF', u'HPR']
#     target_rows = range(1,6)#[1,2,3,4,5]#mae,+2 >> rmse
#     target_cols = range(2,12)#[2,3,4,5,6,7,8,9,10,11]
#     x = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
#     X = [x, x, x, x, x]
#     if excel_sheet == 0:
#         yranges = [[0.1, 0.26], [0.15, 0.4], [0.06, 0.32], [0.1, 0.46], [0.12, 0.34], [0.2, 0.46]]
#         legend_anchor = [[0.03, 0.73], [0.8, 0.71], [0.07, 0.73], [0.9, 0.28], [0.76, 0.73], [0.24, 0.8]]
#         interval = [0.02, 0.04,0.04, 0.04, 0.04, 0.04]
#     else:
#         yranges = [[0.12, 0.36], [0.2, 0.54], [0.15, 0.35], [0.2, 0.56], [0.2, 0.46], [0.28, 0.6]]
#         legend_anchor = [[0.76, 0.73], [0.6, 0.71], [0.9, 0.35], [0.77, 0.73], [0.03, 0.72], [0.02, 0.72]]
#         interval = [0.04, 0.04,0.02, 0.04, 0.04, 0.04]
#
#     type_index = 0
#     for i in range(3):
#         Y = []
#         if i == 0:
#             behind_title = 'combine'
#             type_index = 0
#         elif i == 1:
#             behind_title = 'praise'
#             type_index = 2
#         else:
#             behind_title = 'interrogation'
#             type_index = 4
#
#         for k in range(2):
#             Y = []
#             for j in range(5):
#                 Y.append(table.col_values(7*k + j + 1)[13 * i + 2:13 * i + 12])
#             if k == 0:
#                 ylabel = 'MAE'
#             else:
#                 ylabel = 'RMSE'
#             type_index = type_index + k
#             new_title = front_title + behind_title
#             print "new_title:",new_title
#             new_save_path = save_path + '_' + ylabel + '_' + new_title + '.xls'
#             print 'new_save_path',new_save_path
#             div_fig(X, Y, new_title, new_save_path, ncol, 'Matrix density', ylabel, labels, yrange = [0.5,0.95] + yranges[type_index],legend_anchor = legend_anchor[type_index],interval = interval[type_index])
#
# def start_pre_figrue_keshi():
#     file_path = '../matrix/实验.xlsx'
#     save_path = '../matrix/figure_exp/'
#     pre_figure(file_path.decode('utf-8'), 0, save_path + '1', ncol=1, front_title='endocrinology-')
#     pre_figure(file_path.decode('utf-8'), 1, save_path + '2', ncol=1, front_title='neurology-')
#
# if __name__ == '__main__':
#     # x = [0.05,0.1,0.15,0.2,4,5,6]
#     # x = []
#     # i = 1
#     # j = 10
#     # ratio = 0.05
#     # while (i < j + 1):
#     #     x.append(i * ratio)
#     #     i += 1
#     # y = [0.15115210377, 0.177500354242, 0.172957208709, 0.15865362297, 0.145334627407, 0.175018215143,
#     #      0.155588682501, 0.194563995557, 0.186758838895, 0.204637418947, 0.162845669289, 0.214903603,
#     #      0.187270467423, 0.214427698047, 0.220712075834, 0.198581263499, 0.209633389185, 0.237025676026, 0.188784967164]
#     # y1 = [0.155588682501, 0.155588682501, 0.155588682501, 0.155588682501, 0.155588682501, 0.155588682501, 0.155588682501
#     #     , 0.155588682501, 0.155588682501, 0.155588682501]
#     # y2 = [0.155588682501, 0.35588682501, 0.155588682501, 0.185588682501, 0.17558862501, 0.155588682501, 0.155588682501
#     #     , 0.555588682501, 0.155588682501, 0.5]
#     # # y = np.array(y)
#     # y = np.array(y)
#     # f = open("",r)
#     # print paint1(x, y1,'s','D://jj.jpg')
#
#     # rmse_mae_figure()
#     # sys_div_figure()
#     # start_pre_figrue_keshi()
#     print "start-div=================="
#     new_sys_div_figure()
#     # new_sys_div_figure('../matrix/sys_div_test.xls', ncol=2, titel='test')
