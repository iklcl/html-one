#coding=utf-8

#文件名称:绍兴.py
#作者：huanghong
#创建日期：2017-8-31
#功能描述：绍兴市新注销企业公告
#网页地址：http://www.sxscjg.gov.cn/col/col49988/index.html
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
import time

reload(sys)
sys.setdefaultencoding('utf-8')
upath1=unicode(sys.path[0]+'\\绍兴市简易注销公告.csv','utf-8')
path1=unicode(sys.path[0]+'\\readme.txt','utf-8')
upath2=unicode(sys.path[0]+'\\绍兴市简易注销公告更新部分','utf-8')
logg=unicode(sys.path[0]+'\\logs.log','utf-8')
#log日志
def loggs(strs):
    with open(logg,'ab') as f:
        time = str(datetime.now())[:-7]
        t = os.linesep
        s = time+' : '+str(strs)
        print s
        f.write(s+t)
headers={
	'Host':'www.sxscjg.gov.cn',
	'Origin':'http://www.sxscjg.gov.cn',
	'Referer':'http://www.sxscjg.gov.cn/col/col49988/index.html',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'X-Requested-With':'XMLHttpReques'
}
data={
	'appid':'1',
	'webid':'84',
	'path':'/',
	'columnid':'49988',
	'sourceContentType':'1',
	'unitid':'98323',
	'webname':'绍兴市市场监督管理局',
	'permissiontype':'0'
}



def get_link():
	Link=[]
	i=1
	j=66
	while True:
		url='http://www.sxscjg.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord='+str(i)+'&endrecord='+str(j)+'&perpage=22'
		req=requests.post(url,headers=headers,data=data).content
		print url
		links=re.findall(r'(/art/\d+/\d+/\d+/art_\d+_\d+.html)',req)
		for link in links:
			url='http://www.sxscjg.gov.cn'+link
			Link.append(url)
		if len(links)==0:
			break	
		i=i+66
		j=j+66
	return Link

def get_href():
	Href=[]
	links=get_link()
	for url in links:
		req=requests.get(url,headers=headers).content
		soup=BeautifulSoup(req,'lxml')
		td=soup.find_all('td',class_="title")[0]
		page=re.findall(u'简易注销公示',td.text)
		if len(page)!=0:
			Href.append(url)
	return Href	


def get_data(url):
	#url='http://www.sxscjg.gov.cn/art/2015/11/18/art_49988_1005958.html'
	req=requests.get(url,headers=headers).content.decode('utf-8','ignore')
	soup=BeautifulSoup(req,'lxml')
	td=soup.find_all('div',id="zoom")[0]
	c=td.text.replace(u'\xa0','').replace(u'\u3000','').replace(u'\u0020','').replace(u'\u0026\u0023\u0031\u0036\u0030\u003b\u0026\u0023\u0031\u0036\u0030\u003b\u0026\u0023\u0031\u0036\u0030\u003b\u0026\u0023\u0031\u0036\u0030\u003b\u0026\u0023\u0031\u0036\u0030\u003b','').replace('\n','').replace('\t','')
	name=re.findall(u'(.*?有限公司简易注销公示)',c)	
	if len(name)!=0:
		c=c.replace(name[0],'')	
	if len(c)!=0:	
		name2=re.findall(u'(.*?有限公司|.*?有限责任公司)',c)[0]
		name88=re.findall(u'联系人',c)
		if  len(name88)!=0:	
			name3=re.findall(u'联系人：(.*?)联系电话',c)[0]	
			name4=re.findall(u'联系电话：(\d+-?\d+)联系地点',c)[0]
			name5=re.findall(u'联系地点：(.*?）)',c)[0]
			timee=re.findall(u'(\d+年\d+月\d+日)',c)[0]
			data=[name2,name3,name4,name5,timee,url]
		else:
			data=[name2]					
		with codecs.open(upath1,'ab') as f:
			w = csv.writer(f)
			w.writerow(data)

def main2():
	with codecs.open(upath1,'wb') as f:
		w= csv.writer(f)	
		w.writerow([u'公司名称',u'联系人',u'联系电话',u'联系地点',u'时间'])	
	a=get_href()
	for i in a:
		get_data(i)


#=============================================================================================================================================================
def time_x():
	with codecs.open (path1,'r') as f:
		a=f.readlines()
		key2 = re.findall(r'(\d+)',a[-1])
	return int(key2[0])
		


#读上次数据时间
def read_set1():
	v=[]
	with codecs.open (upath1,'r') as f:
		a=f.readlines()
		for i in a:
			b1=re.findall('(\d+/\d+/\d+)',i)
			for i in b1:
				bi=i.split('/')
				data=int(bi[0])*10000+int(bi[1])*100+int(bi[2])*1
				v.append(data)
	v.sort()			
	return v[-1]	
def read_set2():
	v=[]
	with codecs.open (upath2,'r') as f:
		a=f.readlines()
		for i in a:
			b1=re.findall('(\d+/\d+/\d+)',i)
			for i in b1:
				bi=i.split('/')
				data=int(bi[0])*10000+int(bi[1])*100+int(bi[2])*1
				v.append(data)
	v.sort()			
	return v[-1]

def get_data1(url):
	req=requests.get(url,headers=headers).content.decode('utf-8','ignore')
	soup=BeautifulSoup(req,'lxml')
	td=soup.find_all('div',id="zoom")[0]
	c=td.text.replace(u'\xa0','').replace(u'\u3000','').replace(u'\u0020','').replace(u'\u0026\u0023\u0031\u0036\u0030\u003b\u0026\u0023\u0031\u0036\u0030\u003b\u0026\u0023\u0031\u0036\u0030\u003b\u0026\u0023\u0031\u0036\u0030\u003b\u0026\u0023\u0031\u0036\u0030\u003b','').replace('\n','').replace('\t','')
	name=re.findall(u'(.*?有限公司简易注销公示)',c)	
	if len(name)!=0:
		c=c.replace(name[0],'')	
	if len(c)!=0:	
		name2=re.findall(u'(.*?有限公司|.*?有限责任公司)',c)[0]
		name88=re.findall(u'联系人',c)
		if  len(name88)!=0:	
			name3=re.findall(u'联系人：(.*?)联系电话',c)[0]	
			name4=re.findall(u'联系电话：(\d+-?\d+)联系地点',c)[0]
			name5=re.findall(u'联系地点：(.*?）)',c)[0]
			timee=re.findall(u'(\d+年\d+月\d+日)',c)[0]
			data=[name2,name3,name4,name5,timee,url]
		else:
			data=[name2]					
		with codecs.open(upath2,'ab') as f:
			w = csv.writer(f)
			w.writerow(data)
def main1():
	s1=time_x()		
	a=get_href()
	for it in a:
		b1=re.findall('(\d+-\d+-\d+)',it)
		for i in b1:
			bi=i.split('-')
			data=int(bi[0])*10000+int(bi[1])*100+int(bi[2])*1
			if data>s1:
				get_data(it)
def main3():
	s1=time_x()		
	a=get_href()
	for it in a:
		b1=re.findall('(\d+-\d+-\d+)',it)
		for i in b1:
			bi=i.split('-')
			data=int(bi[0])*10000+int(bi[1])*100+int(bi[2])*1
		if data>s1:
			get_data1(it)			
#============================================================================================================================
#判段更新还是存入
#判段更新还是存入
def main():
	with codecs.open (path1,'r') as f:
		a=f.readlines()
		key2 = re.findall(r'(\d)',a[0])
		if key2[0]=='0':
			#判段更新还是存入
			if os.path.exists(upath1):
				print u'更新数据'
				main1()#调用更新函数
			else:				
				main2()#调用存入函数	
			times=read_set1()
			print times
			with codecs.open(path1,'ab') as f:	
				f.writelines('上次数据最新时间：'+str(times)+'\r\n')
		else:
			if os.path.exists(upath1):
				main3()
			else:
				print u'准备读取数据'
				with codecs.open(upath2, 'wb') as f:
					w = csv.writer(f)
					w.writerow([u'公司名称',u'联系人',u'联系电话',u'联系地点',u'时间'])	
				main3()
			times=read_set2()
			print times
			with codecs.open(path1,'ab') as f:	
				f.writelines('上次数据最新时间：'+str(times)+'\r\n')
		loggs('完成')


if __name__ == '__main__':
	# try:
	# 	main()
	# except Exception as e:
	# 	loggs(e)

    	
