#-*- coding: utf8 -*-

#文件名称:gov114.py
#作者：huanghong
#创建日期：2017-1-20
#功能描述：114网获取站政府机关电话号码
#网页地址：https://114.mingluji.com/
#处理进度：已完成（待优化）



import requests
from lxml import etree
import codecs,csv
import re
import os.path
import threading
import sys
from multiprocessing import Pool,Lock
import multiprocessing
import xlrd
from collections import Counter
import copy
import time

lock = threading.Lock()
Loc = Lock()
reload(sys)
sys.setdefaultencoding('utf-8')
path1=unicode(os.path.join(sys.path[0],'政务机关电话.xlsx'),'utf-8')
path2=unicode(os.path.join(sys.path[0],'政务机关电话添加.csv'),'utf-8')
path3=unicode(os.path.join(sys.path[0],'政务机关电话验证114.xlsx'),'utf-8')
headers={
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}
class Pov114():	
	def __init__(self):
		self.set_name=[]
		self.many_name=[]
		self.name_list =self.get_name()
		print len(self.name_list[0])
		ww=self.name_list[0]
		#把带有相同名字的区分出来
		a=Counter(ww)
		dic=dict(a)
		for it in dic:
			if dic[it]==1:
				self.set_name.append(it)
			else:
				self.many_name.append(it)
		self.my_name=self.my_name()
		print len(self.set_name)			
		print len(self.many_name)
		# print len(self.my_name)
	
	#读取xlsx文件
	def my_name(self):
		name=[]
		data = xlrd.open_workbook(path1)
		table = data.sheets()[0]
		nrows = table.nrows #行数
		ncols = table.ncols #列
		for i in xrange(1,nrows):
			rowValues= table.row_values(i) #某一行数据
			if rowValues[6] in self.many_name:
				name.append(rowValues)
		return name

		
	#获取有相同名字的列表
	def get_name(self):
		name=[]
		alldate=[]
		data = xlrd.open_workbook(path1)
		table = data.sheets()[0]
		nrows = table.nrows #行数
		ncols = table.ncols #列
		for i in xrange(1,nrows):
			rowValues= table.row_values(i) #某一行数据
			alldate.append(rowValues)
			name.append(rowValues[6])
		return name,alldate


	#抓取无相同号码信息并保存
	def tset_req(self):
		while True:
			lock.acquire()
			if len(self.set_name)==0:
				lock.release()
				break
			else:
				po=self.set_name.pop(0)
				lock.release()
				tels=[]
				for i in xrange(5):
					try:
						req1=requests.get('https://114.mingluji.com/minglu/%s_%s'%(po,i),headers=headers)
					except Exception as e:
						# time.sleep(1)#访问保存休息一秒重新访问一次
						req1=requests.get('https://114.mingluji.com/minglu/%s_%s'%(po,i),headers=headers)					
					if req1.status_code!=200:
						break
					else:
						tel1=re.findall(r"<span itemprop='telephone'>(.*?)</span>",req1.content.decode('utf-8','ignore'))
						if len(tel1)!=0:	
							tels+=tel1	

				try:
					req=requests.get('https://114.mingluji.com/minglu/%s'%po,headers=headers).content.decode('utf-8','ignore')
				except Exception as e:
					# time.sleep(1)#访问保存休息一秒重新访问一次
					req=requests.get('https://114.mingluji.com/minglu/%s'%po,headers=headers).content.decode('utf-8','ignore')


				tel=re.findall(r"<span itemprop='telephone'>(.*?)</span>",req)
				if len(tel)==0:	
					tel=['']
				tels+=tel							
				for row in self.name_list[1]:
					if row[6]==po:
						s=['/'.join(tels)]
						row2=row+s
						lock.acquire()
						self.save(row2)
						# self.names.pop(row)
						lock.release()
			# print len(self.names)		
				

	#抓取相同号码信息并保存		
	def many_req(self):
		while True:
			lock.acquire()
			if len(self.many_name)==0:
				lock.release()
				break
			else:
				po=self.many_name.pop(0)
				lock.release()
				for i in range(20):
					req1=requests.get('https://114.mingluji.com/minglu/%s_%s'%(po,i),headers=headers)
					if req1.status_code!=200:
						break
					else:
						content=req1.content.decode('utf-8','ignore')
						tel1=re.findall(r"<span itemprop='telephone'>(.*?)</span>",content)
						if len(tel1)!=0:	
							html=etree.HTML(content)
							sf=html.xpath(u"//span[@itemprop='addressRegion']//text()")
							href=html.xpath(u"//span[@itemprop='addressLocality']//text()")						
							for row in self.my_name:
								if row[6]==po :
									aa=row[5].split('/')
									if sf[0] in aa and href[0] in aa:
										row2=row+tel1
										lock.acquire()
										self.save(row2)
										lock.release()
										
	#保存信息					
	def save(self,date):
		with codecs.open(path2,'ab') as f:
			w= csv.writer(f)
			w.writerow(date)		
	
	#把相同名字中一条有多个号码存到一行，并把没有号码的信息存储
	def deel_file(self):
		dates=[]
		with codecs.open(path2,'r') as f:
			a=f.readlines()
			for row in self.my_name:	
				for i in a:
					lit=i.split(',')
					if lit[5] in row and lit[6] in row:
						row.append(lit[12])
				dates.append(row)					
		with codecs.open(path2,'wb') as f:
			w= csv.writer(f)
			w.writerow(['dbname','dbname1','UID','RecordID','LayerID','行政区','Name','AliasName','FolkName','SearchName','TelNumber','Address','Tel'])
			for a in dates:
				if len(a)>13:
					a[12]=a[12]+'/'+a[13]
					if len(a)>14:
						a[12]=a[12]+'/'+a[14]
						if len(a)>15:
							a[12]=a[12]+'/'+a[15]
					a=a[0:13]		
				w.writerow(a)

def thread2():
	with Loc:	
		da=Pov114()
		tasks = [] #任务列表
		for x in range(20):
			# t1 = threading.Thread(target=da.many_req)	
			t= threading.Thread(target=da.tset_req) #准备线程函数及参数
			t.setDaemon(True) #设置守护线程（主线程退出，子线程也会退出，不会挂起占用资源）
			tasks.append(t)
		for t in tasks:
			t.start() #启动多线程（任务列表有多少个值，就会启动多少个线程）
		for t in tasks:
			t.join()

def pool2():
	pool = multiprocessing.Pool(processes = 4)
	pool.apply_async(thread2)
	pool.close()
	pool.join()	



if __name__ == '__main__':
	thread3()
	pool2()
