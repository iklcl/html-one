#coding=utf-8

#文件名称：botao.py
#作者：huanghong
#创建日期：2018-3-19
#功能描述：华住酒店信息搜索
#网页地址：http://www.plateno.com/list.html?brand=93
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
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest'
}

ip_data=[]
def ip_sql():
	
	#存入数据库
	# 打开数据库连接
	db = MySQLdb.connect("192.168.201.91","root","123456","spidertools" )
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	# 创建数据表SQL语句
	sql="SELECT * FROM proxyippool; "
	cursor.execute(sql)
   # 获取所有记录列表
	results = cursor.fetchall()
	for row in results:
		ip=row[0]+'://'+row[1]+':'+row[2]
		ip_data.append(ip)
	db.commit()	
	# 关闭数据库连接
	db.close()
	# return ip_data



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
    values("%s","%s","%s","%s","%s","%s","%s","%s")'%(u'铂涛集团',data[0],data[1],data[2],data[3],data[4],data[5],data[6])
    con.execute(sql)
    con.commit()
    con.close()

def get_city():
	datas=[]
	jstext=se.get('http://www.plateno.com/basic/ota/whole/city',headers=headers).content
	# print jstext
	text=re.findall('"chinese":(\[.*\]),"overseas":',jstext)[0]
	data =json.loads(text)
	for i in data:
		datas.append([i['cityCode'],i['cityName']])
	return datas	

def get_data(city,page=1,it=0):
	it+=1
	ip= random.sample(ip_data,1)[0]
	se.proxies = {'http': ip,'https': ip}
	headers={
	'Accept':'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.9',
	'Connection':'keep-alive',
	'Content-Length':'298',
	'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
	'Cookie':'HttpOnly=true; _ga=GA1.2.1966650010.1521624997; EC5FA8A6C402F919E6FC90C26FCD533C=5e74597e4374c26ab4f1d64ac6ece2ba; HttpOnly=true; screen=1440x900; _gid=GA1.2.443542060.1521940930; Hm_lvt_0d216c490a56620d27a11a0030ea511f=1521624997,1521940930; _gat=1; JSESSIONID=DE6E3BEA3CA760D818A1E455236D4C4E; Hm_lpvt_0d216c490a56620d27a11a0030ea511f=1521946068',
	'Host':'www.plateno.com',
	'Origin':'http://www.plateno.com',
	# 'Referer':'http://www.plateno.com/list.html?city=%s&cityCode=AR05354&checkInDate=%s&checkOutDate=%s'%(city[1],int(round(time.time() * 1000)),int(round(time.time() * 1000))),
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest'
	}
	# data2={
	# 		'cityCode':city[0]
	# 		}
	# sd=se.post('http://www.plateno.com/basic/ota/getLandMark',headers=headers,data=data2)
	# print u'正在连接'
	while True:
		data={
		'searchKeywordFlag':'0',
		'keyword':'',
		'city':city[1],
		'cityCode':city[0],
		'bizlat':'0.0',
		'bizlng':'0.0',
		'checkInDate':int(round(time.time() * 1000)),
		'checkOutDate':int(round(time.time() * 1000)),
		'days':'1',
		'recommandStarType':'',
		'brand':'',
		'districtCode':'',
		'memberType':'',
		'minPrice':'0',
		'maxPrice':'0',
		'hasRoom':'0',
		'isFacility':'1',
		'sort':'1',
		'page':page,
		'pageSize':'20',
		'promotion':'0',
		'eventType':'0'
			}
		try:
			jstext=se.post('http://www.plateno.com/hotel/query/ota/basic',headers=headers,data=data,timeout=20).content
			text=re.findall('"data":(\[.*\]),"hotelSum"',jstext)
		except requests.exceptions.ProxyError:
			return get_data(city,page,it)
		except requests.exceptions.ConnectionError:
			return get_data(city,page,it)	
		except requests.exceptions.ReadTimeout:
			if it>10:
				break
			return get_data(city,page,it)		
		except Exception as e:
			print type(e)
			if it>20:
				break
			return get_data(city,page,it)	
		print jstext
		if len(text)==0:
			iptest=re.findall('(亲，暂时无相关酒店，请尝试更换搜索条件)',jstext)
			print len(iptest)
			if len(iptest)!=0:
				break	
			else:
				return get_data(city,page,it)
		datas =json.loads(text[0])
		for i in datas:
			url='http://www.plateno.com/detail.html?innId=%s'%i["innId"]
			data = [city[1],i["innName"],i['address'],i['innPhone'],i['glat'],i['glng'],url]
			savesql_hotel(data,'铂涛集团.db')
		page +=1	
		# time.sleep(3)

def main():
	ip_sql()
	city=get_city()
	for  i in city:
		print i[1]
		get_data(i)

if __name__ == '__main__':
	main()