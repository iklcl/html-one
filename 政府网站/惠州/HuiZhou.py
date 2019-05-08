#-*- coding:utf-8 -*-
#网址：http://121.40.70.116:82/%E5%85%AC%E4%BA%A4%E5%87%BA%E8%A1%8C/Default.aspx?type=busLine&val=1
#文件名：惠州公交线路查询列表.py
#作者: huanghong
#创建日期: 2017-09-29
#功能描述: 获取惠州公交线路查询列表信息
#完成状况：完成
import time
import requests
from lxml import etree
import lxml.html
import sys
import codecs,csv
from bs4 import BeautifulSoup
import re
import sqlite3
import MySQLdb
import MySQLdb as db
import os.path
from datetime import datetime
import json
reload(sys)
sys.setdefaultencoding('utf-8')
row_name=[]
logg=unicode(sys.path[0]+'\\logs.log','utf-8')
se = requests.session()
headers={
	'Accept':'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Connection':'keep-alive',
	'Content-Length':'10',
	'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
	'Host':'121.40.70.116:82',
	'Origin':'http://121.40.70.116:82',
	'Referer':'http://121.40.70.116:82/%E5%85%AC%E4%BA%A4%E5%87%BA%E8%A1%8C/BusLine.aspx?busline_name=1',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest'
	}
headers2={
	
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
	}	
#log日志
def loggs(strs):
	with open(logg,'ab') as f:
		time = str(datetime.now())[:-7]
		t = os.linesep
		s = time+' : '+str(strs)
		print s
		f.write(s+t)
def get_zi():
	one = [u'驳',u'快',u'专',u'东莞',u'深圳',u'莞惠']
	name=get8684()
	for i in name:
		zi=re.findall('([A-Z])',i)
		if len(zi)!=0:
			one.append(zi[0])
		z2=re.findall('(.*?)\d+',i)
		if len(z2)!=0:
			one.append(z2[0])
		z3=re.findall('(\d+)',i)
		if len(z3)!=0:
			one.append(z3[0])			
	for i in range(10):
		one.append(i)
	print list(set(one))		
	return list(set(one))

def get_row():
	zsd=get_zi()
	li=[]
	url='http://121.40.70.116:82/%E5%85%AC%E4%BA%A4%E5%87%BA%E8%A1%8C/Ajax.aspx'
	params = {
			"method":"QueryLinesAndStations"
		}
	for i in zsd:	
		data={
			"linename":i
		}	
		req=se.post(url,headers=headers,params=params,data=data).text
		lis = re.findall(r'(\[.*\])',req)[0]		
		jd = json.loads(lis)
		try:
			data=jd[0]['lineStationList'][0]['linesList']
		except Exception as e:
			continue	
		for i in data:
				li.append(i['lineId'])
	print  len(set(li))	
	return list(set(li))	



def get_data(link):
	url='http://121.40.70.116:82/%E5%85%AC%E4%BA%A4%E5%87%BA%E8%A1%8C/Ajax.aspx'
	params = {
			"method":"GetAllStationByLineId"
		}
	for page in range(0,2):
		data={
			"lineid":link,
			"direction":"%s"%page
		}	
		req=se.post(url,headers=headers,params=params,data=data)
		urll=req.url			
		lis = re.findall(r'(\[.*\])',req.text)[0]
		try:
			jd = json.loads(lis)[0]
		except Exception as e:
			break	
		lineId=link+str(page)
		row_name.append(jd['lineName'].replace(u'路',''))
		lineName=jd['lineName']+'('+jd['beginStation']+'-'+jd['endStation']+')'
		dat=jd['stations']
		datas=[]
		stations=[]
		xuhao=0
		for data in dat:
			xuhao+=1
			datas.append(data['stationName'])
			station_data=(lineId,lineName,xuhao,data['stationName'],data['lon'],data['lat'],u'经度、纬度')
			stations.append(station_data)
		row="-".join(datas).replace('\n','')
		print urll
		line_data=(lineId,lineName,jd['startTime']+'-'+jd['endTime'],jd['price'],row,urll)
		print len(line_data)
		bre=1
		try:
			savesqlbuss_line(line_data,u'惠州公交——线路表.db')
		except Exception as e:
			bre=0
		if bre==0:
			pass
		else:	
			buss_stationsql(stations,u'惠州公交——站点表.db')


def savesqlbuss_line(data,savepoint_name):
    #创建数据库
    con=sqlite3.connect(savepoint_name)
    con.execute('''CREATE TABLE IF NOT  EXISTS buss_line
        (
        lineid varchar(50) NOT NULL,
        busname varchar(200) primary key NOT NULL,
        servicetimeType varchar(1000) DEFAULT NULL,
        servicetime varchar(1000) DEFAULT NULL, 
        buscost varchar(30) DEFAULT NULL,
        blocktariff tinyint(1),
        startingrate varchar(30) DEFAULT NULL,
        fullprice varchar(30) DEFAULT NULL,
        stations text, 
        reverse tinyint(1) DEFAULT NULL,
        district varchar(100) DEFAULT NULL,
        linetype  varchar(30) DEFAULT NULL,
        operator varchar(100) DEFAULT NULL, 
        airconditioner tinyint(1) DEFAULT NULL, 
        monthlyticket tinyint(1) DEFAULT NULL, 
        twm tinyint(1) DEFAULT NULL, 
        ltd tinyint(1) DEFAULT NULL,
        loopline tinyint(1) DEFAULT NULL, 
        interval text,
        url varchar(500) DEFAULT NULL,
        remarks text );''')

    # 插入数据

    sql='insert into buss_line(lineid,busname,servicetime,buscost,stations,url)\
    values("%s","%s","%s","%s","%s","%s")'%(data)
    con.execute(sql)
    con.commit()
    con.close()
        
#将站点数据保存到数据库（所有数据，数据库名）
def buss_stationsql(data,savepoint_name):
   
    #创建数据库
    con=sqlite3.connect(savepoint_name)    
    con.execute('''CREATE TABLE IF NOT  EXISTS buss_station
        (
        lineid varchar(50) NOT NULL, 
		busname varchar(200) NOT NULL, 
		seq tinyint(3) DEFAULT NULL, 
		name varchar(200) DEFAULT NULL,
		ox varchar(50) DEFAULT NULL,
		oy varchar(50) DEFAULT NULL,
		oxytype varchar(100) DEFAULT NULL,
		others varchar(200) DEFAULT NULL
		   );''')

    # 插入数据
    for d in data:
        #线路id，线路名，站点序号，站点名称
        sql='insert into buss_station(lineid,busname,seq,name,ox,oy,oxytype)\
        values("%s","%s","%s","%s","%s","%s","%s")'%(d)
        con.execute(sql)
    con.commit()
    con.close() 


def get8684():
	html=requests.get('http://huizhou.8684.cn/so.php?k=pp&q=%25',headers=headers2).content
	html2=etree.HTML(html.decode('utf-8'))
	name=html2.xpath(u"//div[@id='con_site_4']/a/text()")
	# print len(name)
	return name


def main():
	data8684=[]
	newda=[]
	oldda=[]
	hrefs=get_row()
	for i in hrefs:
		# print i
		get_data(i)
		# time.sleep(1)
	name=get8684()
	for i in name:
		data8684.append(i.replace(u'路',''))
	with open(u'文档.txt','ab') as f:
		f.write(u'在公交查询没找到但8684中有的：')	
	for i in set(row_name):
		if i not in data8684:
			with open(u'文档.txt','ab') as f:
				f.write(i+'，')
	with open(u'文档.txt','ab') as f:	
		f.write('\r\n'+'\r\n'+u'在公交查询找到但8684中没有有的：')	
	for i in data8684:
		if i not in set(row_name):
			with open(u'文档.txt','ab') as f:	
				f.write(i+'，')				 
	loggs('完成')

if __name__ == '__main__':
	# try:
		# main()
	# except Exception as e:
	# 	loggs(e)
	main()			