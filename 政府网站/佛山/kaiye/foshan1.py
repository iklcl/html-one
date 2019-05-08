#coding=utf-8

#文件名称：foshan1.py
#作者：huanghong
#创建日期：2017-8-10
#功能描述：佛山市企业新开公告
#网页地址：http://www.fsaic.gov.cn/gsgg/qykygg/index.html
#处理进度：已完成（待优化）
import requests
from lxml import etree
import sys
import codecs,csv
from bs4 import BeautifulSoup
import urllib
import urllib2
import re
import time
import os.path
import threading
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
}
path = unicode(sys.path[0]+'\\data','utf-8')
path1=unicode(sys.path[0]+'\\信息连接.csv','utf-8')
path2=unicode(sys.path[0]+'\\readme.txt','utf-8')
path3=unicode(sys.path[0]+'\\佛山市工商局企业开业公告.csv','utf-8')
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
	b=[]
	t=[]
	for i in range(0,7):
		if i==0:
			url="http://www.fsaic.gov.cn/gsgg/qykygg/index.html"
		else:
			url="http://www.fsaic.gov.cn/gsgg/qykygg/index_"+str(i)+".html"
		res=requests.get(url)
		time.sleep(1)
		html=res.content		
		pages = etree.HTML(html)
		a = pages.xpath(u'//td[@class="right"]/li/a/@href')		
		for i in a:
			i=i.strip('.')
			if i!='/200907/t20090703_1243771.htm':
				href='http://www.fsaic.gov.cn/gsgg/qykygg'+i
				b.append(href)
		text=pages.xpath(u'//td[@class="right"]/li/a/text()')
		for it in text:
			t.append(it)
	c=zip(b,t)
	return c
def get_data(href):
	index=re.findall(r'.htm',href[0])
	if len(index)!=0:
		print href[0]
		res=requests.get(href[0]).content.decode('gb2312','ignore')
		xls=re.findall(r'href="./.*?.xls"',res)		
		if len(xls)==0:			
			soup=BeautifulSoup(res,"lxml")
			table=soup.find_all('tbody')[0]
			time.sleep(1)
			title=table.find_all('tr')[0].text
			p=title.split('\n')
			lis=[x for x in p if x!='']
			a=table.text.replace(u'注册号','').replace('序号','').replace(u'/负责人/首席代表','').replace(u'企业名称','').replace(u'地址','').replace(u'法定代表人','').replace(u'统计结果：','').replace(u'统一社会信用代码','').replace(u'\u3000','')
			a1=a.split('\n')
			new_list = [ x for x in a1 if x !='']
			if len(lis)==3:	
				for i in range(0, len(new_list),3):
					b=new_list[i:i+3]
					b.insert(0,'')
					b.append('')
					b.append(href[0])
					with codecs.open(path3,'ab') as f:
							w = csv.writer(f)
							w.writerow(b)
			if len(lis)==4:	
				for i in range(0, len(new_list),4):
					b=new_list[i:i+4]					
					if lis[0]==u'序号':
						b[0]=''
						b.append('')
						b.append(href[0])
						with codecs.open(path3,'ab') as f:
							w = csv.writer(f)
							w.writerow(b)
					if lis[0]==u'企业名称':
						b.insert(0,'')
						b.append(href[0])
						with codecs.open(path3,'ab') as f:
							w = csv.writer(f)
							w.writerow(b)															
					else:	
						b.append('')
						b.append(href[0])
						with codecs.open(path3,'ab') as f:
								w = csv.writer(f)
								w.writerow(b)	
			if len(lis)==5:	
				for i in range(0, len(new_list),5):
					b=new_list[i:i+5]
					if lis[0]!=u'序号':	
						b.append(href[0])
						with codecs.open(path3,'ab') as f:
							w = csv.writer(f)
							w.writerow(b)
					else:
						b.pop(0)
						b.append('')
						b.append(href[0])						
						with codecs.open(path3,'ab') as f:
							w = csv.writer(f)
							w.writerow(b)	
		else:
			print u'正在下载数据保存至data文件夹中'
			urllib.urlretrieve(href[0], path+"\\"+"%s.xls"%href[1])	
			time.sleep(1)							
	#将连接保存
		with codecs.open(path1,'ab') as f:
			w = csv.writer(f)
			w.writerow([href[0],href[1]])

	else:		
		
		print u'正在下载数据保存至data文件夹中'
		urllib.urlretrieve(href[0], path+"\\"+"%s.xls"%href[1])
		with codecs.open(path1,'ab') as f:
			w = csv.writer(f)
			w.writerow([href[0],href[1]])
		time.sleep(1)
		print u'下载完成！'	

def main1():
	hrefs=get_href()
	with codecs.open(path1,'wb') as f:
		w = csv.writer(f)
		w.writerow([u'连接',u'文件名'])
	with codecs.open(path3,'wb') as f:
		w = csv.writer(f)
		w.writerow([u'企业注册号',u'企业名称',u'企业地址',u'法定代表人（负责人）',u'统一社会信用代码',u'源链接'])
	new_path = os.path.join(path)
	if not os.path.isdir(new_path):
	   	 os.makedirs(new_path)
	else:
		print path+'目录已存在'	
	for i in hrefs:
		get_data(i)

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
	link=get_href()	
	b=[]
	for i in link:
		b.append(i[0])
	for r in b:
		if r not in href:
			gengxin()
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
			new_path = os.path.join(path)
			if not os.path.isdir(new_path):
				os.makedirs(new_path)
				gengxin()
			else:
				gengxin()
		loggs('完成')

if __name__ == '__main__':
	# try:
		main()
	# except Exception as e:
	# 	loggs(e)
				

















