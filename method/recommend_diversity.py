# -*- coding: utf-8 -*-
"""
Created on 2018/1/19 15:14
@file: recommend_diversity.py
@author: Administrator
"""
from __future__ import division
import log
from confact import *
import numpy as np
import math
import baidu_api.map_utils as bdm
import tool.math_method as mathm
import tool.sorted_utils as sorted

class Recommend_Server(object):
    """

    """
    def __init__(self,disease = "", matrix = "", table_name = "", people_locat = ""):
        self.hos_rank_key = {'9': 1, '8': 2, '7': 3, '6': 4, '5': 5, '4': 6, '3': 7, '2': 8, '1': 9}
        self.scort = []
        self.tt = []
        self.length = 0
        self.cal = 0
        self.or_matrix = []

        self.disease = disease
        self.matrix = matrix
        self.table_name = table_name
        self.people_locat = people_locat

    def getResult1(self):
        """
        得到最终结果
        :param matrix:预测的矩阵
        :param disease: 疾病
        :return:
        """

       #  logs = log.Log()
       #  logs.start_log \
       #      ("../matrix/" + self.table_name[3:].decode('utf-8') + "/" + "预测排序结果.txt".decode('utf-8'),self.disease )
       #  f = logs.write_log()
       #  """
       #  doc_info：[[doc_id,doc_name,hos_name,rank,hos_locat,score]]
       #  filter_hos_By_sorted100：根据排名筛选符合条件的医生信息
       # """
        # 得到医院的排名
        final_hos_rank = self.filter_hos_by_sorted(self.table_name)
        # 得到预测填充后的评分
        forecast_socre = self.matrix_score_by_disease(self.disease, self.table_name, self.matrix)
        # 得到的医生信息，但不包含预测填充后的评分 doc_info：[[doc_id,doc_name,hos_name,rank,hos_locat]]
        doc_info_un = self.get_doc_info(self.table_name,final_hos_rank)
        #添加车程信息并排除掉超出指定车程范围的医院的医生, doc_info：[[doc_id,doc_name,hos_name,rank,hos_locat,duration]]
        doc_info = self.filter_by_duration(doc_info_un)
        #得到对应疾病最终的医生信息, doc_info：[[doc_id,doc_name,hos_name,rank,hos_locat,duration,socre]]
        doc_info = self.add_score(doc_info_un,forecast_socre)
        #last_result:[index]按weight降序排列后的
        last_result = self.weighth_with_duration(doc_info)

        # start输出未进行多样性前的排序
        # f = log.write_log()
        # print "预测后顺序======================================================="
        # for doc in doc_info:
        #     print ("%-20s%-20s" % (doc[1].encode('utf-8'), doc[2].encode('utf-8')))
        #
        # print "完成筛选指定距离以内的医院"
        # end输出


        # start输出最终结果
        # f = log.write_log()
        # print >> f, "疾病：", self.disease
        # print >> f, ("%-20s%-20s" % ("姓名", "医院"))
        # for doc in last_result:
        #     print >> f, ("%-20s%-20s" % (doc[1].encode('utf-8'), doc[2].encode('utf-8')))
        # end输出
        return last_result

    def filter_hos_by_sorted(self,table_name):
        """
        返回table_name中各个医院的排名
        :param table_name:
        :return:{"hos_name":rank}
        """
        # 医院信息,hos_rank:[hos_name,hos_rank]
        hos_rank = []
        n_in_has_add = set()
        # 记录不在排名内的医生信息
        hos_rank_n_in_sorted = []

        # sql1 = "select id,yiyuan,score from {0} a,doc_msg3 b where  "
        sql1 = "select DISTINCT(b.yiyuan),b.score from {0} a,doc_msg3 b where a.id = b.id"
        sql2 = "SELECT s.id,s.hos_name from hos_scort s "
        db = DatabaseConnection()
        cur = db.dbConnect()
        #V1 sql1 = sql1.format(self.table_name, self.city)
        sql1 = sql1.format(table_name)
        cur.execute(sql1)

        hoss = cur.fetchall()

        # 开始筛选,筛选条件：city，100排名内医院中的医生
        sql2 = sql2.format(table_name)
        cur.execute(sql2)
        include_hos_name = cur.fetchall()
        for hos in hoss:
            li = []
            has_judge = 0
            for name in include_hos_name:
                #doc[0],name[1]值均为医院名
                if hos[0] == name[1]:
                    # hos_name
                    li.append(hos[0])
                    # rank 排名 id
                    li.append(name[0])
                    # rank 按指定顺序来 用rank_i来操作
                    # li.append(name[0])
                    hos_rank.append(li)
                    has_judge = 1
                    break
            if has_judge == 0:
                # hos_name
                li.append(hos[0])
                # doc[2]医院的等级
                li.append(self.hos_rank_key[str(hos[1])])
                hos_rank_n_in_sorted.append(li)

        cur.close()
        # doc_len = len(hos_rank)

        # print len(hos_rank_n_in_sorted)
        # print hos_rank_n_in_sorted[0]
        hos_rank_type_sum = self.static_type_sum(hos_rank_n_in_sorted,1)
        present_max_rank = mathm.get_max_by_index(hos_rank,1) #当前排名
        present_rank = present_max_rank
        #不在100名内的医院排名
        left_hos_rank_dic = {}
        #循环后得到不在100名以内的医院的排名，按医院等级排的
        for rank,type_num in hos_rank_type_sum.items():
            if present_rank == present_max_rank:
                present_rank = present_rank + 1
                left_hos_rank_dic[str(rank)] = present_rank
                pre_type_num = type_num
            else:
                present_rank = present_rank + pre_type_num
                left_hos_rank_dic[str(rank)] = present_rank
                pre_type_num = type_num

        for hos in hos_rank_n_in_sorted:
            hos[1] = left_hos_rank_dic[str(hos[1])]
            hos_rank.append(hos)

        min_rank = mathm.get_min_by_index(hos_rank,1)
        #统一往前移(min_rank-1)位
        final_hos_rank = {}
        for hos in hos_rank:
            #若有排名1,则不前移
            if min_rank == 1:
                final_hos_rank[hos[0]] = hos[1]
            else:
                final_hos_rank[hos[0]] = hos[1] - (min_rank - 1)

        # for name,val in final_hos_rank.items():
        #     print ("name:%s,val:%s"%(name,val))
        return final_hos_rank

    def matrix_score_by_disease(self,disease,table_name,matrix):
        """
        返回矩阵matrix中对应疾病的预测评分
        :param disease: 疾病名
        :param table_name: 表名
        :param matrix: 预测填充后的矩阵
        :return: score:{"hos_id":point}
        """
        # column用来计算是第几行
        column = 0
        # 矩阵的第几列
        row = -1
        # score {'id':'score'}
        score = {}
        db = DatabaseConnection()
        cur = db.dbConnect()
        #start得到对应列的疾病信息
        sql3 = "select * from {0}"
        sql3 = sql3.format(table_name)
        cur.execute(sql3)
        ids = cur.fetchall()
        #得到疾病disease在矩阵中的第几列
        temp_r = -1
        disease = '高血压'
        for name in cur.description:
            temp_r = temp_r + 1
            if (temp_r > 1):
                row = row + 1
                if name[0] == disease:
                    break;
        # end
        for id in ids:
            # print 'column:',column
            score[id[0]] = matrix[column][row]
            column = column + 1

        return score

    def get_doc_info(self,table_name,hos_rank):
        """
        加上医院的排名信息，得到医生的信息，内容格式为[[doc_id,doc_name,hos_name,rank,locat]]
        :param table_name:
        :param score_dict:
        :param hos_rank:{"hos_name":rank}
        :return: [[doc_id,doc_name,hos_name,rank,locat]]
        """
        # 医生信息
        doc_info = []
        db = DatabaseConnection()
        cur = db.dbConnect()
        sql1 = "select a.id,a.name,b.yiyuan,b.score,b.lnglat from {0} a,doc_msg3 b where a.id = b.id "
        sql1 = sql1.format(table_name)
        cur.execute(sql1)
        docs = cur.fetchall()
        for doc in docs:
            li = []
            # doc_id
            li.append(doc[0])
            # doc_name
            li.append(doc[1])
            # hos_name
            li.append(doc[2])
            # rank 医院的排名,doc[2]医院名
            li.append(hos_rank[doc[2]])
            # hos 坐标
            li.append(doc[4])
            doc_info.append(li)

        cur.close()
        return doc_info

    def add_score(self,doc_info,score_dict):
        """
        在医生信息中加入预测填充后的评分
        :param doc_info:
        :param score_dict:{"doc_id",score}
        :return: doc_info：[[doc_id,doc_name,hos_name,rank,hos_locat,score]]
        """
        for doc in doc_info:
            doc.append(score_dict[doc[0]])
        return doc_info

    def filter_hos_by_sorted100_1(self,table_name, matrix, disease):
        """
        限制条件：city,若要扩充则改变sql语句
        :param table_name:
        :param matrix:
        :param disease:
        :param city:
        :return:[[doc_id,doc_name,hos_name,score,rank,locat]]
        """
        global hos_rank
        # column用来计算是第几行
        column = 0
        # 矩阵的第几列
        row = -1
        # score {'id':'score'}
        score = {}
        # 医生信息
        doc_info = []
        # 记录不在排名内的医生信息
        doc_info_n_in_sorted = []

        # sql1 = "select b.yiyuan,b.score,b.lnglat,a.* from {0} a,doc_msg3 b where a.id = b.id and b.city like %%%%%s%%%%%"%city
        #V1 sql1 = "select b.yiyuan,b.score,b.lnglat,a.* from {0} a,doc_msg3 b where a.id = b.id and b.city = \'{1}\'"
        sql1 = "select b.yiyuan,b.score,b.lnglat,a.* from {0} a,doc_msg3 b where a.id = b.id "
        # sql2 = "SELECT s.id,s.hos_name from doc_msg3 a,hos_scort s,{0} t where a.yiyuan = s.hos_name  and a.city LIKE '%"+"{1}"+"%'and a.id = t.id"
        sql2 = "SELECT s.id,s.hos_name from hos_scort s where s.id < 21"
        sql3 = "select * from {0}"
        db = DatabaseConnection()
        cur = db.dbConnect()
        #V1 sql1 = sql1.format(self.table_name, self.city)
        sql1 = sql1.format(table_name)
        cur.execute(sql1)

        docs = cur.fetchall()
        # 得到对应列的疾病信息
        sql3 = sql3.format(table_name)
        cur.execute(sql3)
        ids = cur.fetchall()
        # 得到疾病disease在矩阵中的第几列
        tempi = 0
        for name in cur.description:
            row = row + 1
            if (tempi >= 3):
                if name[0] == disease:
                    break;
            tempi = tempi + 1
        # end

        for id in ids:
            score[id[0]] = matrix[column][row]
            column = column + 1

        # 开始筛选,筛选条件：city，100排名内医院中的医生
        sql2 = sql2.format(table_name)
        cur.execute(sql2)
        include_hos_name = cur.fetchall()
        li = []
        for doc in docs:
            # doc_id
            li.append(doc[3])
            # doc_name
            li.append(doc[4])
            # hos_name
            li.append(doc[0])
            # score,     doc[3]为doc_id
            li.append(score[doc[3]])
            #has_judge判断医院是否在100名中，并已被添加到li中
            has_judge = 0
            for name in include_hos_name:
                #doc[0],name[1]值均为医院名
                if doc[0] == name[1]:
                    # rank
                    li.append(name[0])
                    # hos 坐标
                    li.append(doc[2])
                    doc_info.append(li)
                    has_judge = 1
                    break
            if has_judge == 1:
                # doc[1]医院的等级
                li.append(self.hos_rank_key[str(doc[1])])
                # hos 坐标
                li.append(doc[2])
                doc_info_n_in_sorted.append(li)
                has_judge = 0
            li = []

        cur.close()
        doc_len = len(doc_info)

        hos_rank_type_sum = self.static_type_sum(doc_info_n_in_sorted,4)
        present_rank = doc_len #当前排名
        #不在100名内的医院排名
        left_hos_rank_dic = {}
        #循环后得到不在100名以内的医院的排名，按医院等级排的
        for rank,type_num in hos_rank_type_sum.items():
            if present_rank == doc_len:
                left_hos_rank_dic[str(rank)] = present_rank
                pre_type_num = type_num
            else:
                present_rank = present_rank + pre_type_num
                left_hos_rank_dic[str(rank)] = present_rank
                pre_type_num = type_num

        for doc in doc_info_n_in_sorted:
            doc[4] = left_hos_rank_dic[str(doc[4])]
            doc_info.append(doc)
        return doc_info

    def weighth_with_duration(self,doc_info):
        """
        doc_info:[[doc_id,doc_name,hos_name,rank,hos_locat,duration,socre]]
        :param doc_info:医生信息
        :return:[index,...,index],doc_info:[[doc_id,doc_name,hos_name,rank,hos_locat,duration,socre,utility]]
        """
        # # 总评分
        # c_sum = mathm.get_sum_by_index(doc_info, 6)
        # 得到对应列的最大值
        c_max = mathm.get_max_by_index(doc_info, 6)
        # 医院最低排名
        hos_lowest = mathm.get_maxormin_by_index(doc_info, 3, "max")
        # 最远车程
        max_duration = mathm.get_maxormin_by_index(doc_info, 5, "max")
        # hos_dic:医院数量信息
        hos_dic = self.static_type_sum(doc_info,2)
        hos_sum = len(hos_dic)
        ls_sort = []
        i = 0
        while i < len(doc_info):
            li = []
            # w_c = doc_info[i][6] / c_sum
            w_c = doc_info[i][6] / c_max
            w_h = int(hos_dic[doc_info[i][2]])/hos_sum * (-doc_info[i][3] / (hos_lowest + 1) + 1)
            temp_d = doc_info[i][5] / (max_duration + 1)
            w_d = (1 - temp_d) * math.exp(-(doc_info[i][5] / max_duration))
            # ls_sort[doc_info[i][0]] = w_c * w_h * w_d
            utility = w_c * w_h * w_d
            li.append(i)
            li.append(utility)
            doc_info[i].append(utility)
            ls_sort.append(li)
            i += 1
        ls_sorted = sorted.sort_by_index(ls_sort,1)
        new_ls_sorted = []
        for li in ls_sorted:
            new_ls_sorted.append(li[0])
        # print "new_ls_sorted:",new_ls_sorted
        return new_ls_sorted,doc_info

    def filter_by_sql_duration(self, people_location, doc_info):
        """
        添加车程信息，并删除掉不符合指定车程范围内的doc_info
        doc_info:[[doc_id,doc_name,hos_name,rank,hos_locat]]
        返回docs形式的指定车程内的医院的医生
        :param people_location:人所在的地址名
        :param doc_info:
        :param index:doc_info中坐标信息所在的doc_index,即列
        :return: [[doc_id,doc_name,hos_name,rank,hos_locat,dis]]
        """

        db = DatabaseConnection()
        cur = db.dbConnect()
        sql = "select duration from people_hospital_duration where school_name = \'{0}\' and hos_name = \'{1}\'"

        temp_doc_info = []
        hos_set = self.get_hos_set(doc_info,2,4)
        people_hospital_duration = {}
        un_caculate_hospital = set()
        for hos in hos_set:
            # print "people_location:", people_location
            # print "doc[index]:", str(doc[doc_index])
            if hos[0] not in un_caculate_hospital:
                # 人的位置(学校)，医院名
                # s = sql.format('中国科学技术大学', '南京脑科医院')
                # print "people_location:", people_location[0]
                # print "hos[0]:", hos[0]
                s = sql.format(people_location[0].encode('utf-8'),hos[0].encode('utf-8'))
                cur.execute(s)
                re = cur.fetchall()
                # print re
                duration = re[0][0]
                # 指定医院的车程，大于指定车程的则去掉，7个小时
                if duration > 25200:
                    un_caculate_hospital.add(hos)
                else:
                    people_hospital_duration[hos[0]] = duration
            else:
                pass
        cur.close
        #将在people_hospital_duration中的医院的车程信息添加到医院信息中
        for doc in doc_info:
            if people_hospital_duration.has_key(doc[2]):
                li = list(doc)
                li.append(int(people_hospital_duration[doc[2]]))
                temp_doc_info.append(li)
            else:
                pass
        return temp_doc_info,people_hospital_duration

    def filter_by_duration(self, people_location, doc_info):
        """
        添加车程信息，并删除掉不符合指定车程范围内的doc_info
        doc_info:[[doc_id,doc_name,hos_name,rank,hos_locat]]
        返回docs形式的指定车程内的医院的医生
        :param people_location:
        :param doc_info:
        :param index:doc_info中坐标信息所在的doc_index,即列
        :return: [[doc_id,doc_name,hos_name,rank,hos_locat,dis]]
        """
        temp_doc_info = []
        i = 0
        hos_set = self.get_hos_set(doc_info,2,4)
        # print "请求次数：", len(hos_set)
        people_hospital_duration = {}
        un_caculate_hospital = set()
        for hos in hos_set:
            # print "people_location:", people_location
            # print "doc[index]:", str(doc[doc_index])
            if hos[1] not in un_caculate_hospital:
                # 人的坐标，医院坐标
                duration = bdm.getDuration(people_location, hos[1])
                # 指定医院的车程，大于指定车程的则去掉，5个小时
                if duration > 18000:
                    un_caculate_hospital.add(hos)
                else:
                    people_hospital_duration[hos[0]] = duration
            else:
                pass
        #将在people_hospital_duration中的医院的车程信息添加到医院信息中
        for doc in doc_info:
            if people_hospital_duration.has_key(doc[2]):
                li = list(doc)
                li.append(int(people_hospital_duration[doc[2]]))
                temp_doc_info.append(li)
            else:
                pass
        return temp_doc_info,people_hospital_duration

    def static_type_sum(self,info,index):
        """
        返回info中按指定的index内容统计的分类数量，以dic形式返回,{"type":num}
        :param info: 包含医院名信息的二维数组
        :param index: 医院名在第二维中的位置
        :return: :{"type":num}
        """
        dic = {}
        t = list(info)
        hos = 0
        while hos < len(t):
            name = t[hos][index]
            t.pop(hos)
            i = 1
            if (len(t) == 0):
                dic[name] = i
                break;
            j = 0
            while j < len(t):
                if (t[j][index] == name):
                    i += 1
                    t.pop(j)
                    j = j - 1
                    if (len(t) == 0):
                        dic[name] = i
                        break;
                j += 1
            dic[name] = i
        # for key, values in dic.items():
        #     print "k:", key
        #     print "v:", values
        return dic

    def static_hos_type(self,docs, hos_index,id_index):
        """
        返回docs中各个级别的医院数量，以dic形式返回,{"rank":num}
        :param docs: 包含医院名信息的二维数组
        :param hos_index: 医院名在第二维中的位置
        :param id_index: 医生id在第二维中的位置
        :return: :{"rank":num}
        """
        dic = {}
        t = list(docs)
        hos = 0
        while hos < len(t):
            name = t[hos][hos_index]
            id = t[hos][id_index]
            # hos_doc[name] = []
            t.pop(hos)
            i = 1
            if (len(t) == 0):
                dic[name] = i
                break;
            # print "name:", name
            j = 0
            #循环遍历医院名等于name的信息，并去掉医院名等于name的信息
            while j < len(t):
                # print 't[j][hos_index]', t[j][hos_index]
                # print "j:", j
                if (t[j][hos_index] == name):
                    i += 1
                    t.pop(j)
                    j = j - 1
                    if (len(t) == 0):
                        dic[name] = i
                        break;
                j += 1
            dic[name] = i
        # for key, values in dic.items():
        #     print "k:", key
        #     print "v:", values
        # print "----------------------hos_dict：", dic
        return dic

    def calcaulat_diversity_one(self,doc_filter):
        """
        计算权重
        :param doc_filter: [[doc_id,doc_name,hos_name,score,rank,hos_locat,dis]]
        :return: [[doc_id,doc_name,hos_name,score,rank,hos_locat,dis]]
        """
        # 总评分
        # c_sum = mathm.get_sum_by_index(doc_filter, 3)
        # # 医院最低排名
        # hos_lowest = mathm.get_maxormin_by_index(doc_filter, 4, "max")
        # # 最远路程
        # dis_max = mathm.get_maxormin_by_index(doc_filter, 6, "max")
        # ls_sort = {}
        # i = 0
        # while i < len(doc_filter):
        #     w_c = doc_filter[i][3] / c_sum
        #     w_h = -doc_filter[i][4] / (hos_lowest + 1) + 1
        #     temp_d = doc_filter[i][6] / (dis_max + 1)
        #     w_d = (1 - temp_d) * math.exp(-temp_d)
        #     ls_sort[doc_filter[i][0]] = w_c * w_h * w_d
        #
        #     # ls_sort[doc_filter[i][0]] = w_c * w_h
        #     i += 1
        # i = 0
        # ls_sorted = sort_by_value(ls_sort)
        # hos_dic = gethosdic(doc_filter, 2)
        # # 排序
        # doc_filter_sorted = sorted_by_sorted(doc_filter, ls_sorted)
        # while i < len(doc_filter_sorted):
        #     hos_dic_sum = gethoss(hos_dic)
        #     ls_sorted[i][1] = ls_sorted[i][1] * hos_dic[doc_filter_sorted[i][2]] / hos_dic_sum
        #     hos_dic[doc_filter_sorted[i][2]] -= 1
        #     i += 1
        # ls_sorted = sort_desc(ls_sorted)
        # re = sorted_by_sorted(doc_filter, ls_sorted)
        # return re

    def sorted_by_index(self,doc_info, ls_sorte):
        """
        根据ls_sorte顺序排doc_info的顺序，并返回排序后的doc_info
        :param doc_info:
        :param ls_sorte:
        :return:
        """
        docs = []
        for doc in ls_sorte:
            #doc[0],顺序号
            docs.append(doc_info[doc[0]])
        return docs

    def sorted_by_sorted(self,doc_info, ls_sorte):
        """
        根据ls_sorte顺序排doc_info的顺序，并返回排序后的doc_info
        :param doc_info:
        :param ls_sorte:
        :return:
        """
        docs = []
        for doc_l in ls_sorte:
            for i in doc_info:
                if i[0] == doc_l[0]:
                    docs.append(i)
        return docs

    def get_hos_set(self, doc_info,i,j):
        """
        返回doc_info中所有的医院
        :param doc_info:
        :param i: 医院名序序列号
        :param j: 医院坐标序列号
        :return: set((医院名,医院坐标))
        """
        hos = set()
        for doc in doc_info:
            hos.add((doc[i],doc[j]))
        return hos

    def get_disease(self, table_name):
        """
        得到矩阵中的所有的疾病
        :param table_name:
        :return: [disease,...,disease]
        """
        diseases = []
        sql3 = "select * from {0}"
        db = DatabaseConnection()
        cur = db.dbConnect()
        # 得到对应列的疾病信息
        sql3 = sql3.format(table_name)
        cur.execute(sql3)
        ids = cur.fetchall()
        # 得到矩阵中的所有疾病，diseases
        tempi = 0
        for name in cur.description:
            if (tempi >= 3):
                diseases.append(name[0])
            tempi += 1
        # end
        cur.close()
        return diseases

    def get_university_sql(self, table_name,sql):
        """
        得到表中的所有的学校名及坐标
        :param table_name:
        :return: [[name,latlng]...]
        """
        tempi = []
        db = DatabaseConnection()
        cur = db.dbConnect()
        # 得到对应列的疾病信息
        # sql = sql.format(table_name)
        cur.execute(sql)
        univerities = cur.fetchall()
        tempi = []
        for i in univerities:
            li = []
            li.append(i[1])#名字
            li.append(i[2])#坐标
            tempi.append(li)
        # end
        cur.close()
        return tempi

    def get_university(self, table_name):
        """
        得到表中的所有的学校名及坐标
        :param table_name:
        :return: [[name,latlng]...]
        """
        tempi = []
        sql = "select  *  from university_list where id <147"
        db = DatabaseConnection()
        cur = db.dbConnect()
        # 得到对应列的疾病信息
        # sql = sql.format(table_name)
        cur.execute(sql)
        univerities = cur.fetchall()
        tempi = []
        for i in univerities:
            li = []
            li.append(i[1])#名字
            li.append(i[2])#坐标
            tempi.append(li)
        # end
        cur.close()
        return tempi


if __name__ == '__main__':
    t = [['中'],['中'],['2'],['4'],['中']]
    recommend_server = Recommend_Server()
    # dic = recommend_server.static_type_sum(t,0)
    t = recommend_server.get_disease('tp_神经内科')
    print len(t)
    print t[0]
