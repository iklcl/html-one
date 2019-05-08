#coding=utf-8

#文件名称：suqian1.py
#作者：huanghong
#创建日期：2017-8-23
#功能描述：徐州市新设立企业公告
#网页地址：http://www.sqgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=95000000&queryType=6
#处理进度：已完成（待优化）

import requests
from lxml import etree
import sys
import codecs,csv
from bs4 import BeautifulSoup
import urllib
import urllib2
import re
import os.path
import threading
from datetime import datetime

reload(sys)
sys.setdefaultencoding('utf-8')
uipath = unicode(sys.path[0]+'\\宿迁市设立企业公告.csv' , 'utf-8')
path1=unicode(sys.path[0]+'\\readme.txt','utf-8')
uipath2 = unicode(sys.path[0]+'\\宿迁市设立企业公告更新部分.csv' , "utf-8")
headers={
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
		}
#获取网页页数
Href=[]
Link=[]		

logg=unicode(sys.path[0]+'\\logs.log','utf-8')


#log日志
def loggs(strs):
    with open(logg,'ab') as f:
        time = str(datetime.now())[:-7]
        t = os.linesep
        s = time+' : '+str(strs)
        print s
        f.write(s+t)
#获取网页页数


def get_page():
	r=requests.get('http://www.sqgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=95000000&queryType=6',headers=headers)
	html=r.content
	soup=BeautifulSoup(html,'lxml')
	table=soup.find_all('table',width="90%")[0]	
	td=table.select('td[align=right]')[0].text
	page=re.findall(u'共(\d*)页',td)
	return page#总页数



#传入参数，获取网页数据
def get_href():
	while True:
		lock.acquire()
		if len(Link)==0:
			lock.release()
			break
		else:
			url=Link.pop(0)
			lock.release()	
			html=requests.get(url,headers=headers).content
			print url
			pages = etree.HTML(html.decode('utf-8'))
			a = pages.xpath(u"//table[@width='700']/tr[position("u")>1]/td/a/@onclick")
			for i in a:
				t=i.replace('javaScript:window.open(\'','').replace('\',\'a\',\'width=550 height=350\')','')
				url2='http://www.sqgsj.gov.cn/baweb/show/shiju/'+t
				print url2
				Href.append(url2)

def get_data():
	while True:
		lock.acquire()
		if len(Href)==0:
			lock.release()
			break
		else:
			url3=Href.pop(0)
			lock.release()
			html=requests.get(url3,headers=headers).content
			pages = etree.HTML(html.lower().decode('utf-8'))
			text= pages.xpath(u"//table[@width='427']/tr/td[position()>1]/input/@value")
			for i in range(0, len(text),6):					
				ta=text[i:i+6]
				print ta
				ta.append(url3)
				lock.acquire()
				with codecs.open(uipath,'ab') as f:
					w = csv.writer(f)
					w.writerow(ta)
				lock.release()
#调用以上函数，把数据写入csv
def main2():
	pages=get_page()
	for i in range(1,int(pages[0])+1):
		url=("http://www.sqgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=95000000&total=22064&queryType=6&pagenum="+str(i)+"&action=gg.jsp?ssid=ZxSlh1DBkGGpV2hnWMSt5PG7f8FPjTbvH78vJ1nFcwYyMhWzGBzy!1470507879!1500631589968&findWenhao=&findName=")
		Link.append(url)
	with codecs.open(uipath,'wb') as f:
		f.write(codecs.BOM_UTF8)
		w = csv.writer(f)
		w.writerow([u'企业注册号',u'企业名称',u'法定代表人（负责人）',u'企业住所',u'企业类型',u'时间',u'源链接'])
	tasks2 = [] #任务列表
	for x in range(5):
		t2 = threading.Thread(target=get_href) #准备线程函数及参数
		t2.setDaemon(True) #设置守护线程（主线程退出，子线程也会退出，不会挂起占用资源）
		tasks2.append(t2)
	for t2 in tasks2:
		t2.start() #启动多线程（任务列表有多少个值，就会启动多少个线程）
	for t2 in tasks2:
		t2.join() #等待线程执行结束  # 启动多线程（任务列表有多少个值，就会启动多少个线程）

	tasks = [] #任务列表
	for x in range(5):
		t = threading.Thread(target=get_data) #准备线程函数及参数
		t.setDaemon(True) #设置守护线程（主线程退出，子线程也会退出，不会挂起占用资源）
		tasks.append(t)
	for t in tasks:
		t.start() #启动多线程（任务列表有多少个值，就会启动多少个线程）
	for t in tasks:
		t.join() #等待线程执行结束  # 启动多线程（任务列表有多少个值，就会启动多少个线程）


#==================================================================================================================================
#以下为用于更新的代码

def time_x():
	with codecs.open (path1,'r') as f:
		a=f.readlines()
		key2 = re.findall(r'(\d+)',a[-1])
	return int(key2[0])
		


#读上次数据时间
def read_set1():
	v=[]
	with codecs.open (uipath,'r') as f:
		a=f.readlines()
		for i in a:
			b1=re.findall('(\d+-\d+-\d+)',i)
			for i in b1:
				bi=i.split('-')
				data=int(bi[0])*10000+int(bi[1])*100+int(bi[2])*1
				v.append(data)
	v.sort()			
	return v[-1]

def read_set2():
	v=[]
	with codecs.open (uipath2,'r') as f:
		a=f.readlines()
		for i in a:
			b1=re.findall('(\d+-\d+-\d+)',i)
			for i in b1:
				bi=i.split('-')
				data=int(bi[0])*10000+int(bi[1])*100+int(bi[2])*1
				v.append(data)
	v.sort()			
	return v[-1]	



#获取更新部分的数据
def get_data1():
	s1=time_x()	
	d=[]		
	ti=0
	while True:
		ti=ti+1
		url=("http://www.sqgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=95000000&total=22064&queryType=6&pagenum="+str(ti)+"&action=gg.jsp?ssid=ZxSlh1DBkGGpV2hnWMSt5PG7f8FPjTbvH78vJ1nFcwYyMhWzGBzy!1470507879!1500631589968&findWenhao=&findName=")
		# 定义url，传入数据

		html=requests.get(url,headers=headers).content
		print url
		print u'正在读取第'+str(ti)+u'页数据'
		
		pages = etree.HTML(html.decode('utf-8'))
		a = pages.xpath(u"//table[@width='700']/tr[position("u")>1]/td/a/@onclick")
		for i in a:
			t=i.replace('javaScript:window.open(\'','').replace('\',\'a\',\'width=550 height=350\')','')		
			url='http://www.sqgsj.gov.cn/baweb/show/shiju/'+t
			print url
			html=requests.get(url,headers=headers).content
			pages = etree.HTML(html.lower().decode('utf-8'))
			a = pages.xpath(u"//table[@width='427']/tr/td[position()>1]/input/@value")
			for i in range(0, len(a),6):					
				b=a[i:i+6]
				b.append(url)
				a6=b[5].split('-')
				datsa=int(a6[0])*10000+int(a6[1])*100+int(a6[2])			 
				if datsa>s1:
					d.append(b)	
				else:
					print u'更新完成'						
					return d[::-1]

#将得到的数据编排，写入csv
def main1():		
	data=get_data1()
	print u'完成'	
	with codecs.open(uipath,'ab') as f:
		w = csv.writer(f)
		for i in data:		
			w.writerow(i)
def gengxin():
	Data=get_data1()
	with codecs.open(uipath2, 'ab') as f:		
		w = csv.writer(f)
		for i in Data:
			w.writerow(i)

#判段更新还是存入
def main():
	with codecs.open (path1,'r') as f:
		a=f.readlines()
		key2 = re.findall(r'(\d)',a[0])
		if key2[0]=='0':
			#判段更新还是存入
			filename=uipath
			if os.path.exists(filename):
				print u'更新数据'
				main1()#调用更新函数
			else:
				lock = threading.Lock()
				main2()#调用存入函数	

			times=read_set1()
			print times
			with codecs.open(path1,'ab') as f:	
				f.writelines('上次数据最新时间：'+str(times)+'\r\n')
		else:
			if os.path.exists(uipath2):
				gengxin()
			else:
				print u'准备读取数据'
				with codecs.open(uipath2, 'wb') as f:
					w = csv.writer(f)
					w.writerow([u'企业名称',u'企业注册号/统一社会信用代码',u'登记机关',u'企业类型',u'注销登记时间',u'源链接'])	
				gengxin()
			times=read_set2()
			print times
			with codecs.open(path1,'ab') as f:	
				f.writelines('上次数据最新时间：'+str(times)+'\r\n')
		loggs(u'完成')


if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		loggs(e)
