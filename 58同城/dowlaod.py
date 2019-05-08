#coding=utf-8

#文件名称：dowload.py
#作者：huanghong
#创建日期：2018-4-10
#功能描述：58网上海房源图片下载
#网页地址：http://cd.58.com/xiaoqu/
#处理进度：已完成（待优化）
import requests,random,time,json
import urllib
from lxml import etree
import sys
import codecs,csv
import re
import os.path
import sqlite3
import MySQLdb 
from datetime import datetime
import threading
from multiprocessing import Pool,Lock,Process
import multiprocessing
reload(sys)
sys.setdefaultencoding('utf-8')



lock = threading.Lock()
Loc = Lock()
new_path=os.path.join(sys.path[0],'data')
if not os.path.isdir(new_path):
	os.makedirs(new_path)
path1=unicode(os.path.join(sys.path[0],'58上海.csv'),'utf-8')
path2=unicode(os.path.join(sys.path[0],'58上海3.csv'),'utf-8')
path4=unicode(os.path.join(sys.path[0],'58上海5.csv'),'utf-8')
def read_path3():
	data=[]
	t=0
	with codecs.open(path2,'r') as f:
		reads = csv.reader(f)
		for i in reads:	
			data.append([i[0].decode('utf-8'),i[1].decode('utf-8'),i[2].decode('utf-8'),i[3].decode('utf-8'),i[4].decode('utf-8'),i[5].decode('utf-8')])
	return data	


#下载图片并存储
def dowload(link):
	link_list=[]
	url='http://m.58.com/xiaoquweb/getXiaoquPics/?callback=jQuery112407269697319778079_1522727385080&infoid=%s&_=1522727385081'%(link[5])
	req=requests.get(url).content
	print url
	text=re.findall('"data":(\{.*?\}),"flag"',req)[0]
	cont=json.loads(text)
	t=0
	name=link[0]
	new_path_data=os.path.join(new_path,name)
	if not os.path.isdir(new_path_data):
		os.makedirs(new_path_data)	
	try:
		picture1=cont["huxingtu"]
		for lin in picture1:
			t+=1
			with codecs.open(path4,'ab') as f:
				w = csv.writer(f)
				w.writerow([name,t,lin['picurl']])
	except KeyError:
		pass
	try:
		picture2=cont["shijingtu"]
		for lin in picture2:
			t+=1
			with codecs.open(path4,'ab') as f:
				w = csv.writer(f)
				w.writerow([name,t,lin['picurl']])
	except KeyError:
		pass	
	number=t
	print u'图片数量%s'%number
	data=[link[0],link[1],link[2],link[3],number,link[4]]
	with codecs.open(path1,'ab') as f:
		w = csv.writer(f)
		w.writerow(data)


class Dowload_pic():
	def __init__(self):
		self.data=[]
		with codecs.open(path4,'r') as f:
			reads = csv.reader(f)
			# print dir(read)
			for i in reads:
				self.data.append([i[0].decode('utf-8'),i[1].decode('utf-8'),i[2].decode('utf-8')])

	def dowload_pic(self):
		while True:
			lock.acquire()
			if len(self.data)==0:
				lock.release()
				break
			else:
				url=self.data.pop(0)
				print len(self.data)
				lock.release()
				new_path_data=os.path.join(new_path,url[0])
				if not os.path.isdir(new_path_data):
					os.makedirs(new_path_data)
				try:
					urllib.urlretrieve(url[2],os.path.join(new_path_data,"%s%s.%s"%(url[0],url[1],'jpg')))
				except Exception as e:
					urllib.urlretrieve(url[2],os.path.join(new_path_data,"%s%s.%s"%(url[0],url[1],'jpg')))
				except Exception as e:
					pass	
			
def thread2():
	with Loc:	
		da=Dowload_pic()
		tasks = [] 
		for x in range(20):
			t= threading.Thread(target=da.dowload_pic) 
			t.setDaemon(True) 
			tasks.append(t)
		for t in tasks:
			t.start() 
		for t in tasks:
			t.join()

def pool2():
	pool = multiprocessing.Pool(processes = 4)
	pool.apply_async(thread2)
	pool.close()
	pool.join()	
	os.remove(path4)


def main():
	if not os.path.isdir(path1):
		with codecs.open(path1,'wb') as f:
			w = csv.writer(f)
			w.writerow([u'name',u'adress','lat','lng','number','url'])
	data=read_path3()
	for i in data:
		dowload(i)
	os.remove(path2)	
if __name__ == '__main__':
	main()
	pool2()