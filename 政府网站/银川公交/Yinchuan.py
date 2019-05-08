#-*- coding:utf-8 -*-
#网址：http://www.ycgjgs.com/qynews.php?type=5
#文件名：银川公交线路查询列表.py
#作者: huanghong
#创建日期: 2017-09-26
#功能描述: 获取银川公交线路查询列表信息
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
reload(sys)
sys.setdefaultencoding('utf-8')

logg=unicode(sys.path[0]+'\\logs.log','utf-8')
se = requests.session()
headers={
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	"Accept-Encoding":"gzip, deflate",
	"Accept-Language":"zh-CN,zh;q=0.8",
	"Connection":"keep-alive",
	"Cookie":"yunsuo_session_verify=295fbf067834d901a34a507aa1e9785c; ASPSESSIONIDASTBBDQR=PFFJJECCDKGEDMAPAGAACNEB; srcurl=687474703a2f2f7777772e7963676a67732e636f6d2f7869616e6c752f3f5f583230332e68746d6c; security_session_mid_verify=1ee58db9fbb2a0b927475c43cd0e8648",
	"Host":"www.ycgjgs.com",
	"Upgrade-Insecure-Requests":"1",
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
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
	hrefs=[]
	idnames=[]
	idname=0
	for i in xrange(1,9):	
		url='http://www.ycgjgs.com/xianlu/'
		params = {
			"_L%s.Html"%i:""
		}
		req=se.get(url,headers=headers,params=params).content
		soup=BeautifulSoup(req,'lxml')
		fieldset=soup.find_all('fieldset',class_="lblock zhan")[1]
		alink=fieldset.find_all('a')
		for link in alink:
			idname+=1
			idnames.append(idname)
			a=link.get('href').replace('/xianlu/?','')
			hrefs.append(a)
		time.sleep(3)
	links=zip(idnames,hrefs)	
	return	links	
def get_data(link):
	data=[]
	datas=[]
	datas.append(link[0])
	url='http://www.ycgjgs.com/xianlu/'
	params = {
			"%s"%link[1]:""
		}
	req=se.get(url,headers=headers,params=params).content
	soup=BeautifulSoup(req,'lxml')
	fieldset1=soup.find_all('fieldset',class_="lblock zhan")[1]
	fieldset2=soup.find_all('fieldset',class_="lblock zhan")[0]
	#路线名
	names=fieldset2.find_all('legend')[0].string.replace(u'说明','')
	information=fieldset2.text.replace(u' ','').replace(u'：','').replace(u'\u000d\u000a','').replace('\n','')
	# print information
	#发车间隔描述
	
	wuren=re.findall(u'无人售票',information)
	if len(wuren)==0:
		twm=''
	else:
		twm='1'	
	interval=re.findall(u'(间隔.*?)营运',information)	
	if len(interval)==0:
		interval=re.findall(u'―\d{2}:\d{2}(.*?)营运',information)
		if len(interval)==0:
			interval=re.findall(u'(单程.*?)营运',information)
			if len(interval)==0:
				interval=['']
	#票价
	pascost=re.findall(u'票价(\d|.)元',information)
	if len(pascost)==0:
		pascost=''
		qijia=re.findall(u'(\d)元起价',information)
		if len(qijia)==0:
			qijia=''
		else:
			qijia=qijia[0]	
		quancheng=re.findall(u'全程(\d)元',information)
		if len(quancheng)==0:
			quancheng=''
		else:
			quancheng=quancheng[0]
	else:
		pascost=pascost[0]
		qijia=''
		quancheng=''
	times=re.findall(u'首末班时间(.*―\d{2}:\d{2})',information)
	#时间
	if len(times)==0:
		times=re.findall(u'发车时间(.*?)间隔时间',information)
		if len(times)==0:
			times=re.findall(u'首末班时间(.*?)间隔',information)
			if len(times)==0:
				times=re.findall(u'时间(.*?)单程',information)
				if len(times)==0:
					es=re.findall(u'首末班时间',information)
					if len(es)==0:
						times=re.findall(u'(.*?)发车',information)
					else:
						times=re.findall(u'首末班时间(.*?)；',information)	

	times=times[0].strip(':').replace(u'、','-').replace(u'计划发车','').replace(u'发车','')
	#路线
	alink=fieldset1.find_all('a')
	for linkess in alink:
		a=linkess.text.replace('\n','').replace('\r','')
		data.append(a)
	row="-".join(data).replace('\n','')
	url='http://www.ycgjgs.com/xianlu/'+link[1]
	datas.append(names)
	datas.append(times)
	datas.append(pascost)
	datas.append(qijia)
	datas.append(quancheng)
	datas.append(row)
	
	datas.append(twm)
	datas.append(interval[0])
	datas.append(url)
	
	savesqlbuss_line(datas,u'银川公交——线路表.db')
	buss_stationsql(datas,data,u'银川公交——站点表.db')


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

    sql='insert into buss_line(lineid,busname,servicetime,buscost,startingrate,fullprice,stations,twm,interval,url)\
    values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9])
    con.execute(sql)
    con.commit()
    con.close()
        
#将站点数据保存到数据库（所有数据，数据库名）
def buss_stationsql(datas,data,savepoint_name):
    rowdata=[]
    for i in range(len(data)):
            xuhao=i+1#序号
            # print xuhao,st[i]
            rowdata.append((datas[0],datas[1],xuhao,data[i]))
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
    for d in rowdata:
        #线路id，线路名，站点序号，站点名称
        sql='insert into buss_station(lineid,busname,seq,name)\
        values("%s","%s","%s","%s")'%(d)
        con.execute(sql)
    con.commit()
    con.close() 
	

def main():
	hrefs=get_row()
	print len(hrefs)
	for i in hrefs:
		print i
		get_data(i)
		time.sleep(2)
	loggs('完成')	
if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		loggs(e)		