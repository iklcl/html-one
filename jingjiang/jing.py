#coding=utf-8

#文件名称：jing.py
#作者：huanghong
#创建日期：2018-3-28
#功能描述：锦江国际旗下其他酒店信息搜集
#网页地址：http://hotel.bestwehotel.com/HotelSearch/?checkinDate=2018-03-19&checkoutDate=2018-03-20&cityCode=AR04567&brand=137
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
'Accept':'application/json, text/plain, */*',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'Content-Length':'25',
'Content-Type':'application/json;charset=UTF-8',
'Cookie':'tongji_key=b3848d53-b37d-b5a7-9b85-ea244429a698',
'Host':'hotel.bestwehotel.com',
'Origin':'http://hotel.bestwehotel.com',
'Referer':'http://hotel.bestwehotel.com/HotelSearch/?checkinDate=2018-03-19&checkoutDate=2018-03-20&cityCode=AR04567&brand=137',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
}
def get_city():
	citys=[]
	datas={
	"channelCode":"CA00046"
	}
	data=json.dumps(datas)
	text=requests.post('http://hotel.bestwehotel.com/api/hotel/queryAllCites',headers=headers,data=data).content
	js=re.findall(',"otaCitys":(\[.*?\]),"hotOtaCitys"',text)[0]
	cont=json.loads(js)
	for i in cont:
		print i['cityCode'],i['cityName'],i['lat'],i['lng']
		citys.append([i['cityCode'],i['cityName'],i['lat'],i['lng']])
	return citys

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
    values("%s","%s","%s","%s","%s","%s","%s","%s")'%(u'锦江国际旗下其他酒店',data[0],data[1],data[2],data[3],data[4],data[5],data[6])
    con.execute(sql)
    con.commit()
    con.close()

def get_data(city):
	page=1
	while True:
		headers1={
		'Accept':'application/json, text/plain, */*',
		'Accept-Encoding':'gzip, deflate',
		'Accept-Language':'zh-CN,zh;q=0.9',
		'Connection':'keep-alive',
		'Content-Length':'258',
		'Content-Type':'application/json;charset=UTF-8',
		'Cookie':'tongji_key=b3848d53-b37d-b5a7-9b85-ea244429a698',
		'Host':'hotel.bestwehotel.com',
		'Origin':'http://hotel.bestwehotel.com',
		'Referer':'http://hotel.bestwehotel.com/HotelSearch/?checkinDate=2018-03-28&checkoutDate=2018-03-29&cityCode=AR00252&queryWords=',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
			}
		datas={
		'brands':[],
		'bzLat':"",
		'bzLng':"",
		'channelCode':"CA00046",
		'checkInDate':"2018-03-28",
		'cityCode':city[0],
		'days':1,
		'districtCode':"",
		'keyWord':"",
		'loLat':int(float(city[2])),
		'loLng':int(float(city[3])),
		'maxPrice':"1000",
		'minPrice':0,
		'page':page,
		'size':10,
		'sort':1,
		'starTypes':[]
			}
		data=json.dumps(datas)
		text=requests.post('http://hotel.bestwehotel.com/api/hotel/searchHotels',headers=headers1,data=data).content	
		js=re.findall(',"hotels":(\[.*?\,"labels":\[\]}\])}',text)
		if len(js)==0:
			break
		cont = json.loads(js[0])
		for i in cont:
			jwd=i['mapInfos'][1]
			url='http://hotel.bestwehotel.com/HotelDetail/?hotelId='+i['hotelId']
			data=[city[1],i['hotelName'],i['hotelAddress'],i['hotelPhone'],jwd['lat'],jwd['lng'],url]
			savesql_hotel(data,u'锦江国际旗下其他酒店.db')
		print page
		page+=1	
		

def main():
	citys=get_city()
	for city in citys:
		if city[2]!=None:
			print city[1],city[2],city[3]
			get_data(city)



if __name__ == '__main__':
	main()