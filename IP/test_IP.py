#-*- coding:utf-8 -*-
#网址：
#文件名：test_IP.py
#作者: huanghong
#创建日期: 2017-010-15
#功能描述: 检测出有用的ip
#完成状况：完成
import threading
import random
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
reload(sys)
sys.setdefaultencoding('utf-8')
lock = threading.Lock()
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    }




#查询数据
def savesql_ip(savepoint_name):
    data=[]  
    con=sqlite3.connect(savepoint_name)
    datas=con.execute('SELECT IP from data')
    for i in datas:
    	data.append(i[0]) 	
    con.commit()
    con.close()
    print len(set(data))
    return data



class ClassName:
	"""docstring for ClassName"""
	bad_ip=[]
	ipdata=[]

	def __init__(self,data):
		self.savepoint_name='IP.db'
		self.data=data
		
	def check_ip(self):
		while True:
			lock.acquire()
			if len(self.data)==0:
				lock.release()
				break
			else:
				ip=self.data.pop(0)
				lock.release()
				test_url = 'http://www.baidu.com'
				proxy = {'http': ip}
				try:
				    response = requests.get(test_url, headers=headers, proxies=proxy,timeout=5)
				    if response.status_code == 200:
				    	print 'true'
				        self.ipdata.append(ip)
				    else:
				    	time.sleep(2)
				    	response = requests.get(test_url, headers=headers, proxies=proxy,timeout=5)
				    	if response.status_code == 200:
				    		print 'true'
				        	self.ipdata.append(ip)
				    	else:
				        	self.bad_ip.append(ip)
				except Exception as e:
				    self.bad_ip.append(ip) 
				     
	# 检查出无用的数据
	def thread(self):		
		tasks = [] #任务列表
		for x in range(20):
			t = threading.Thread(target=self.check_ip) #准备线程函数及参数
			t.setDaemon(True) #设置守护线程（主线程退出，子线程也会退出，不会挂起占用资源）
			tasks.append(t)
		for t in tasks:
			t.start() #启动多线程（任务列表有多少个值，就会启动多少个线程）
		for t in tasks:
			t.join()
		print len(set(self.ipdata))
	

	#删除无用的数据
	def deletesql_ip(self):   
	    con=sqlite3.connect(self.savepoint_name)
	    con.execute('''delete from data;''')
    # 插入数据
	    for data in self.ipdata:
	        sql='insert into data(IP) values("%s")'%(data)
	        con.execute(sql)    
	    con.commit()
	    con.close()
	def save_badIP(self):
    #创建数据库
	    con=sqlite3.connect('IP2.db')
	    con.execute('''CREATE TABLE IF NOT  EXISTS data
	        (
	        IP varchar(100) NOT NULL);''')
	    # 插入数据
	    for data in self.bad_ip:
	        sql='insert into data(IP) values("%s")'%(data)
	        con.execute(sql)
	    con.commit()
	    con.close()

def main1():
	datas=savesql_ip('IP.db')
	data_ip=list(set(datas))
	check=ClassName(data_ip)
	check.thread()
	check.deletesql_ip()
	check.save_badIP()
def main2():
	datas=savesql_ip('IP2.db')
	data_ip=list(set(datas))
	check=ClassName(data_ip)
	check.thread()
	check.deletesql_ip()
	check.save_badIP()
def main():
	main1()
	main2()
if __name__ == '__main__':
	main()
	# datas=savesql_ip('IP.db')
	# print len(datas),len(set(datas))