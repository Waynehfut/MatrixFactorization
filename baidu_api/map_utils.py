# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:57:03 2017

@author: Administrator
"""
import json
import urllib as ur
import re
import pandas as pd #导入这些库后边都要用到
import sys
sys.path.append("E:\\Pycharm_Workspace\\lyqystj")
import cf.test as tt
ak = 'x3Esjm9x9UWjTt1irrVQ4ycEhkGwKXcp'

def getDuration(origin,destination):
    """
    经纬度:百度格式
    公共交通
    返回花费的时间，单位秒
    :param origin:目的地的经纬度
    :param destination:终点的经纬度
    :return:
    """
    global ak
    output = 'json'
    url = 'http://api.map.baidu.com/direction/v2/transit'
    uri = url + '?' + 'origin=' + origin + '&destination=' + destination +'&output=' + output +'&ak=' + ak
    print uri
    req = ur.urlopen(uri)
    res = req.read() #将其他编码的字符串解码成unicode
    temp = json.loads(res) #对json数据进行解析
    if temp['status'] == 0:
        try:
            duration = int(temp['result']['routes'][0]['duration'])
        except IndexError as e:
            print e.message
            duration = int(temp['result']['taxi']['duration'])
    else:
        url_d = 'http://api.map.baidu.com/routematrix/v2/driving'
        info_d = getRTD(origin, destination, url_d)  # 驾车
        duration = info_d[1]
    return duration

def getDistance(ori,hos_address,i):
    """
    返回的距离单位是米
    得到车程信息
    :param ori: 人的坐标（百度格式的）
    :param hos_address: 医院名或地址
    :param i =0 则要通过getlnglat()求医院的坐标，i=1则表明hos_address已是医院的坐标而不是医院名
    :return: 返回车程信息info_w[distance][duration] or info_d[]:0:distance;1:state;2:duration
    """
    if(i == 0):
        hos_lnglat = getlnglat(hos_address)
    else:
        hos_lnglat = hos_address
    url_r = 'http://api.map.baidu.com/routematrix/v2/riding'
    url_d = 'http://api.map.baidu.com/routematrix/v2/driving'
    info_r = getRTD(ori, hos_lnglat, url_r)#骑行
    info_d = getRTD(ori, hos_lnglat, url_d)#驾车
    if(info_r[0]<=1500):
        info_r.append('in range')
        info_r.append('riding')
        return info_r
    else:
        if(info_d[0]>20000):
            info_d.append('out of range')
            info_d.append('driving')
            return info_d
        info_d.append('in range')
        info_d.append('driving')
        return info_d

def getRTD(ori, dest, url):
    """
    经纬度使用默认的百度坐标格式
    :param ori: 人所在经纬度
    :param dest: 医院经纬度
    :param url:调用接口的url,对步行、驾车或骑行进行选择
    :return:info[0]:distance 单位米,info[1]:duration 单位秒
    """
    global ak
    info = list()
    # url = 'http://api.map.baidu.com/routematrix/v2/driving'
    # url = 'http://api.map.baidu.com/routematrix/v2/riding'
    # url = 'http://api.map.baidu.com/routematrix/v2/walking'
    origin = ori
    destination = dest
    output = 'json'
    uri = url + '?' + 'origins=' + origin + '&destinations=' + destination +'&output=' + output +'&ak=' + ak
    req = ur.urlopen(uri)
    res = req.read() #将其他编码的字符串解码成unicode
    temp = json.loads(res) #对json数据进行解析
    info.append(int(temp['result'][0]['distance']['value']))#数值的单位为米。若没有计算结果，值为0
    info.append(int(temp['result'][0]['duration']['value']))#数值的单位为秒。若没有计算结果，值为0
    return info

def getGTD(ori, dest):
    """
    经纬度默认使用百度坐标格式
    Geocoding API
    返回到医院的车程
    :param ori: 人所在经纬度
    :param dest: 医院经纬度
    :return: info[路程距离][时间] type:list
    """
    global ak
    info = list()
    url = 'http://api.map.baidu.com/direction/v2/transit'
    origin = ori
    destination = dest
    output = 'json'
    uri = url + '?' + 'origin=' + origin + '&destination=' + destination +'&output=' + output +'&ak=' + ak
    req = ur.urlopen(uri)
    res = req.read() #将其他编码的字符串解码成unicode
    temp = json.loads(res) #对json数据进行解析
    info.append(str(temp['result']['taxi']['distance']))
    info.append(str(temp['result']['taxi']['duration']))
    return info

def getlnglat(address):
    """
    调用百度地图的api得到医院经纬度

    :param address:地名
    :return: 地名经纬度，如"116.403119,39.937289"
    """
    global ak
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ret_coordtype = 'bd09ll'#坐标类型选择 bd09ll,gcj02ll,wgs84
    add = ur.quote(address) #由于本文城市变量为中文，为防止乱码，先用quote进行编码
    # print "address:",type(add.decode())
    uri = url + '?' + 'address=' + add + '&output=' + output + '&ret_coordtype='+ ret_coordtype +'&ak=' + ak
    req = ur.urlopen(uri)
    res = req.read() #将其他编码的字符串解码成unicode
    temp = json.loads(res) #对json数据进行解析
    if(str(temp['status']) == '0'):
        lng = temp['result']['location']['lng']
        lat = temp['result']['location']['lat']
        t = str(lng) + ',' + str(lat)
        t1 = str(lat)[0:str(lat).find('.') + 7] + ',' + str(lng)[0:str(lng).find('.') + 7]
    else:
        t1 = 'false'
    return t1

def getReverse_lnglat(location):
    """
    逆解析经纬度
    :param location:
    :return:city
    """
    global ak
    url = 'http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&output=json&'
    coordtype = 'bd09ll'#坐标类型选择 bd09ll,gcj02ll,wgs84
    # add = ur.quote(address) #由于本文城市变量为中文，为防止乱码，先用quote进行编码
    # print "address:",type(add.decode())
    uri = url +  '&location=' + location + '&coordtype='+ coordtype +'&ak=' + ak
    req = ur.urlopen(uri)
    res = req.read() #将其他编码的字符串解码成unicode
    print "res:", res[len(' renderReverse&&renderReverse(')-1:len(res)-1]
    temp = json.loads(res[len(' renderReverse&&renderReverse(')-1:len(res)-1]) #对json数据进行解析
    status = str(temp['status'])
    if(status == '0'):
        city = temp['result']['addressComponent']['city']
    else:
        city = 'false'
    return city

if __name__ == '__main__':
    # print sys.path
    # tt.pp()
    hos = "安徽省立医院南区"
    # pepole = '39.963633,116.429629'#北京
    pepole = '31.238152,121.436558'#上海
    #南京
    pepole = '32.062604,118.813988'
    #芜湖
    # pepole = '31.35681,118.424196'
    # hos_ll = '39.963633,116.423035'
    # hos_ll = '31.202939,121.463295'
    # print "hos_ll:",hos_ll
    # t = getDistance(pepole,hos)
    # # t = getDistance('31.238152,121.436558', '31.202939,121.463295')
    # print "type:",t[2]
    # print "range:",t[3]
    # print "distance:", t[0]
    # print "duration:",t[1]
    print getDuration('31.842039,117.276562','31.202939,121.463295')
    # print getlnglat('华北电力大学(保定)')