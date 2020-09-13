# -*- coding: utf-8 -*-
"""
Created on 2017/8/28 17:13
@file: update_filter.py
@author: Administrator
"""
import sys
sys.path.append("E:\\Pycharm_Workspace\\lyqstj\\methon")
import confact as cdb
import map_utils as map
import re
import time
import tool.ULog as lg

def update():
    sql1 = "select id,yiyuan from doc_msg3 "
    sql4 = "update doc_msg3 set city = %s,lnglat = %s where id = %s"
    db = cdb.DatabaseConnection()
    cur,con = db.dbConnect('lyqystj')
    cur.execute(sql1)
    all_hos = cur.fetchall()
    hos = []
    for i in all_hos:
        temp = []
        print 'hos:',i[1]
        print 'hos_type:',type(i[1].encode('utf-8'))
        lnglat = map.getlnglat(i[1].encode('utf-8'))
        if(lnglat != 'false'):
            city = map.getReverse_lnglat(lnglat)
            temp.append(city)  # city
            temp.append(lnglat)  # lnglat
            temp.append(i[0])
            hos.append(temp)
    cur.executemany(sql4,hos)
    con.commit()
    cur.close()
    print '插入完成'

def update_hos():
    sql1 = "select id,yiyuan from doc_msg3 "
    sql4 = "update doc_msg3 set yiyuan = %s where id = %s"
    db = cdb.DatabaseConnection()
    cur,con = db.dbConnect('lyqystj')
    cur.execute(sql1)
    all_hos = cur.fetchall()
    hos = []
    for i in all_hos:
        temp = []
        # print "type:",type(i[1])
        t = i[1].encode('utf-8').replace(' ','')
        print "t:",t
        temp.append(t)#yiyuan
        temp.append(i[0])#id
        hos.append(temp)
    cur.executemany(sql4,hos)
    con.commit()
    cur.close()
    print '插入完成'

def update_university_latlng():
    sql1 = "select id,university from university_list where id > '234' "
    sql4 = "update university_list set latlng = %s where id = %s"
    db = cdb.DatabaseConnection()
    cur,con = db.dbConnect('lyq_sy_db')
    cur.execute(sql1)
    all_university = cur.fetchall()
    univer = []
    for i in all_university:
        temp = []
        # print "type:",type(i[1])
        # university_id = i[0]
        name = i[1].encode('utf-8')
        latlng = map.getlnglat(name)
        temp.append(latlng)#坐标
        temp.append(i[0])#id
        univer.append(temp)
    cur.executemany(sql4,univer)
    con.commit()
    cur.close()
    print '插入完成'

def update_university_hos_duration():
    # log = lg.Log('D://yiyuan.txt')
    # f = log.get_log()
    sql1 = "select university,latlng from university_list where id >= '276' and id <= '295'"
    sql2 = "select yiyuan,lnglat from doctor_hos"
    sql3 = "insert into people_hospital_duration(school_name,hos_name,duration) values(%s, %s, %s)"
    db = cdb.DatabaseConnection()
    cur, con = db.dbConnect('lyq_sy_db')
    cur.execute(sql1)
    all_university = cur.fetchall()
    cur.execute(sql2)
    all_hospital = cur.fetchall()
    number = 1
    for university in all_university:
        durations = []
        print "university:%s 第%s个:" % (university[0].encode('utf-8'),number)
        for hospital in all_hospital:
            duration = map.getDuration(university[1],hospital[1])
            temp = []
            # print "type:",type(i[1])
            # university_id = i[0]
            temp.append(university[0])  # 学校名
            temp.append(hospital[0])  # 医院名
            temp.append(duration)  # 车程
            durations.append(temp)
        number += 1
        time.sleep(180)
        cur.executemany(sql3, durations)
        con.commit()
    # temp = []
    # temp.append('中国')  # 医院名
    # temp.append('死者')  # 学校名
    # temp.append(555)  # 车程
    # durations.append(temp)
    cur.close()
    print '插入完成'

if __name__ == '__main__':
    # update_hos()
    # update_university_latlng()
    update_university_hos_duration()#276-295

    #universitys = ['上海海事大学','济南大学','天津工业大学','天津师范大学','中国计量大学','常州大学','安徽外国语学院','安徽行政学院']
    #