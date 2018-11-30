# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 18:48:19 2018

@author: zhouj
"""

import requests
import time
import json

def DownloadHtml(url):
    request = requests.get(url=url, timeout=(5, 27))
    html = request.text
    request.close()
    return html

#base_url=http://restapi.amap.com/v3/place/polygon?polygon=
#url=http://restapi.amap.com/v3/place/polygon?polygon=108.640287,26.043184;110.579374,27.275355&key=你的KEY&extensions=all&offset=5&page=1
def CutChina(xmin,ymin,xmax,ymax,base_url,types,key):
    url = base_url+str(xmin)+","+str(ymin)+";"+str(xmax)+","+str(ymax)+"&types="+types+"&key="+key+"&extensions=all&offset=5&page=1"
    file = "MapCutPoint/"+types+".txt"
    data = DownloadHtml(url=url)
    jsonData=json.loads(data)
    count=int(jsonData["count"])
    print(count)
    if(0<count<721):
        with open(file,"a") as f:
            f.writelines(str(xmin)+","+str(ymin)+","+str(xmax)+","+str(ymax)+"\n")
            time.sleep(2)
            print("已写入"+types+".txt")
    elif(count>720):
        midX = (xmin+xmax)/2
        midY = (ymin+ymax)/2
        time.sleep(1)
        CutChina(xmin,ymin,midX,midY,base_url,types,key)
        time.sleep(1)
        CutChina(midX,ymin,xmax,midY,base_url,types,key)
        time.sleep(1)
        CutChina(xmin,midY,midX,ymax,base_url,types,key)
        time.sleep(1)
        CutChina(midX,midY,xmax,ymax,base_url,types,key)

if __name__ == "__main__":
    key = “”
    base_url = "http://restapi.amap.com/v3/place/polygon?polygon="
    #typelist=["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","22","97","99"]
    typelist = ["01"]
    for type0 in typelist:
        types = type0+"0000"
        CutChina(71.234018,17.725738,136.139681,55.28893,base_url,types,key)
