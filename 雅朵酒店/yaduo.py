#coding=utf-8

#文件名称：yaduo.py
#作者：huanghong
#创建日期：2018-4-2
#功能描述：雅朵酒店信息收集
#网页地址：http://wechat.yaduo.com/#/home
#处理进度：已完成（待优化）

import requests,random,time,json
from lxml import etree
import sys
import codecs,csv
import re
import os.path
import sqlite3
import MySQLdb 
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf-8')
se = requests.session()


headers={
'Accept':'application/json, text/plain, */*',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'Content-Length':'77',
'Content-Type':'application/x-www-form-urlencoded',
'Host':'api2.yaduo.com',
'Origin':'http://wechat.yaduo.com',
'Referer':'http://wechat.yaduo.com/',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
}

def get_city():
	citys=[]
	data={
	'appVer':'1.6.1',
	'channelId':3000001,
	'platType':3,
	'activitySource':'',
	'activeId':'',
	'deviceId':''
	}
	req=se.post('http://api2.yaduo.com/atourlife/city/listOfChain',headers=headers,data=data).content
	text=re.findall('"cityList":(\[.*?\]),"hotCityList"',req)[0]
	cont=json.loads(text)
	for i in cont:
		citys.append( i['cityName'] )
	return citys
def get_data(city):
	dataid=[]
	data={
	'beginDate':'2018-04-02',
	'endDate':'2018-04-03',
	'cityName':city,
	'longitude':'114.05838',
	'latitude':'22.69549',
	'appVer':'1.6.1',
	'channelId':'3000001',
	'platType':'3',
	'activitySource':'',
	'activeId':'',
	'deviceId':''
	}	
	req=se.post('http://api2.yaduo.com/atourlife/chain/cityChainList',headers=headers,data=data).content
	text=re.findall('"result":(\[.*?\]),"retcode"',req)[0]
	cont=json.loads(text)
	for i in cont:
		dataid.append([city,i['chainId']])
	return	dataid
def get_tel(citycode):
	data={
	'beginDate':'2018-04-02',
	'endDate':'2018-04-03',
	'chainId':citycode[1],
	'appVer':'1.6.1',
	'channelId':'3000001',
	'platType':'3',
	'activitySource':'',
	'activeId':'',
	'deviceId':''
	}
	req=se.post('http://api2.yaduo.com/atourlife/chain/detail',headers=headers,data=data).content
	text=json.loads(req)
	result=text['result']
	datas=[citycode[0],result['name'],result['address'],result['telephone'],result['latitude'],result['longitude'],result['shareUrl']]
	savesql_hotel(datas,'雅朵酒店.db')

def savesql_hotel(data,savepoint_name):
    #创建数据库
    con=sqlite3.connect(savepoint_name)
    con.execute('''CREATE TABLE IF NOT  EXISTS data
        (
        hoteltype varchar(200) NOT NULL,
        -- province varchar(200) NOT NULL,
        city varchar(200) NOT NULL,
        name varchar(1000) DEFAULT NULL,
        address varchar(1000) DEFAULT NULL,
        salesTel varchar(100) DEFAULT NULL, 
        lat varchar(100) DEFAULT NULL,
        lng varchar(100) DEFAULT NULL,
        Url  varchar(1000) DEFAULT NULL);''')
    # 插入数据
    sql='insert into data(hoteltype,city,name,address,salesTel,lat,lng,Url)\
    values("%s","%s","%s","%s","%s","%s","%s","%s")'%(u'雅朵酒店',data[0],data[1],data[2],data[3],data[4],data[5],data[6])
    con.execute(sql)
    con.commit()
    con.close()

def main():
	citys=get_city()
	for city in citys:
		citycodes=get_data(city)
		for citycode in citycodes:
			get_tel(citycode)
if __name__ == '__main__':
	main()	