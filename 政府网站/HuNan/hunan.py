#coding=utf-8

#文件名称：jiaozuo.py
#作者：huanghong
#创建日期：2017-9-14
#功能描述：湖南省新设立、注销、吊销企业，表格下载
#网页地址：http://www.hnaic.gov.cn/visit/socialservice/a/listenternotice?unitecodeIndex=430000
#处理进度：已完成（待优化）
import time
import threading
import requests
from lxml import etree
import lxml.html
import sys
import codecs,csv
from bs4 import BeautifulSoup
import urllib
import urllib2
import re
import os.path
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf-8')
path1=unicode(sys.path[0]+'\\readme.txt','utf-8')
logg=unicode(sys.path[0]+'\\logs.log','utf-8')
upath1=unicode(sys.path[0]+'\\湖南省信息公告.csv','utf-8')
headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}
link1=[]
link2=[]
link3=[]
link4=[]
def loggs(strs):
    with open(logg,'ab') as f:
        time = str(datetime.now())[:-7]
        t = os.linesep
        s = time+' : '+str(strs)
        print s
        f.write(s+t)
def get_page():
    req=requests.get('http://www.hnaic.gov.cn/visit/socialservice/a/listenternotice?unitecodeIndex=430000',headers=headers).content.decode('gbk','ignore') 
    pages = etree.HTML(req)
    a = pages.xpath(u"//tr[@class='pager']/td/text()")[0]
    page=re.findall(u'\d+',a)[1]
    return page
			
def get_href():
	page=get_page()
	ii=0
	while True:
		ii=ii+1
		if ii>int(page):
			break
		url='http://www.hnaic.gov.cn/visit/socialservice/a/listenternotice?unitecodeIndex=430000&currentP=%s'%ii
		req=requests.get(url,headers=headers).content.decode('gbk','ignore')
		html=etree.HTML(req)
		href=html.xpath(u"//div[@id='biaoge']/ul/li[@class='biaotou1']/a/@href")
		name=html.xpath(u"//div[@id='biaoge']/ul/li[@class='biaotou1']/a/text()")
		da=zip(name,href)
		for i in da:
			print i[1]
			zhuxiao=re.findall(u'注销',i[0])
			sheli=re.findall(u'设立',i[0])
			biangeng=re.findall(u'变更',i[0])
			zhunhe=re.findall(u'核准',i[0])
			if len(zhuxiao)==1:
				link1.append(i[1])
			if len(sheli)==1:
				link2.append(i[1])
			if len(biangeng)==1:
				link3.append(i[1])
			if len(zhunhe)==1:
				link4.append(i[1])			

def get_data():	
	for i1 in link1:
		url1='http://www.hnaic.gov.cn'+i1
		req1=requests.get(url1,headers=headers).content.decode('gbk','ignore')
		html=etree.HTML(req1)
		data=html.xpath(u"//table[@align='center']/tr[position()>1]/td/text()")
		print url1
		for t in range(0,len(data),3):
			text=data[t:t+3]
			text.append(u'注销')
			text.append(url1) 
			with codecs.open(upath1,'ab') as f:
				w = csv.writer(f)		
				w.writerow(text)
	for i2 in link2:
		url2='http://www.hnaic.gov.cn'+i2
		req2=requests.get(url2,headers=headers).content.decode('gbk','ignore')
		html=etree.HTML(req2)
		data=html.xpath(u"//table[@align='center']/tr[position()>1]/td/text()")
		print url2
		for t in range(0,len(data),3):
			text=data[t:t+3]
			text.append(u'设立')
			text.append(url2)  
			with codecs.open(upath1,'ab') as f:
				w = csv.writer(f)		
				w.writerow(text)
	for i3 in link3:
		url3='http://www.hnaic.gov.cn'+i3
		req3=requests.get(url3,headers=headers).content.decode('gbk','ignore')
		html=etree.HTML(req3)
		data=html.xpath(u"//table[@align='center']/tr[position()>1]/td/text()")
		print url3
		for t in range(0,len(data),3):
			text=data[t:t+3]
			text.append(u'变更') 
			text.append(url3) 
			with codecs.open(upath1,'ab') as f:
				w = csv.writer(f)		
				w.writerow(text)
	for i4 in link4:
		url4='http://www.hnaic.gov.cn'+i4
		req4=requests.get(url4,headers=headers).content.decode('gbk','ignore')
		html=etree.HTML(req4)
		data=html.xpath(u"//table[@align='center']/tr[position()>1]/td/text()")
		print url4
		for t in range(0,len(data),3):
			text=data[t:t+3]
			text.append(u'名称核准')
			text.append(url4)  
			with codecs.open(upath1,'ab') as f:
				w = csv.writer(f)		
				w.writerow(text)
def main1():
	with codecs.open(upath1,'wb') as f:
		w= csv.writer(f)
		w.writerow([u'通知书文号/统一社会信用代码/注册号',u'企业名称',u'日期',u'源连接'])												
	get_href()				
	get_data()		


#===============================================================================================================
#以下为用于更新的代码
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
			b1=re.findall('(\d+-\d+-\d+)',i)
			for i in b1:
				bi=i.split('-')
				data=int(bi[0])*10000+int(bi[1])*100+int(bi[2])*1
				v.append(data)
	v.sort()			
	return v[-1]




def get_href1():
	ii=0
	sl=time_x()
	while True:
		ii=ii+1
		if ii>10000:
			break
		url='http://www.hnaic.gov.cn/visit/socialservice/a/listenternotice?unitecodeIndex=430000&currentP=%s'%ii
		req=requests.get(url,headers=headers).content.decode('gbk','ignore')
		html=etree.HTML(req)
		numb=html.xpath(u"//div[@id='biaoge']/ul/li[@class='biaotou3']/text()")
		href=html.xpath(u"//div[@id='biaoge']/ul/li[@class='biaotou1']/a/@href")
		name=html.xpath(u"//div[@id='biaoge']/ul/li[@class='biaotou1']/a/text()")
		da=zip(name,href,numb)
		for i in da:
			a6=i[2].split('-')
			amub=int(a6[0])*10000+int(a6[1])*100+int(a6[2])*1
			if amub>sl:
				zhuxiao=re.findall(u'注销',i[0])
				sheli=re.findall(u'设立',i[0])
				biangeng=re.findall(u'变更',i[0])
				zhunhe=re.findall(u'核准',i[0])
				if len(zhuxiao)==1:
					link1.append(i[1])
				if len(sheli)==1:
					link2.append(i[1])
				if len(biangeng)==1:
					link3.append(i[1])
				if len(zhunhe)==1:
					link4.append(i[1])
			else:
				ii=10000	
					
def gengxin():
	get_href1()
	get_data()


def chongzhi():
	with codecs.open(upath1,'wb') as f:
		w= csv.writer(f)
		w.writerow([u'通知书文号/统一社会信用代码/注册号',u'企业名称',u'日期',u'源连接'])												
	get_href1()				
	get_data()	



#判段更新还是存入
#判段更新还是存入
def main():	
	with codecs.open (path1,'r') as f:
		a=f.readlines()
		key2 = re.findall(r'(\d)',a[0])
		if key2[0]=='0':
			#判段更新还是存入
			filename=unicode(sys.path[0]+'\\湖南省信息公告.csv','utf-8')
			if os.path.exists(filename):
				print u'准备更新数据'
				gengxin()
			else:
				print u'准备读取数据'			
				main1()		

			times=read_set1()
			print times
			with codecs.open(path1,'ab') as f:	
				f.writelines('上次数据最新时间：'+str(times)+'\r\n')
		else:
			uipath2=unicode(sys.path[0]+'\\湖南省信息公告.csv','utf-8')
			if os.path.exists(uipath2):
				gengxin()
			else:
				chongzhi()
			times=read_set1()
			print times
			with codecs.open(path1,'ab') as f:	
				f.writelines('上次数据最新时间：'+str(times)+'\r\n')
		loggs('完成')



if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		loggs(e)