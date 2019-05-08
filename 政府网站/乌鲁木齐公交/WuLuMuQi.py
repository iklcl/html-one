#-*- coding:utf-8 -*-
#网址：http://www.wlmqbrt.com/changgu-bus01.html
#文件名：昆明公交线路查询列表.py
#作者: huanghong
#创建日期: 2017-09-23
#功能描述: 获取乌鲁木齐公交线路查询列表信息
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
import MySQLdb as db
import os.path
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

logg=unicode(sys.path[0]+'\\logs.log','utf-8')

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"
}
#log日志
def loggs(strs):
	with open(logg,'ab') as f:
		time = str(datetime.now())[:-7]
		t = os.linesep
		s = time+' : '+str(strs)
		print s
		f.write(s+t)	
#获取公交线路
def get_row():
	links=[]
	names=[]
	ids=[]
	req=requests.get('http://www.wlmqbrt.com/changgu-bus01.html',headers=headers).content.decode('gbk','ignore')
	soup=BeautifulSoup(req,'lxml')
	dd=soup.find_all('dd')[0]
	hrefs=dd.find_all('a')
	idname=0
	for i in hrefs:
		name=i.text
		if name in [u'环线','5020','5030']:
			idname=idname+1
			ids.append(idname)
			href=i.get('href')
			links.append(href)
			names.append(name)
		else:
			idname=idname+1
			ids.append(idname)
			idname=idname+1
			ids.append(idname)
			href=i.get('href')
			links.append(href)
			href=href.strip('/')+'/1'
			links.append(href)
			
			names.append(name)
			names.append(name)	
	data=zip(names,links,ids)
	return data	

def get_data(an):
	station_data=[]
	station_data.append(an[2])
	req=requests.get(an[1],headers=headers).content	
	time.sleep(1)
	print an[1],an[2]
	soup=BeautifulSoup(req,'lxml')
	div=soup.find_all('div',id='stationTujing')
	p2=soup.find_all('p',id="endbrain")[0]
	linename=p2.find_all('strong')
	line_name=an[0]+'('+linename[0].text+'-'+linename[1].text+')'
	# print line_name
	station_data.append(line_name)
	luxian=div[0].text.replace('→','-').replace('\n','')
	p=soup.find_all('p',class_='description')[0].text
	timrs=p.replace('            ','').replace('	','').split('\n')
	lis=[x for x in timrs if x!='']
	if len(lis)==0:
		times=''
		piaozhi=''
	else:		

		times=lis[0].replace(u'起点站首末车时间:','')

		if len(lis)==3:
			piaozhi=re.findall(u'分段计价',lis[2])
		else:
			piaozhi=''	
		if len(piaozhi)!=0:
			piaozhi=1
		else:
			piaozhi=''
	station_data.append(times)
	station_data.append(piaozhi)
	station_data.append(luxian)
	station_data.append('1')
	station_data.append(an[1])
	savesqlbuss_line(station_data,u'乌鲁木齐公交——线路表.db')
	buss_station(station_data)

def savesqlbuss_line(data,savepoint_name):
    #创建数据库
    con=sqlite3.connect(savepoint_name)
    con.execute('''CREATE TABLE IF NOT  EXISTS buss_line
        (
        id integer primary key NOT NULL,
        lineid varchar(50) NOT NULL,
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

    sql='insert into buss_line(lineid,busname,servicetime,blocktariff,stations,reverse,url)\
    values("%s","%s","%s","%s","%s","%s","%s")'%(data[0],data[1],data[2],data[3],data[4],data[5],data[6])
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
        print d[0],d[1],d[2],d[3]
        sql='insert into buss_station(lineid,busname,seq,name)\
        values("%s","%s","%s","%s")'%(d)
        con.execute(sql)
    con.commit()
    con.close() 
def buss_station(data):
    	ds=[]
    
        st= data[4].split('-')
        #设置序号
        for i in range(len(st)):
            xuhao=i+1#序号
            # print xuhao,st[i]
            ds.append((data[0],data[1],xuhao,st[i]))
        buss_stationsql(ds,u'乌鲁木齐公交——站点表.db')        
    
def main():
	datas=get_row()
	for i in datas:
		get_data(i)
	loggs('完成')	
if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		loggs(e)	