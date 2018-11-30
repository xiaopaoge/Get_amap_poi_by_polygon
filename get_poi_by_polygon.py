# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 17:10:24 2018

@author: zhouj
"""

import json
import xlwt
from datetime import datetime
from urllib import request
from urllib.parse import quote
import time
import os

#定义矩形边界的一个类
class Rec:
    def __init__(self,xmin,ymin,xmax,ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

# 获取数据
# base_url = http://restapi.amap.com/v3/place/polygon?polygon=
def get_data(pageindex,base_url,rec,types,key):
    global total_record
    # 暂停500毫秒，防止过快取不到数据
    time.sleep(0.5)
    print('解析页码： ' + str(pageindex) + ' ... ...')
    url = base_url+str(rec.xmin)+","+str(rec.ymin)+","+str(rec.xmax)+","+str(rec.ymax)+"&types="+types+"&key="+key+"&extensions=all&offset=25&page="+str(pageindex)
    # 中文编码
    print(url)
    url = quote(url, safe='/:?&=')
    html = ""
    with request.urlopen(url) as f:
        html = f.read()
        rr = json.loads(html)
        if total_record == 0:
            total_record = int(rr['count'])
        return rr['pois']    

def getPOIdata(page_size,json_name,base_url,rec,types,key):
    global total_record
    print('获取POI数据开始')
    josn_data = get_data(1,base_url,rec,types,key)
    if (total_record % page_size) != 0:
        page_number = int(total_record / page_size) + 2
    else:
        page_number = int(total_record / page_size) + 1

    with open(json_name, 'w') as f:
        # 去除最后]
        f.write(json.dumps(josn_data).rstrip(']'))
        for each_page in range(2, page_number):
            html = json.dumps(get_data(each_page,base_url,rec,types,key)).lstrip('[').rstrip(']')
            if html:
                html = "," + html
            f.write(html)
            print('已保存到json文件：' + json_name)
        f.write(']')
    print('获取POI数据结束')


# 写入数据到excel
def write_data_to_excel(json_name,hkeys,bkeys,name):
    # 获取当前日期
    today = datetime.today()
    # 将获取到的datetime对象仅取日期
    today_date = datetime.date(today)
    
    # 从文件中读取数据
    fp = open(json_name, 'r')
    result = json.loads(fp.read())
    # 实例化一个Workbook()对象(即excel文件)
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)

    # 创建表头
    # for循环访问并获取数组下标enumerate函数
    #for index, hkey in enumerate(hkeys):
    #    sheet.write(0, index, hkey)

    # 遍历result中的每个元素。
    for i in range(len(result)):
        values = result[i]
        n = i
        for index, key in enumerate(bkeys):
            val = ""
            # 判断是否存在属性key
            if key in values.keys():
                val = values[key]
            sheet.write(n, index, val)
    wbk.save(name + str(today_date) + '.xls')
    print('保存到excel文件： ' + name + str(today_date) + '.xls!')
    
def readRec(file):
    with open(file,encoding="utf-8") as f:
        return f.readlines()

if __name__ == '__main__':
    key = “”
    base_url = "http://restapi.amap.com/v3/place/polygon?polygon="
    json_name = 'data_amap.json'
    if not os.path.exists('poi_data'):
        os.makedirs('poi_data')
    typelist=["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","22","97","99"]
    for type0 in typelist:
        i=0
        types = type0+"0000"
        file = "E:/study/20181128/MapCutPoint/"+types+".txt"
        Reclist = readRec(file)
        for recpolygon in Reclist:
            i=i+1
            pol = recpolygon.split(",")
            rec = Rec(float(pol[0]),float(pol[1]),float(pol[2]),float(pol[3]))
            page_size = 25  # 每页记录数据，强烈建议不超过25，若超过25可能造成访问报错
            global total_record
            total_record = 0
            getPOIdata(page_size,json_name,base_url,rec,types,key)
            hkeys = ['id', '行业类型', '名称', '类型', '地址', '联系电话', 'location', '省份代码', '省份名称', '城市代码', '城市名称', '区域代码', '区域名称',
                 '所在商圈']
            # 获取数据列
            bkeys = ['id', 'biz_type', 'name', 'type', 'address', 'tel', 'location', 'pcode', 'pname', 'citycode', 'cityname',
                     'adcode', 'adname', 'business_area']
            write_data_to_excel(json_name,hkeys,bkeys,"poi_data\\"+types++"-"+str(i)+"-高德地图")
            if(i%13==0):
                time.sleep(30)
            elif(i%13!=0):
                time.sleep(10)
            