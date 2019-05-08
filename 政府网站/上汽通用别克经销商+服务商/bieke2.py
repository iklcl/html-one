#-*- coding:utf-8 -*-
#网址：http://www.buick.com.cn/service.html
#文件名：bieke.py
#作者: huanghong
#创建日期: 2017-010-25
#功能描述: 上汽通用别克服务商
#完成状况：完成
import threading
import json
import time
import requests
from lxml import etree
import lxml.html
import sys
import codecs,csv
import re
import sqlite3
import MySQLdb as db
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf-8')
headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest"
        }
def get_data():
	req=requests.get('http://www.buick.com.cn/api/service-shop.aspx',headers=headers).content
	lis = re.findall('(\[.*\])',req)[0]
	js=json.loads(lis)
	for i in js:
		data = [i['provinceName'],i['cityName'],i['dealerName'],i['tel'],i['address'],i['lat'],i['lng']]
		savesql(data,'上汽通用别克服务商.db')
	
def savesql(data,savepoint_name):
    #创建数据库
    con=sqlite3.connect(savepoint_name)
    con.execute('''CREATE TABLE IF NOT  EXISTS data
        (
        id integer primary key NOT NULL,
        province varchar(200) NOT NULL,
        city varchar(100) NOT NULL,
        company varchar(1000) DEFAULT NULL, 
        salesTel varchar(100) DEFAULT NULL,
        afterSalesTel varchar(100) DEFAULT NULL,
        RescueCall varchar(100) DEFAULT NULL,
        lng varchar(100) DEFAULT NULL,
        lat varchar(100) DEFAULT NULL,
        address varchar(1000) DEFAULT NULL,
        indexUrl varchar(100) DEFAULT NULL,
        fromUrl  varchar(100) DEFAULT NULL,
        others varchar(100) DEFAULT NULL, 
        classify varchar(100) DEFAULT NULL);''')

    # 插入数据
    sql='insert into data(province,city,company,salesTel,address,lng,lat,classify)\
    values("%s","%s","%s","%s","%s","%s","%s","%s")'%(data[0],data[1],data[2],data[3],data[4],data[5],data[6],u'上汽通用别克服务商')
    con.execute(sql)
    con.commit()
    con.close()
if __name__ == '__main__':
    get_data()    