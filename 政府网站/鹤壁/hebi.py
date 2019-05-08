#coding=utf-8

#文件名称：hebi.py
#作者：huanghong
#创建日期：2017-9-11
#功能描述：鹤壁市新设立、注销、吊销企业，表格下载
#网页地址：http://www.hbgs.gov.cn/col/col3158/index.html
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
upath3=unicode(sys.path[0]+'\\信息连接.csv','utf-8')
path1 = unicode(sys.path[0]+'\\鹤壁市公告表格','utf-8')
path2=unicode(sys.path[0]+'\\readme.txt','utf-8')
logg=unicode(sys.path[0]+'\\logs.log','utf-8')
upath2=unicode(sys.path[0]+'\\鹤壁市信息公告.csv','utf-8')
#log日志
def loggs(strs):
    with open(logg,'ab') as f:
        time = str(datetime.now())[:-7]
        t = os.linesep
        s = time+' : '+str(strs)
        print s
        f.write(s+t)

headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}
Data=[]
#获取每页的连接
def get_links():
	linkss = []
	url='http://www.hbgs.gov.cn/col/col3158/index.html'
	req=requests.get(url,headers=headers).content.decode('utf-8','ignore')
	soup=BeautifulSoup(req,"lxml")
	tbody=soup.find_all('script',language="javascript")[2]
	links=re.findall(r"../..(/art/\d+/\d+/\d+/art.*?.html)",tbody.string)
	href=set(links)
	for i in href:		
		it=("http://www.hbgs.gov.cn"+i)
		linkss.append(it)
	return linkss
	
def get_data(url):
	Data=[]
	print url
	# url='http://www.hbgs.gov.cn/art/2016/11/14/art_3158_91641.html'
	req=requests.get(url,headers=headers).content.decode('utf-8','ignore')
	href=re.findall('href="../../../..(/module/download/downfile.jsp?.*?..*?)"',req)
	if len(href)==0:
		oo=re.findall(u'序号',req)
		
		#判断是否有数据
		if len(oo)!=0:
			soup=BeautifulSoup(req,"lxml")
			tbody=soup.find_all('tbody')[1]
			tr=tbody.find_all('tr')
			
			#索引出标题位置
			for i in tr:
				xuhao=re.findall(u'序号',i.text)
				if len(xuhao)!=0:
					xy=tr.index(i)
			
			titll=tr[xy].text.replace(u'\xa0','').replace(u'            ','').replace('\r','')			
			a1=titll.split('\n')
			titllist=[x for x in a1 if x!='']
			# print titllist
			for i in xrange(0,int(xy)+1):
				tee=tr.pop(0)
			
			if len(titllist)==8:
				riqi=re.findall(u'(.*?日期)',titll)
				xingyong=re.findall(u'(.?统一社会信用代码.*)',titll)
				daibiao=re.findall(u'(法定代表人.*)',titll)
				dizhi=re.findall(u'(经营地址.*)',titll)
				dengji=re.findall(u'(登记类型|档案号|联系电话)',titll)
				mingchen=re.findall(u'(.*?企业名称)',titll)
				fanwei=re.findall(u'经营范围',titll)
				if len(riqi)==2:
					x1=titllist.index(u'核准日期')
					x2=titllist.index(xingyong[0])
					x3=titllist.index(u'成立日期')
					x4=titllist.index(mingchen[0])
					x5=titllist.index(fanwei[0])
					x6=titllist.index(dizhi[0])
					x7=titllist.index(daibiao[0])
					for i in tr:
						a5=i.text.strip('').replace(u'\u3000','').replace(u'\xa0','').split('\n')
						while True:
							if a5[0]!='':
								break
							else:
								a3=a5.pop(0)
						if len(a5)==8:
							a4=a5
						else:	
							while True:
								if a5[-1]!='':
									break
								else:
									a3=a5.pop(-1) 		
							if len(a5)!=8:
								a4=[x for x in a5 if x!='']
								if len(a4)<8:
									s=a5.pop(0)
									cs=[s]
									for i in range(0, len(a5),3):                  
										ta=a5[i:i+3]
										cs.append(ta[-1])
									a4=cs 
							else:
								a4=a5			  		
						data=[a4[x2],a4[x4],a4[x3],a4[x1],a4[x7],a4[x6],a4[x5],url]
						print data
						with codecs.open(upath2,'ab') as f:
							w = csv.writer(f)		
							w.writerow(data)
				else:	
					x1=titllist.index(riqi[0])
					x2=titllist.index(xingyong[0])
					x3=titllist.index(dengji[0])
					x4=titllist.index(mingchen[0])
					x5=titllist.index(fanwei[0])
					x6=titllist.index(dizhi[0])
					x7=titllist.index(daibiao[0])
					for i in tr:
						a5=i.text.strip('').replace(u'\u3000','').replace(u'\xa0','').split('\n')
						while True:
							if a5[0]!='':
								break
							else:
								a3=a5.pop(0)
						if len(a5)==8:
							a4=a5
						else:	
							while True:
								if a5[-1]!='':
									break
								else:
									a3=a5.pop(-1) 		
							if len(a5)!=8:
								a4=[x for x in a5 if x!='']
								if len(a4)<8:
									s=a5.pop(0)
									cs=[s]
									for i in range(0, len(a5),3):                  
										ta=a5[i:i+3]
										cs.append(ta[-1])
									a4=cs 
							else:
								a4=a5			  		
						data=[a4[x2],a4[x4],a4[x3],a4[x1],a4[x7],a4[x6],a4[x5],url]
						print data
						with codecs.open(upath2,'ab') as f:
							w = csv.writer(f)		
							w.writerow(data)

			if len(titllist)==7:
				riqi=re.findall(u'(.*?日期)',titll)
				xingyong=re.findall(u'(统一社会信用代码.*)',titll)
				daibiao=re.findall(u'(法定代表人.*)',titll)
				dizhi=re.findall(u'(经营地址.*)',titll)
				dengji=re.findall(u'(登记类型|档案号)',titll)
				mingchen=re.findall(u'(.*?企业名称)',titll)
				fanwei=re.findall(u'经营范围',titll)
				if len(daibiao)==0:
					x1=titllist.index(riqi[0])
					x2=titllist.index(xingyong[0])
					x3=titllist.index(dengji[0])
					x4=titllist.index(mingchen[0])
					x5=titllist.index(fanwei[0])
					x6=titllist.index(dizhi[0])
					for i in tr:
						a4=i.text.replace(u'\xa0','').split('\n')
						a3=a4.pop(0)
						# print a4
						data=[a4[x2],a4[x4],a4[x3],a4[x1],'',a4[x6],a4[x5],url]	
						print data
						with codecs.open(upath2,'ab') as f:
							w = csv.writer(f)		
							w.writerow(data)
				# if len(fanwei)==0:
				else:
					x1=titllist.index(riqi[0])
					x2=titllist.index(xingyong[0])
					x3=titllist.index(dengji[0])
					x4=titllist.index(mingchen[0])
					# x5=titllist.index(fanwei[0])
					x6=titllist.index(dizhi[0])
					x7=titllist.index(daibiao[0])
					for i in tr:
						a4=i.text.replace(u'\xa0','').split('\n')
						a3=a4.pop(0)
						# print a4
						data=[a4[x2],a4[x4],a4[x3],a4[x1],a4[x7],a4[x6],'',url]	
						print data									 	
						with codecs.open(upath2,'ab') as f:
							w = csv.writer(f)		
							w.writerow(data)
			if len(titllist)==5:
				mingchen=re.findall(u'(企.*?业.*?名.*?称)',titll)
				xingyong=re.findall(u'(.*?注册号)',titll) 
				x2=titllist.index(xingyong[0])
				x4=titllist.index(mingchen[0])
				x5=titllist.index(u'经营场所')							
				x7=titllist.index(u'法定代表人')			
				for i in tr:
					a4=i.text.replace(u'\xa0','').split('\n')
					a4=[x for x in a4 if x!='']
					data=[a4[x2],a4[x4],u'拟吊销','',a4[x7],'',a4[x5],url]
					print data
					with codecs.open(upath2,'ab') as f:
						w = csv.writer(f)		
						w.writerow(data)
		with codecs.open(upath3,'ab') as f:
			w = csv.writer(f)		
			w.writerow([url,'网页历史url'])					
	else:
		html=etree.HTML(req)
		name=html.xpath(u'//div[@id="zoom"]/p/a/text()')
		lis=zip(href,name)
		for i in lis:
			key2 = re.findall(r'filename=\d+.([a-z]{3})',i[0])
			link='http://www.hbgs.gov.cn'+i[0].replace('amp;','')
			print link
			urllib.urlretrieve(link, path1+'\\'+'%s.%s'%(i[1],key2[0]))
			with codecs.open(upath3,'ab') as f:
				w = csv.writer(f)		
				w.writerow([url,i[1],link])	


def main1():
	new_path = os.path.join(path1)
	if not os.path.isdir(new_path):
		os.makedirs(new_path)
	else:
		print path1+'目录已存在'
	with codecs.open(upath3, 'wb') as f:
		w = csv.writer(f)
		w.writerow([u'网页地址',u'文件名',u'下载链接'])				
	with codecs.open(upath2, 'wb') as f:
		w = csv.writer(f)
		w.writerow([u'统一社会信用代码/注册号',u'公司名称',u'登记类型',u'登记日期',u'经营范围',u'地址',u'法定代表人'])		
	links=get_links()
	for link in links:
		data=get_data(link)

def read_line():
	ap=[]
	with codecs.open (upath3,'r') as f:
		a=f.readlines()
		for i in a:
			p = i.split(',')
			ap.append(p[0])
	return ap				
def gengxin():
	hrefs=read_line()
	links=get_links()
	for i in links:
		if i not in hrefs:
			get_data(i)
	
def main():
	with codecs.open (path2,'r') as f:
		a=f.readlines()
		key2 = re.findall(r'(\d)',a[0])
		if key2[0]=='0':
			filename=upath3
			if os.path.exists(filename):
				print u'更新数据'
				gengxin()#调用更新函数
			else:
				main1()#调用存入函数	
		else:
			new_path = os.path.join(path1)
			if not os.path.isdir(new_path):
				os.makedirs(new_path)
				gengxin()
			if not os.path.isdir(upath2):
				with codecs.open(upath2, 'wb') as f:
					w = csv.writer(f)
					w.writerow([u'统一社会信用代码/注册号',u'公司名称',u'登记类型',u'登记日期',u'经营范围',u'地址',u'法定代表人'])			
			else:
				gengxin()
		loggs('完成')
if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		loggs(e)
									