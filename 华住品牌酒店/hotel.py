#coding=utf-8

#文件名称：hotel.py
#作者：huanghong
#创建日期：2018-3-19
#功能描述：华住酒店信息搜索
#网页地址：http://hotels.huazhu.com/?CityID=3101&HotelStyleList=4
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
headers2={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest'
}
headers={
'__v_t':'3988192165626873a453bb8e189b4697cecad8d93599d34cf5332086e96e8c466de2a6eb45c8137033d1ccc93424c4fc0fe1ff57ab9856cd0babb6d990c0f424b1dbcf2964886ab68ad20f3d90e6f0bf55aabacab829d4fe96c403d5f214221e07bb8da9705b68fd2c83049153ad21711ae6eaa54d7a300a51e959a33bf727d8bcb283b6b46ac8d548b4286945ee96957833cb5c93e359232fab3afb0778c8860a4243216093ab5e86aa24ff9dcc823aed74f3dedc280902cc1e8bf68473b16d79d064663fa34c552deb07f4af4abdf8e9d326745970394c23f86cf0ea418ad1d95c55510e3493267617a961aaafc9d372752f934e329a25b7909e9125b9605240a02f9b4f5417f028186234e71c3e39adea97f5165d07927199bbb97b1c2fd5c1049cb5c9a641b6bc1c4006a7cc34c0ed0ca18daf531271e71abc625858485332906c6dc5f1edb6289fc1dd584f23cae2f4511b258999c7edb12810d055875d68d891b0667a6a71db423ac9992326f274cb42bf0aa09ffbf8c6952a990edc19df9c4099b02ad72b9e7b22b7cebd4ddcda1f9268815c247c5dde3235cdcebf690411f510a0e711e583bebf60dde145f473e59c93736b9ed41f343c2d73da495daa05e2c071d841918d4733641121ece6eb9b7b101079957654c7f577894a49eeb32a2c2e6715140c1ccc192dcb51301258adc66163b3c2247d3c38d8344abeae22a79fd2c0460415c62c963e94adf1d56b70b31376e7f4b8bd7b892ba7e5ebd14117f5bb5e6c4b63fcc96f1f788e5313976302058293b139d38624e409e19d4f804f59756bbc564609368bbe3a575f5c082a08404b7cff66f446e979a519a39e95f8ceb60e728aa2658c059d2f4c124d4cdfe259e69c91eec44dcb0e3258e6c9a7b3111d83f1e22aaf4cf454957fb2f08a84623dfe28e4f72e96aeea719806f9c911c9a6879465666b04eddd45cfa82fa2d4283e7a64e8e6926789da13c5540181661787f3ee0e9d8820c68ead275f36',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
'X-Requested-With':'XMLHttpRequest'
}

path=os.path.join(os.getcwd(),'path2.csv')

def savesql_hotel(data,savepoint_name):
    #创建数据库
    con=sqlite3.connect(savepoint_name)
    con.execute('''CREATE TABLE IF NOT  EXISTS data
        (
        id integer primary key NOT NULL,
        city varchar(200) NOT NULL,
        name varchar(1000) DEFAULT NULL,
        address varchar(1000) DEFAULT NULL,
        salesTel varchar(100) DEFAULT NULL, 
        lat varchar(100) DEFAULT NULL,
        lng varchar(100) DEFAULT NULL,
        Url  varchar(1000) DEFAULT NULL);''')
    # 插入数据
    sql='insert into data(city,name,address,salesTel,lat,lng,Url)\
    values("%s","%s","%s","%s","%s","%s","%s")'%(data[0],data[1],data[2],data[3],data[4],data[5],data[6])
    con.execute(sql)
    con.commit()
    con.close()



citys=[]#存储城市列表
datas=[]#存储酒店id列表


#抓取城市列表
def get_city():
	html = requests.get('http://hotels.huazhu.com/Basic/NativeCityOverView?_=%s'%int(round(time.time() * 1000)),headers=headers).content
	cont=re.findall('"CityList":(\[.*\]),"HotCityList"',html)[0]
	htmll=json.loads(cont)
	t=0
	for city in htmll:
		t+=1
		citys.append([city['CityName'],city['CityID']])

#通过城市id获取酒店信息
def get_data(cityID):
	page=0
	while True:
		page+=1
		params={
		'CheckInDate':'2018-03-27',
		'CheckOutDate':'2018-03-28',
		'CityID':cityID[1],
		'PageIndex':page,
		'_':int(round(time.time()*1000))
		}
		
		html =req(params)
		# print html
		cont=re.findall('"HotelList":(\[.*\]),"TotalCount"',html)
		try:
			htmll=json.loads(cont[0])
		except Exception as e:
			print cont[0]
		if len(htmll)==0:
			break
		for data in htmll:
			data=[cityID[0],data['HotelName'],data['HotelAddressShort'],data['Lat'],data['Lng'],data['HotelID']]
			datas.append(data)
			with codecs.open(path,'ab') as f:
					w = csv.writer(f)
					w.writerow(data)
		print len(datas),'===='
		# time.sleep(1)	


#请求url，报错再次请求
def req(params):
	try:
		html =se.get('http://hotels.huazhu.com/Search/HotelList',headers=headers,params=params).content
	except Exception as e:
		return req(params)
	return html	

#抓取电话号码
def get_tel(data):
	url='http://hotels.huazhu.com/hotel/detail/%s'%data[5]
	html =requests.get(url,headers=headers2)
	print html.status_code
	if html.status_code	!=200:
		url='http://hotels.huazhu.com/inthotel/detail/%s'%data[5]
		html =requests.get(url,headers=headers2)
		tel=''
	else:	
		try:
			tel =re.findall('<div class="text itembox"><span>(.*)</span><span>',html.content)[0]
		except Exception as e:
			# print html
			print url,data[0],data[1]
			tel=''
	hoteldata=[data[0],data[1],data[2],tel,data[3],data[4],url]
	savesql_hotel(hoteldata,u'华住品牌酒店.db')


def process_start(url_list): 
	tasks = []  
	for data in url_list:  
	    tasks.append(gevent.spawn(get_tel,data))  
	gevent.joinall(tasks)#使用协程来执行 


def run():
    data=read_file()
    url_list=[]
    i = 0 #计数器，记录添加了多少个url到协程队列  
    while True:  
        i += 1 
        print len(data)
        if len(data)==0:
        	break
        url=data.pop()
        url_list.append(url)#每次读取出url，将url添加到队列  
        if i ==2000:#一定数量的url就启动一个进程并执行  
            process_start(url_list)  
            url_list = [] #重置url队列  
            i = 0 #重置计数器
    if len(url_list)!=0:#若退出循环后任务队列里还有url剩余  
        process_start(url_list)  



def read_file():
	data=[]
	idname=[]
	import csv
	#读取csv文件
	csv_reader = csv.reader(open(path))
	for row in csv_reader:
		if row[5] not in idname: 
			idname.append(row[5])
			data.append(row)
	if  os.path.exists(path):
		os.remove(path)		
	return data


def main():
	get_city()
	print len(citys)
	t=0
	for i in citys:
		t+=1
		print t,i[1]
		get_data(i)
	print len(datas)
if __name__ == '__main__':
	main()
	run()
