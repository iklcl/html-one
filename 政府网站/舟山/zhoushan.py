#coding=utf-8
#文件名称：zhoushan.py
#作者：huanghong
#创建日期：2017-8-8
#功能描述：舟山市新设立、注销、吊销企业
#网页地址：http://www.zsscjg.gov.cn/QYDJGG/QYDJGG.html
#处理进度：已完成
import requests
from lxml import etree
import sys
import codecs,csv
from bs4 import BeautifulSoup
import urllib
import urllib2
import re
import os.path
reload(sys)
sys.setdefaultencoding('utf-8')
uipath = unicode(sys.path[0]+'\\舟山市1.csv' , 'utf-8')
uipath2 = unicode(sys.path[0]+'\\舟山市更新部分.csv' , 'utf-8')
path1=unicode(sys.path[0]+'\\off.txt','utf-8')


headers={
			"Host":"www.zsscjg.gov.cn",
			"Referer":"http://www.zsscjg.gov.cn/QYDJGG/QYDJGG_2.html",
			"Upgrade-Insecure-Requests":"1",
			"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
			}

#获取网页页数			
def get_page():
	r=requests.get('http://www.zsscjg.gov.cn/QYDJGG/QYDJGG_1.html',headers=headers)
	# print r.content
	html=r.content
	soup=BeautifulSoup(html,'lxml')
	table=soup.select('div[id="AllowPagePanel"]')[0]
	td=table.select('div[style="float: left;color:#505050"]')[0].text
	page=re.findall(u'\d/(\d*?)$',td)
	return page
	# return page#总页数

#传入参数，获取网页数据
def get_data(page):
	for i in page:	
		for  j in xrange(1,int(i)+1):			
			url="http://www.zsscjg.gov.cn/QYDJGG/QYDJGG_"+str(j)+".html"		
		# 	# 定义url，传入数据
			r=requests.get(url,headers=headers)
			html = r.content
			pages = etree.HTML(html.lower().decode('utf-8'))
			a = pages.xpath(u"//table[@id='tb_content']/tr[position()>1]/td/text()")			
			for i in range(0, len(a),4):					
				b=a[i:i+4]
				b.append(url)
				c=','.join(b)
				d=c.split(',')
				print d
				with codecs.open(uipath,'ab') as f:
					w = csv.writer(f)		
					w.writerow(d)


#调用以上函数，把数据写入csv
def main1():
	with codecs.open(uipath,'wb') as f:
		w = csv.writer(f)
		w.writerow([u'企业名称',u'结办时间',u'登记机关',u'当前状态',u'源链接'])
	page=get_page()
	data=get_data(page)

#==================================================================================================================================
#以下为用于更新的代码
def time_x():
	with codecs.open (path1,'r') as f:
		a=f.readlines()
		key2 = re.findall(r'(\d+)',a[-1])
		if key2[0]=='0':
			k=read_set1()
			return int(k)
		else:
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
def get_data2():
	s1=time_x()
	d=[]		
	ti=0
	while True:
		ti=ti+1
	# for i in range(1,3)
		url="http://www.zsscjg.gov.cn/QYDJGG/QYDJGG_"+str(ti)+".html"			
		# 	# 	# 定义url，传入数据
		r=requests.get(url,headers=headers)
		html = r.content
		print url
		print u'正在读取第'+str(ti)+u'页数据'
		pages = etree.HTML(html.lower().decode('utf-8'))
		a = pages.xpath(u"//table[@id='tb_content']/tr[position()>1]/td/text()")
		for i in range(0, len(a),4):					
				b=a[i:i+4]
				b.append(url)
				a6=b[1].split('-')
				datsa=int(a6[0])*10000+int(a6[1])*100+int(a6[2])*1 
				if datsa>s1:
					d.append(b)	
				else:
					print u'更新完成'											
					return d[::-1]
#将得到的数据编排，写入csv

def zhuijia():
	Data=get_data2()
	with codecs.open(uipath,'ab') as f:
		w = csv.writer(f)	
		for i in Data:
			w.writerow(i)

def gengxin():
	Data=get_data2()
	with codecs.open(uipath2, 'ab') as f:		
		w = csv.writer(f)
		for i in Data:
			w.writerow(i)






#============================================================================================================================


#判段更新还是存入
#判段更新还是存入
def main():	
	with codecs.open (sys.path[0]+'\\off.txt','r') as f:
		a=f.readlines()
		key2 = re.findall(r'(\d)',a[0])
		if key2[0]=='0':
			#判段更新还是存入
			filename=uipath
			if os.path.exists(filename):
				print '准备更新数据'
				zhuijia()
			else:
				print '准备读取数据'			
				main1()		

			times=read_set1()
			print times
			with codecs.open(sys.path[0]+'\\off.txt','ab') as f:	
				f.writelines('上次数据最新时间：'+str(times)+'\r\n')
		else:
			if os.path.exists(uipath2):
				gengxin()
			else:
				print '准备读取数据'
				with codecs.open(uipath2, 'wb') as f:
					w = csv.writer(f)
					w.writerow([u'企业名称',u'结办时间',u'登记机关',u'当前状态',u'源链接'])	
				gengxin()
			times=read_set2()
			print times
			with codecs.open(sys.path[0]+'\\off.txt','ab') as f:	
				f.writelines('上次数据最新时间：'+str(times)+'\r\n')
	



if __name__ == '__main__':
	main()