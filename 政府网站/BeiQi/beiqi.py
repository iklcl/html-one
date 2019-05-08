#-*- coding:utf-8 -*-
#网址：http://www.bjev.com.cn/dealers/findUs.htm?type=2
#文件名：beiqi.py
#作者: huanghong
#创建日期: 2017-10-18
#功能描述: 北汽新能源服务商
#完成状况：完成
import time
import json
import requests
from lxml import etree
import lxml.html
import sys
import codecs,csv
from bs4 import BeautifulSoup
import re
import sqlite3
import MySQLdb as db
import os.path
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest"
}
def get_id():
	data=[]
	req=requests.get('http://www.bjev.com.cn/api/dict/getRegion.ns?oid=',headers=headers).content
	lis = re.findall('(\[.*\])',req)[0]
	jd = json.loads(lis)
	for i in jd:
		dat=(str(i['oid']),i['name'])
		data.append(dat)
	return data
def get_city(iod,province):
	infornation=[]
	req=requests.get('http://www.bjev.com.cn/api/dict/getRegion.ns?oid=%s'%(iod),headers=headers).content
	lis = re.findall('(\[.*\])',req)[0]
	jd = json.loads(lis)
	for i in jd:
		dat=(province,i['name'])	
		infornation.append(dat)
	return infornation
def get_data(province,city):
	data={
	'province':province,
	'city':city,
	'type':'2',
	'dealerName':'',
	'modelsId':''
	}
	req=requests.post('http://www.bjev.com.cn/testDrive/initial.htm',headers=headers,data=data).content
	lis = re.findall('(\[.*\])',req)[0]
	jd = json.loads(lis)
	if len(jd)!=0:
		for i in jd:
			datas=[i['province'],i['city'],i['dealerName'],i['phone'],i['streetAddress'],i['longitude']+','+i['latitude']]
			savesqlcar_4s(datas,u'北汽新能源服务商.db')
def savesqlcar_4s(data,savepoint_name):
    #创建数据库
    con=sqlite3.connect(savepoint_name)
    con.execute('''CREATE TABLE IF NOT  EXISTS data
        (
        id integer primary key NOT NULL,
        province varchar(200) NOT NULL,
        city varchar(200) NOT NULL,
        district varchar(1000) DEFAULT NULL,
        company varchar(1000) DEFAULT NULL, 
        shopName varchar(1000) DEFAULT NULL,
        salesTel varchar(100) DEFAULT NULL,
        afterSalesTel varchar(100) DEFAULT NULL,
        RescueCall varchar(100) DEFAULT NULL,
        lng varchar(100) DEFAULT NULL,
        lat varchar(100) DEFAULT NULL,
        address varchar(1000) DEFAULT NULL,
        indexUrl varchar(100) DEFAULT NULL,
        fromUrl  varchar(100) DEFAULT NULL,
        others varchar(100) DEFAULT NULL, 
        jwd varchar(100) DEFAULT NULL,
        classify varchar(100) DEFAULT NULL);''')

    # 插入数据

    sql='insert into data(province,city,company,salesTel,address,jwd,classify)\
    values("%s","%s","%s","%s","%s","%s","%s")'%(data[0],data[1],data[2],data[3],data[4],data[5],'北汽新能源服务商')
    con.execute(sql)
    con.commit()
    con.close()


def main():
	data=get_id()
	# print data
	for t in data:
		datas=get_city(t[0],t[1])
		for i in datas:
			# print i[1]
			infornation=get_data(i[0],i[1])	

if __name__ == '__main__':
	main()			
