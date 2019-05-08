#coding=utf-8

#文件名称：zuzhou3.py
#作者：huanghong
#创建日期：2017-8-9
#功能描述：徐州市新吊销企业公告
#网页地址：http://www.xzgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=95000000&queryType=8
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
reload(sys)
sys.setdefaultencoding('utf-8')

headers={
		"Host":"www.xzgsj.gov.cn",
		"Referer":"http://www.xzgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=96000000&total=7652&queryType=7&pagenum=2&action=pagin&findWenhao=&findName=",
		"Upgrade-Insecure-Requests":"1",
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
		}
path1=unicode(sys.path[0]+'\\readme.txt','utf-8')
uipath = unicode(sys.path[0]+'\\徐州市新吊销企业公告.csv ', 'utf-8')
uipath2 = unicode(sys.path[0]+'\\徐州市新吊销企业公告更新部分.csv' , "utf-8")
Href=[]
Link=[]
lock = threading.Lock()		
#获取网页页数
def get_page():
	r=requests.get('http://www.xzgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=95000000&queryType=8',headers=headers)
	# print r.content
	html=r.content
	soup=BeautifulSoup(html,"lxml")
	table=soup.select('table[width=90%]')[0]
	td=table.select('td[align=right]')[0].text
	page=re.findall(u'共(\d*)页',td)
	return page#总页数

#传入参数，获取网页数据
def get_href(page):
	
	for  i in range(1,int(page)+1):		
		url="http://www.xzgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=95000000&total=7652&queryType=8&pagenum="+str(i)+"&action=gg.jsp?ssid=ZxSlh1DBkGGpV2hnWMSt5PG7f8FPjTbvH78vJ1nFcwYyMhWzGBzy!1470507879!1500631589968&findWenhao=&findName="		
		# 定义url，传入数据
		r=requests.get(url,headers=headers)
		html = r.content
		pages = etree.HTML(html.decode('utf-8'))
		a = pages.xpath(u"//table[@width='700']/tr[position("u")>1]/td/a/@onclick")
		for i in a:
			a=i.replace('javaScript:window.open(\'','').replace('\',\'a\',\'width=550 height=350\')','')
			url='http://www.xzgsj.gov.cn/baweb/show/shiju/'+a
			r=requests.get(url,headers=headers)
			html = r.content
			pages = etree.HTML(html.lower().decode('utf-8'))
			a = pages.xpath(u"//table[@width='427']/tr/td[position()>1]/input/@value")
			b=[]
			for i in range(0, len(a),6):
				t=a[i:i+6]
				t.append(url)							
				with codecs.open(u'徐州市新吊销企业公告.csv','ab') as f:
					w = csv.writer(f)
					w.writerow(t)

				#写入数据
#调用以上函数，把数据写入csv
def main2():
	with codecs.open(uipath,'wb') as f:
			f.write(codecs.BOM_UTF8)
			w = csv.writer(f)
			w.writerow([u'企业注册号',u'企业名称',u'法定代表人（负责人）',u'企业住所',u'企业类型',u'吊销日期',u'源链接'])
	pages=get_page()
	for i in pages:
		href=get_href(i)
		


#==================================================================================================================================
#以下为用于更新的代码

def time_x():
	k=read_set1()
	with codecs.open (path1,'r') as f:
		a=f.readlines()
		key2 = re.findall(r'(\d+)',a[-1])
		try:
			if int(key2[0])<int(k):
				return int(k)
			else:
				return int(key2[0])
		except Exception as e:
			k=read_set1()
			return int(k)	


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
def get_data2():
	s1=time_x()	
	d=[]		
	ti=0
	while True:
		ti=ti+1
		url=("http://www.xzgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=95000000&total=7652&queryType=8&pagenum="+str(ti)+"&action=gg.jsp?ssid=ZxSlh1DBkGGpV2hnWMSt5PG7f8FPjTbvH78vJ1nFcwYyMhWzGBzy!1470507879!1500631589968&findWenhao=&findName=")
		# 定义url，传入数据
		r=requests.get(url,headers=headers)
		html = r.content
		print u'正在读取第'+str(ti)+u'页数据'
		# print html
		pages = etree.HTML(html.decode('utf-8'))
		a = pages.xpath(u"//table[@width='700']/tr[position("u")>1]/td/a/@onclick")
		for i in a:
			t=i.replace('javaScript:window.open(\'','').replace('\',\'a\',\'width=550 height=350\')','')			
			url='http://www.xzgsj.gov.cn/baweb/show/shiju/'+t
			# print url
			r=requests.get(url,headers=headers)
			html = r.content
			pages = etree.HTML(html.lower().decode('utf-8'))
			a = pages.xpath(u"//table[@width='427']/tr/td[position()>1]/input/@value")
			

			for i in range(0, len(a),6):					
				b=a[i:i+6]
				b.append(url)
				a6=b[5].split('-')
				datsa=int(a6[0])*1000+int(a6[1])*100+int(a6[2])*1 				 
				if datsa>s1:
					d.append(b)

				else:
					print u'更新数据'													
					return d[::-1]






#将得到的数据编排，写入csv
def main1():		
	data=get_data2()		
	with codecs.open(uipath,'ab') as f:
		w = csv.writer(f)
		for i in data:		
			w.writerow(i)


def gengxin():
	Data=get_data2()
	with codecs.open(uipath2, 'ab') as f:		
		w = csv.writer(f)
		for i in Data:
			w.writerow(i)







#============================================================================================================================


def main():
	with codecs.open (path1,'r') as f:
		a=f.readlines()
		key2 = re.findall(r'(\d)',a[0])
		if key2[0]=='0':
			#判段更新还是存入
			filename=uipath
			if os.path.exists(filename):
				print '准备更新数据'
				main1()
			else:
				print '准备读取数据'
				main2()	
			times=read_set1()
			print times
			with codecs.open(path1,'ab') as f:	
				f.writelines('上次数据最新时间：'+str(times)+'\r\n')
		else:
			if os.path.exists(uipath2):
				gengxin()
			else:
				print '准备读取数据'
				with codecs.open(uipath2, 'wb') as f:
					w = csv.writer(f)
					w.writerow([u'企业名称',u'企业注册号/统一社会信用代码',u'登记机关',u'企业类型',u'注销登记时间',u'源链接'])	
				gengxin()
			times=read_set2()
			print times
			with codecs.open(path1,'ab') as f:	
				f.writelines('上次数据最新时间：'+str(times)+'\r\n')
	


if __name__ == '__main__':
			main()		