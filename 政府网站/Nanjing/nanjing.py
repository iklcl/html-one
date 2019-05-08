#-*- coding:utf-8 -*-
#网址：http://61.155.108.52:8181/
#文件名：南京公交线路查询列表.py
#作者: huanghong
#创建日期: 2017-10-16
#功能描述: 获取南京公交线路查询列表信息
#完成状况：完成
import time
import requests
from lxml import etree
import lxml.html
import sys
import codecs,csv
from bs4 import BeautifulSoup
import re
import json
import sqlite3
import MySQLdb
import MySQLdb as db
import os.path
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

logg=unicode(sys.path[0]+'\\logs.log','utf-8')
se = requests.session()
headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest'
}
uids=[]
fan=[]
#log日志
def loggs(strs):
	with open(logg,'ab') as f:
		time = str(datetime.now())[:-7]
		t = os.linesep
		s = time+' : '+str(strs)
		print s
		f.write(s+t)
def savesqlbuss_line(data,savepoint_name):
    #创建数据库
    con=sqlite3.connect(savepoint_name)
    con.execute('''CREATE TABLE IF NOT  EXISTS buss_line
        (
        lineid varchar(50) primary key NOT NULL,
        busname varchar(200) NOT NULL,
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
    sql='insert into buss_line(lineid,busname,servicetime,stations,url)\
        values("%s","%s","%s","%s","%s")'%(data[0],data[1],data[2],data[3],data[4])
    con.execute(sql)
    con.commit()
    con.close()
#将站点数据保存到数据库（所有数据，数据库名）
def buss_stationsql(data_station,savepoint_name):   
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
    #线路id，线路名，站点序号，站点名称
    for data in data_station:
        sql='insert into buss_station(lineid,busname,seq,name,others)\
        values("%s","%s","%s","%s","%s")'%(data[0],data[1],data[2],data[3],data[4])
        con.execute(sql)
    con.commit()
    con.close()



def get_one():
	row_name=[]
	url_list=['http://61.155.108.51:28088/electronicStation//a/station/busLineOut/findYangtzeNorth',
				'http://61.155.108.51:28088/electronicStation//a/station/busLineOut/findJiangNing',
				'http://61.155.108.51:28088/electronicStation//a/station/busLineOut/findCitProper']
	for url in url_list:
		req=se.get(url,headers=headers).content
		lis=re.findall(r'\[.*\]',req)[0]
		jd = json.loads(lis)
		for i in jd:
			row_name.append((i['routeName'],url))
		time.sleep(3)
	return row_name		
		
def get_row():
	url_list=['http://61.155.108.51:28088/electronicStation//a/station/busLineOut/findYangtzeNorth',
				'http://61.155.108.51:28088/electronicStation//a/station/busLineOut/findJiangNing',
				'http://61.155.108.51:28088/electronicStation//a/station/busLineOut/findCitProper']
	for url in url_list:
		req=se.get(url,headers=headers).content
		lis=re.findall(r'\[.*\]',req)[0]
		jd = json.loads(lis)
		for i in jd:
			if i['routeName'] in fan:			
				line1_name=i['routeName']+'('+i['firstStationSite']+'-'+i['firstStationSiteOther']+')'
				line1_row=i['lineSites'].replace(' ','').replace('、','-')
				if i['serviceStartTime']==None:
					i['serviceStartTime']='-'
				if i['serviceEndTime']==None:
					i['serviceEndTime']='-'
				line1_time=i['serviceStartTime']+'-'+i['serviceEndTime']
				line1_id=str(i['serviceId'])+'1'
				line1=[line1_id,line1_name,line1_time,line1_row,url]
				line1_station=i['lineSites'].replace(' ','').split('、')
				t1=0
				sta1=[]
				for station1 in line1_station:
					t1+=1
					da1=[line1_id,line1_name,str(t1),station1,'']
					sta1.append(da1)
				buss_stationsql(sta1,'南京公交——站点表.db')
				savesqlbuss_line(line1,'南京公交——路线表.db')

				line2_name=i['routeName']+'('+i['lastStationSite']+'-'+i['lastStationSiteOther']+')'
				line2_row=i['lineSitesOther'].replace(' ','').replace('、','-')
				if i['serviceStartTimeOther']==None:
					i['serviceStartTimeOther']='-'
				if i['serviceEndTimeOther']==None:
					i['serviceEndTimeOther']='-'	
				line2_time=i['serviceStartTimeOther']+'-'+i['serviceEndTimeOther']
				line2_id=str(i['serviceId'])+'2'
				line2=[line2_id,line2_name,line2_time,line2_row,url]
				line2_station=i['lineSitesOther'].replace(' ','').split('、')
				t2=0
				sta2=[]
				for station2 in line2_station:
					t2+=1
					da2=[line2_id,line2_name,str(t2),station2,'']
					sta2.append(da2)
				buss_stationsql(sta2,'南京公交——站点表.db')
				savesqlbuss_line(line2,'南京公交——路线表.db')
		

def get_id(name):
	params={
	'qt':'bl',
	'c':'315',
	'wd':name[0],
	'ie':'utf-8',
	'oue':'1',
	'fromproduct':'jsapi',
	'res':'api',
	'callback':'BMap._rd._cbk90778',
	'ak':'nzaTOFWB7YmDxNAgYSul3j8U4kFzFgUA'
	}
	req=requests.get('http://api.map.baidu.com/?',params=params).content
	bre=0
	try:
		lis1=re.findall(r'{"content":(\[.*\])',req)[0]
	except Exception as e:
		fan.append(name[0])
		bre=1
	if bre!=1:	
		lis2=re.findall(r'(\[.*?\]),"current_city"',lis1)[0]
		jd = json.loads(lis2)
		for i in jd:
			try:
				uids.append((i['uid'],i['name'],name[1],name[0]))
			except Exception as e:
				fan.append(name[0])
				break
		

def get_station(name):
	params={
	'qt':'bsl',
	'c':'315',
	'uid':name[0],
	'ie':'utf-8',
	'oue':'1',
	'fromproduct':'jsapi',
	'res':'api',
	'callback':'BMap._rd._cbk8021',
	'ak':'nzaTOFWB7YmDxNAgYSul3j8U4kFzFgUA'
	}	
	req=requests.get('http://api.map.baidu.com/?',params=params).content
	try:
		lis1=re.findall(r'"stations":(\[.*),"ticketPrice"',req)[0]
	except Exception as e:
		fan.append(name[3])
		print u'请求无效'
		return
	lis1=re.findall(r'"stations":(\[.*),"ticketPrice"',req)[0]
	time=re.findall(r'"timetable":"(.*)","timetable_ext"',req)[0].replace(u'\u65e9','').replace(u'\u665a','')
	jd = json.loads(lis1)
	line=[]
	data_station=[]
	xuhao=0
	for i in jd:
		xuhao+=1
		da=[name[0],name[1],xuhao,i["name"],i["geo"]]
		data_station.append(da)		
		line.append(i["name"])
	row="-".join(line).replace('\n','')
	data_line=[name[0],name[1],time,row,name[2]]
	r=1
	try:
		savesqlbuss_line(data_line,'南京公交——路线表.db')
	except Exception as e:
		r=0	
	if r!=0:
		buss_stationsql(data_station,'南京公交——站点表.db')

def main():
    row_name=get_one()
    print len(row_name)
    for name in row_name:
    	# print name[1]
    	get_id(name)
    print len(uids)
    print len(set(uids))
    for i in list(set(uids)):
    	print i[0],i[1]
    	get_station(i)
    get_row()
    	

if __name__ == '__main__':
	# try:
	main()
	# except Exception as e:
	# 	loggs(e)		