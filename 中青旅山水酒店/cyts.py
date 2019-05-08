#coding=utf-8

#文件名称：botao.py
#作者：huanghong
#创建日期：2018-3-26
#功能描述：中青旅山水酒店信息搜集
#网页地址：http://www.shanshuihotel.com/listBookOrder.htm
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

headers={
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
'X-Requested-With':'XMLHttpRequest'
}
def get_city():
	citys=[]
	text=requests.post('http://www.shanshuihotel.com/listAreaCountCity.htm',headers=headers).content
	cont=json.loads(text)
	for i in cont:
		citys.append([i['city'],i['descript']])
	return citys	
def get_data(city):
	data={
	'cityCode':city[0],
	'checkInDate':'2018-03-26',
	'checkOutDate':'2018-03-27',
	'keyWordFind':'',
	'enableFilter':'1',
	'pageSize':'10'
	}
	html = requests.post('http://www.shanshuihotel.com/listBookOrder.htm',headers=headers,data=data).content
	pages=etree.HTML(html.decode('utf-8'))
	div=pages.xpath('//div[@class="left"]/ul//li')
	for i in div:
		div2=i.xpath('./div[@class="info"]/div')[0]
		jwd=i.xpath('./@position')[0].split(',')
		name=div2.xpath('./h4/a/text()')[0]
		href=div2.xpath('./h4/a/@href')[0]
		nameid=re.findall('(hotelId=.*?)&checkInDate=',href)[0]
		link='http://www.shanshuihotel.com/hotel.htm?'+nameid
		print link
		adress=div2.xpath('./p/text()')[0]
		phone=div2.xpath('./span/text()')[0].replace(u'电话：','')
		data=[city[1],name,adress,phone,jwd[0],jwd[1],link]
		savesql_hotel(data,u'中青旅山水酒店.db')


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
    values("%s","%s","%s","%s","%s","%s","%s","%s")'%(u'中青旅山水酒店',data[0],data[1],data[2],data[3],data[4],data[5],data[6])
    con.execute(sql)
    con.commit()
    con.close()

def main():
	citys=get_city()
	for city in citys:
		get_data(city)
if __name__ == '__main__':
	main()		