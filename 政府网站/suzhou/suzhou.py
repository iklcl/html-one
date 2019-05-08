#-*- coding:utf-8 -*-
#网址：http://www.jszwfw.gov.cn/jszwfw/jszwfwMap/leftmap.do?webId=1
#文件名：get_IP.py
#作者: huanghong
#创建日期: 2017-010-21
#功能描述: 江苏政务服务网
#完成状况：完成
import threading
import json
import time
import requests
from lxml import etree
import lxml.html
import sys
import codecs,csv
import re
import sqlite3
import MySQLdb as db
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf-8')
lock = threading.Lock()
headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest"
        }
class Get_data():
	"""docstring for Get_data"""
	def __init__(self, arg):
		self.arg = arg
		self.ran=[]


	def get_yibao(self):
		infornation=[]
		data={
		"webId":"1",
		"icataid":self.arg[1]
		}
		req=requests.post('http://www.jszwfw.gov.cn/jszwfw/jszwfwMap/getCgmlList.do?',headers=headers,data=data).content.replace('(','').replace(')','')
		# print req
		munber=re.findall(r'getCglb2(.*?)\'>',req.replace('&quot;','').replace('\\','').replace('\"',''))
		for i in munber:
			ids=re.findall(',(\d),\d',i)[0]
			it=re.sub(',(\d),\d',':',i).replace(':','')
			its=[ids,it]
			infornation.append(its)
			
		return infornation
	def get_page(self,ti):
		data={
			'webId':'1',
			'i_cataid':ti[1],
			'i_styletype':ti[0],
			'i':'0',
			'word':'',
			'pageno':'1'
			}
		req=requests.post('http://www.jszwfw.gov.cn/jszwfw/jszwfwMap/getCgListSearch2.do?',headers=headers,data=data).content
		times=re.findall('(\d+)页',req)
		if len(times)==0:
			time=1
		else:
			time=times[0]	
		for i in range(1,int(time)+1):
			self.ran.append(i)		
	def get_data(self,ti):
		while True:
			lock.acquire()
			if len(self.ran)==0:
				lock.release()
				break
			else:
				page=self.ran.pop(0)
				lock.release()
				data={
				'webId':'1',
				'i_cataid':ti[1],
				'i_styletype':ti[0],
				'i':'0',
				'word':'',
				'pageno':page
				}
				req=requests.post('http://www.jszwfw.gov.cn/jszwfw/jszwfwMap/getCgListSearch2.do?',headers=headers,data=data).content	
				jd = json.loads(req)
				pages = etree.HTML(jd["html"].decode('utf-8'))
				a = pages.xpath(u"//a[@class='sub_tit']/@onclick")					 
				for i in a:
					data=re.findall('\((.*)\)',i.replace('\"','').replace('\r\n',''))[0].split(',')
					tel=re.findall('(\d+-\d+|\d{11}|\d{10}|\d{8}|\d{7})',data[2])
					print i.replace('\"','').replace('\r\n','')
					print tel
					if len(tel)==0:
						mub=''
					else:
						mub=tel[0]	
					Data=[u'江苏省',data[0],data[1],mub,data[3]+','+data[4],self.arg[0]]
					lock.acquire()
					savesql(Data,'江苏政务服务网.db')
					lock.release()
				print page
			
	def finaly(self):
		munber_data=self.get_yibao()
		for mun in munber_data:
			yeshu=self.get_page(mun)
			tasks = [] #任务列表
			for x in range(10):
				t = threading.Thread(target=self.get_data,args=(mun,)) #准备线程函数
				t.setDaemon(True) #设置守护线程（主线程退出，子线程也会退出，不会挂起占用资源）
				tasks.append(t)
			for t in tasks:
				t.start() #启动多线程（任务列表有多少个值，就会启动多少个线程）
			for t in tasks:
				t.join()
			






def savesql(data,savepoint_name):
    #创建数据库
    con=sqlite3.connect(savepoint_name)
    con.execute('''CREATE TABLE IF NOT  EXISTS data
        (
        id integer primary key NOT NULL,
        province varchar(200) NOT NULL,
        type varchar(100) DEFAULT NULL,
        company varchar(1000) DEFAULT NULL, 
        salesTel varchar(100) DEFAULT NULL,
        afterSalesTel varchar(100) DEFAULT NULL,
        RescueCall varchar(100) DEFAULT NULL,
        lng varchar(100) DEFAULT NULL,
        lat varchar(100) DEFAULT NULL,
        address varchar(1000) DEFAULT NULL,
        indexUrl varchar(100) DEFAULT NULL,
        fromUrl  varchar(100) DEFAULT NULL,
        others varchar(100) DEFAULT NULL, 
        jwd varchar(100) DEFAULT NULL,
        classify varchar(100) DEFAULT NULL);''')

    # 插入数据
    sql='insert into data(province,type,company,salesTel,address,jwd,classify)\
    values("%s","%s","%s","%s","%s","%s","%s")'%(data[0],data[5],data[1],data[3],data[2],data[4],u'江苏政务服务网')
    con.execute(sql)
    con.commit()
    con.close()
def main():	
	web_data=[(u'就医保健','16','2'),(u'教育服务','17','2'),(u'纳税缴费','24','2'),(u'婚育收养','13','2'),(u'福利救助','21','2'),(u'公共安全','22','2'),(u'三农服务','18911','2'),(u'场馆设施','18','4'),(u'劳动就业','15','2')]	
	for i in web_data:
		data=Get_data(i)
		# data.get_yibao()
		data.finaly()
		time.sleep(5)
if __name__ == '__main__':
		main()		