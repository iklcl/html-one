#coding=utf-8

#文件名称：pingding1.py
#作者：huanghong
#创建日期：2017-9-11
#功能描述：平顶山市新设立、注销、吊销企业，表格下载
#网页地址：http://www.pdsaic.gov.cn/col/col7852/index.html
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
upath1=unicode(sys.path[0]+'\\历史连接更新用.csv','utf-8')
upath3=unicode(sys.path[0]+'\\下载信息连接.csv','utf-8')
path1 = unicode(sys.path[0]+'\\平顶山市公告表格','utf-8')
path2=unicode(sys.path[0]+'\\readme.txt','utf-8')
logg=unicode(sys.path[0]+'\\logs.log','utf-8')
upath2=unicode(sys.path[0]+'\\平顶山市信息公告.csv','utf-8')
headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}

#log日志

def loggs(strs):
    with open(logg,'ab') as f:
        time = str(datetime.now())[:-7]
        t = os.linesep
        s = time+' : '+str(strs)
        print s
        f.write(s+t)
def get_links():
	linkss = []
	url='http://www.pdsaic.gov.cn/col/col7852/index.html'
	req=requests.get(url,headers=headers).content.decode('utf-8','ignore')
	soup=BeautifulSoup(req,"lxml")
	tbody=soup.find_all('script',language="javascript")[2]
	links=re.findall(r"../..(/art/\d+/\d+/\d+/art.*?.html)",tbody.string)
	href=set(links)
	for i in href:		
		it=("http://www.pdsaic.gov.cn"+i)
		linkss.append(it)
	return linkss
def get_href(url):
	req=requests.get(url,headers=headers).content.decode('utf-8','ignore')
	href=re.findall('href="../../../..(/module/download/downfile.jsp?.*?..*?)"',req)
	
	if len(href)==0:
		
		oo=re.findall(u'企.*?业.*?名.*?称',req)		
		#判断是否有数据
		if len(oo)!=0:
			print url
			soup=BeautifulSoup(req,"lxml")
			text_biaoti=soup.find_all('td',class_="text_biaoti")[0].text
			zhuxiao=re.findall(u'注销',text_biaoti)
			sheli=re.findall(u'设立',text_biaoti)
			biangeng=re.findall(u'变更',text_biaoti)
			zhunhe=re.findall(u'核准',text_biaoti)
			tbody=soup.find_all('tbody')[1]
			tr=tbody.find_all('tr')
			for i in tr:
				xuhao=re.findall(u'.*?注.*?册.*?号',i.text)
				if len(xuhao)!=0:
					xy=tr.index(i)
			title=tr[xy].text.replace(u'\xa0','').replace(u'法定代表人(负责人)',u'(负责人)').replace(u'法定代表人',u'(负责人)').replace(u'表人',u'(负责人)').replace(u'法定代','').replace(u'用代码','').replace(u'统一社会信',u'统一社会信用代码').replace(' ','').replace(u'\n             \n','').replace(u'(住所)','').replace('\r','').replace(u'\u5e8f \u53f7',u'序号').replace(u'核准日期',u'日期').replace(u'注销日期',u'日期').replace(u'登记日期',u'日期').replace(u'成立日期',u'日期').replace(u'	统一社会信用代码／注册号',u'注册号')					
			fuzeren=re.findall(u'(负责人)',title)
			a1=title.split('\n')
			if len(fuzeren)==2:
				a1.remove(u'(负责人)')
			
			for i in xrange(0,int(xy)+1):
				tee=tr.pop(0)
			titlelist=[x for x in a1 if x!='']
			titlelist.append(u'登记类型')
			datas=[]
			if len(zhuxiao)!=0:				
				for i in tr:
					lis=i.text.split('\n')
					while True:
						if lis[0]!='':
							break
						else:
							a3=lis.pop(0)
					while True:
						if lis[-1]!='':
							break
						else:
							a3=lis.pop(-1)        
					lis.append(u'注销')
					print len(lis)
					datas.append(lis)
					
			if len(sheli)!=0:				
				for i in tr:
					lis=i.text.split('\n')
					while True:
						if lis[0]!='':
							break
						else:
							a3=lis.pop(0)
					while True:
						if lis[-1]!='':
							break
						else:
							a3=lis.pop(-1)        
					lis.append(u'设立')
					print len(lis)
					datas.append(lis)
			if len(biangeng)!=0:
				for i in tr:
					lis=i.text.split('\n')
					while True:
						if lis[0]!='':
							break
						else:
							a3=lis.pop(0)
					while True:
						if lis[-1]!='':
							break
						else:
							a3=lis.pop(-1)        
					lis.append(u'变更')
					print len(lis)
					datas.append(lis)	
			if len(zhunhe)!=0:
				for i in tr:
					lis=i.text.split('\n')
					while True:
						if lis[0]!='':
							break
						else:
							a3=lis.pop(0)
					while True:
						if lis[-1]!='':
							break
						else:
							a3=lis.pop(-1)	

					lis.append(u'核准')
					print len(lis)
					datas.append(lis)
			for times in range(0,len(datas)):
				di=dict(zip(titlelist,datas[times]))
				for x in [u'(负责人)',u'登记类型',u'序号',u'统一社会信用代码',u'注册号',u'日期',u'经营地址',u'经营范围',u'变更事项',u'企业名称']:
					di.setdefault(x,'')
				liss=di[u'注册号'],di[u'企业名称'],di[u'(负责人)'],di[u'经营地址'],di[u'经营范围'],di[u'日期'],di[u'登记类型'],di[u'统一社会信用代码'],di[u'变更事项']
				liss=list(liss)
				liss.append(url)
				print liss
				with codecs.open(upath2,'ab') as f:
					w = csv.writer(f)		
					w.writerow(liss)
	else:
		print url
		print href
		soup=BeautifulSoup(req,"lxml")
		div=soup.find_all('div',id="zoom")[0]
		name=div.find_all('a',attrs={"href":re.compile(r'^../')})[0]
		a=[name.text]
		lis=zip(href,a)
		for i in lis:
			key2 = re.findall(r'filename=\d+.([a-z]{3})',i[0])
			link='http://www.pdsaic.gov.cn'+i[0].replace('amp;','')
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
		w.writerow([u'注册号',u'公司名称',u'负责人',u'登经营地址',u'经营范围',u'日期',u'登记类型',u'统一社会信用代码',u'变更事项',u'源链接'])		
	links=get_links()
	for link in links:
		data=get_href(link)
		with codecs.open(upath1,'ab') as f:
			w = csv.writer(f)		
			w.writerow([link])

def read_line():
	ap=[]
	with codecs.open (upath1,'r') as f:
		a=f.readlines()
		for  i in a:
			i=i.replace('\n','')
			ap.append(i)
	return ap		
def gengxin():
	links=get_links()
	hrefs=read_line()
	for i in links:
		if i not in hrefs:
			get_href(i)
			with codecs.open(upath1,'ab') as f:
				w = csv.writer(f)		
				w.writerow(i)
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
				main1()#调用存入函数	
		else:
			new_path = os.path.join(path1)
			if not os.path.isdir(new_path):
				os.makedirs(new_path)
				
			if not os.path.isdir(upath2):
				with codecs.open(upath2, 'wb') as f:
					w = csv.writer(f)
					w.writerow([u'注册号',u'公司名称',u'负责人',u'登经营地址',u'经营范围',u'日期',u'登记类型',u'统一社会信用代码',u'变更事项',u'源链接'])		
			gengxin()
			
		loggs('完成')
if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		loggs(e)