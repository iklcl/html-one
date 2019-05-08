#coding=utf-8

#文件名称:菏泽市.py
#作者：huanghong
#创建日期：2017-9-1
#功能描述：菏泽市登记信息公示
#网页地址：q
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
lock = threading.Lock()
headers={
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
		}
path2=unicode(sys.path[0]+'\\readme.txt','utf-8')
href_list=[]
links=[]

path1=unicode(sys.path[0]+'\\信息连接.csv','utf-8')
logg=unicode(sys.path[0]+'\\logs.log','utf-8')
#log日志
def loggs(strs):
    with open(logg,'ab') as f:
        time = str(datetime.now())[:-7]
        t = os.linesep
        s = time+' : '+str(strs)
        print s
        f.write(s+t)	
def get_href():	
	for i in range(10):
		url='http://www.hz-redshield.com.cn/eportal/ui?pageId=762011&currentPage='+str(i)+'&moduleId=049eb719cf09460192cd347478052a38'
		req=requests.get(url,headers=headers).content.decode('utf-8','ignore')
		pages = etree.HTML(req)			
		a = pages.xpath(u"//div[@class='lw_wz_change']/span[position()>1]/a/@href")
		for link in a:
			href='http://www.hz-redshield.com.cn'+link
			href_list.append(href)
def get_link():
	while True:
		lock.acquire()
		if len(href_list)==0:
			lock.release()
			break
		else:
			url=href_list.pop(0)
			lock.release()
			# url='http://www.hz-redshield.com.cn/eportal/ui?pageId=725536&articleKey=857006&columnId=762011'	
			html=requests.get(url,headers=headers).content.decode('utf-8','ignore')
			html=etree.HTML(html)
			txt=html.xpath(u"//tr[position()<2]/td/text()")[0]
			key = re.findall(u'名单|公示|表|登记信息',txt)
			if len(key)!=0:				
				links.append(url)


def get_data(Link):
	it=0
	while True:
		it=it+1
		li=[]
		lock.acquire()
		if len(Link)==0:
			lock.release()
			break
		else:
			url=Link.pop(0)
			lock.release()			
			print url
			html=requests.get(url,headers=headers).content.decode('utf-8','ignore')
			html=etree.HTML(html)	
			txt=html.xpath(u"//tr[position()<2]/td/text()")[0]
			href=html.xpath(u"//div[@id='Zoom']/p/a/@href")
			wei=html.xpath(u"//div[@id='Zoom']/p/a/text()")[0]
			key2 = re.findall(r'\.([a-z]{3})',wei)
			if len(key2)!=0:					
				for i in href:
					it=it+1		
					link='http://www.hz-redshield.com.cn'+i										
					lock.acquire()
					urllib.urlretrieve(link,sys.path[0]+"\\data"+"\\"+"%s%s.%s"%(txt,it,key2[0]))
					lock.release()
					lock.acquire()
					li.append(url)
					li.append(txt)
					li.append(link)
					with codecs.open(path1,'ab') as f:
						w = csv.writer(f)
						w.writerow(li)	
					lock.release()										
			else:
				for i in href:
					it=it+1			
					link='http://www.hz-redshield.com.cn'+i									
					lock.acquire()
					urllib.urlretrieve(link,sys.path[0]+"\\data"+"\\"+"%s%s.xls"%(txt,it))
					lock.release()
					lock.acquire()
					li.append(url)
					li.append(txt)
					li.append(link)
					with codecs.open(path1,'ab') as f:
						w = csv.writer(f)
						w.writerow(li)	
					lock.release()	
def main1():
	get_href()	
	path = u"data"
	new_path = os.path.join(path)
	if not os.path.isdir(new_path):
		os.makedirs(new_path)
	else:
		print path+'目录已存在'
	with codecs.open(path1,'wb') as f:
		w= csv.writer(f)	
		w.writerow([u'网页连接',u'数据名称',u'下载连接'])
	tasks = [] #任务列表
	for x in range(5):
		t = threading.Thread(target=get_link) #准备线程函数及参数
		t.setDaemon(True) #设置守护线程（主线程退出，子线程也会退出，不会挂起占用资源）
		tasks.append(t)
	for t in tasks:
		t.start() #启动多线程（任务列表有多少个值，就会启动多少个线程）
	for t in tasks:
		t.join()
	Link=list(set(links))	
	tasks2 = [] #任务列表
	for x in range(5):
		t2 = threading.Thread(target=get_data,args=(Link,)) #准备线程函数及参数
		t2.setDaemon(True) #设置守护线程（主线程退出，子线程也会退出，不会挂起占用资源）
		tasks2.append(t2)
	for t2 in tasks2:
		t2.start() #启动多线程（任务列表有多少个值，就会启动多少个线程）
	for t2 in tasks2:
		t2.join()	
def read_line():
	ap=[]
	with codecs.open (path1,'r') as f:
		a=f.readlines()
		for i in a:
			p = i.split(',')
			ap.append(p[0])
	return ap	



def gengxin():
	href=read_line()
	get_href()
	tcpr=[]
	tasks = [] #任务列表
	for x in range(5):
		t = threading.Thread(target=get_link) #准备线程函数及参数
		t.setDaemon(True) #设置守护线程（主线程退出，子线程也会退出，不会挂起占用资源）
		tasks.append(t)
	for t in tasks:
		t.start() #启动多线程（任务列表有多少个值，就会启动多少个线程）
	for t in tasks:
		t.join()
	Link=list(set(links))
	for i in Link:
		if i not in href:
			tcpr.append(i)
	tasks2 = [] #任务列表
	for x in range(5):
		t2 = threading.Thread(target=get_data,args=(tcpr,)) #准备线程函数及参数
		t2.setDaemon(True) #设置守护线程（主线程退出，子线程也会退出，不会挂起占用资源）
		tasks2.append(t2)
	for t2 in tasks2:
		t2.start() #启动多线程（任务列表有多少个值，就会启动多少个线程）
	for t2 in tasks2:
		t2.join()


def main():
	with codecs.open (path2,'r') as f:
		a=f.readlines()
		key2 = re.findall(r'(\d)',a[0])
		if key2[0]=='0':
			filename=path1
			if os.path.exists(filename):
				print u'更新数据'
				gengxin()#调用更新函数
			else:
				lock = threading.Lock()
				main1()#调用存入函数	
		else:
			gengxin()
		loggs('完成')
if __name__ == '__main__':
	main()
	# try:
	# 	main()
	# except Exception as e:
	# 	loggs(e)
					