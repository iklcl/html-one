#coding=utf-8

#文件名称：city118.py
#作者：huanghong
#创建日期：2018-3-21
#功能描述：都市酒店集团信息搜索
#网页地址：http://www.118inns.com/new/HotelList.aspx?city=%E9%9D%92%E5%B2%9B
#处理进度：已完成（待优化）


import requests,random,time,json
from lxml import etree
import sys
import codecs,csv
import re
import os.path
import sqlite3
import MySQLdb as db
from datetime import datetime
import gevent  
from multiprocessing import Pool,Lock,Process
import multiprocessing
reload(sys)
sys.setdefaultencoding('utf-8')
se = requests.session()

headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest'
}
headers1={
'Accept':'application/json, text/javascript, */*',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'Content-Length':'91',
'Content-Type':'application/json; charset=UTF-8',
'Cookie':'UM_distinctid=162463a340e4cc-0a3c5849d88325-4540002c-13c680-162463a340f34e; CNZZDATA1258123502=673298807-1521596441-http%253A%252F%252Fwww.118inns.com%252F%7C1521596441',
'Host':'www.118inns.com',
'Origin':'http://www.118inns.com',
'Referer':'http://www.118inns.com/new/HotelList.aspx?city=%E9%9D%92%E5%B2%9B',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
'X-Requested-With':'XMLHttpRequest'
}

def savesql_hotel(data,savepoint_name):
    #创建数据库
    con=sqlite3.connect(savepoint_name)
    con.execute('''CREATE TABLE IF NOT  EXISTS data
        (
        hoteltype varchar(200) NOT NULL,
        province varchar(200) NOT NULL,
        city varchar(200) NOT NULL,
        name varchar(1000) DEFAULT NULL,
        address varchar(1000) DEFAULT NULL,
        salesTel varchar(100) DEFAULT NULL, 
        lat varchar(100) DEFAULT NULL,
        lng varchar(100) DEFAULT NULL,
        Url  varchar(1000) DEFAULT NULL);''')
    # 插入数据
    sql='insert into data(hoteltype,province,city,name,address,salesTel,Url)\
    values("%s","%s","%s","%s","%s","%s","%s")'%(u'都市酒店集团',data[0],data[1],data[2],data[3],data[4],data[5])
    con.execute(sql)
    con.commit()
    con.close()

def get_city():
	data=[]
	jstext=se.get('http://www.118inns.com/js/strcity.js?v=1',headers=headers).content
	# print jstext
	text=re.findall('"(.*)"',jstext)
	for i in  text[0].strip('@').split('@'):
		data.append(i.split('|')[1])
	return data	
# get_city()
def get_data(city):
	page=0
	while True:
		page+=1
		payload={
		"city":city, 
		"storeName":"", 
		"cardTypeName":"", 
		"dtB":"", 
		"dtE":"", 
		"pageSize":"5",
		"pageIndex":page
		}
		data=json.dumps(payload)
		cont=se.post('http://www.118inns.com/new/HotelList.aspx/GetStoInfoAndRoomRateList',headers=headers1,data=data)
	
		text=json.loads(cont.content)
		li=text['d']["DataList"]
		if len(li)==0:
			break
		for i in li[0]:
			url='http://www.118inns.com/new/HotelDetail.aspx?StoreId=%s'%i[1]
			data=[i[6],i[7],i[12]+i[2],i[8],i[5],url]

			# try:
			# 	print i[6],i[7],i[2],i[8],i[5]
			# except Exception as e:
			# 	print cont.content
			
			savesql_hotel(data,u'都市酒店集团.db')
def main():
	city=get_city()
	for i in city:
		print i
		get_data(i)
if __name__ == '__main__':
	main()
