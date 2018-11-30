###通过切块爬取高德地图POI数据###

Tips：通过城市名爬取高德地图POI详见https://github.com/zhoujungis/amap_poi_scrapy

1. 运行cutmap.py，将整个大块区域分割成POI数据不超过720条的小区域（修改路径，Key）
2.运行get_poi_by_polygon.py，分块爬取数据（修改路径，Key）
3.去除所有表头，只保留一个，然后使用excel_merge.py合并所有的excel（修改对应的路径）
4.数据分列，将location分为lon和lat两列
5.使用huoxing2wgs84.py进行坐标转换，转化为wgs1984，然后利用arcgis转化为shape文件，all done！！！（修改对应的路径）