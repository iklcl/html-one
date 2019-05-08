#coding=utf-8

#文件名称：spider.py
#作者：huanghong
#创建日期：2018-4-9
#功能描述：58网天津房源信息收集
#网页地址：http://wh.58.com/xiaoqu/
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
reload(sys)
sys.setdefaultencoding('utf-8')

new_path=os.path.join(sys.path[0],'data')
if not os.path.isdir(new_path):
	os.makedirs(new_path)

path1=unicode(os.path.join(sys.path[0],'58天津.csv'),'utf-8')
path2=unicode(os.path.join(sys.path[0],'58天津2.csv'),'utf-8')
path2=unicode(os.path.join(sys.path[0],'58天津3.csv'),'utf-8')
se = requests.session()


lock=threading.Lock()
ip_data=[]


USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
]

headers={
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	'Connection': 'keep-alive',
	'Cookie': 'userid360_xml=E1D6EE1AAB45A51797CB088E4F70C5D4; time_create=1526108508502; f=n; id58=mgjwFVrN2oUYlia8AwRwAg==; 58tj_uuid=1741cc44-cc18-4b3b-894d-66e60bf33cf8; als=0; __utmz=253535702.1523497496.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); commontopbar_myfeet_tooltip=end; 58home=sz; xxzl_deviceid=71kpsJWaXeBB52O5zudw8LbQI5xEzHL12u6yLGL86N2wz3XkDnTSsz2tW4A3hqeX; __utmc=253535702; duibiId=; commontopbar_ipcity=sz%7C%E6%B7%B1%E5%9C%B3%7C0; new_uv=11; utm_source=; spm=; init_refer=; __utma=253535702.958518258.1523497496.1523780901.1523839410.11; new_session=0; city=tj; Hm_lvt_ae019ebe194212c4486d09f377276a77=1523516508,1523840198; __utmt_pageTracker=1; commontopbar_new_city_info=18%7C%E5%A4%A9%E6%B4%A5%7C18; Hm_lpvt_ae019ebe194212c4486d09f377276a77=1523840208; __utmb=253535702.22.8.1523840285371',
	'Host': 'tj.58.com',
	'Referer': 'http://tj.58.com/xiaoqu/22/pn_11/?PGTID=0d011138-0001-2fcd-199b-2869076ae60b&ClickID=2',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent':random.sample(USER_AGENTS,1)[0]
		}
#拿到ip
def ip_sql():
	#存入数据库
	# 打开数据库连接
	db = MySQLdb.connect("192.168.201.91","root","123456","spidertools" )
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	# 创建数据表SQL语句
	sql="SELECT * FROM proxyippool where score>=0; "
	cursor.execute(sql)
   # 获取所有记录列表
	results = cursor.fetchall()
	for row in results:
		ip=row[0]+'://'+row[1]+':'+row[2]
		ip_data.append(ip)
	db.commit()	
	# 关闭数据库连接
	db.close()
	# print len(ip_data)

class Beijing58():
	citycodes=['22','21','20','19','23','6627','25','6630','6631','6632','6633','11354','27','26','5225','5526','8278','8279','8280','1905']


	def __init__(self):
		for i in self.citycodes:
			self.datas=[]
			self.shuliang=0
			self.data=self.get_link(i)
			print i,'============='




	# 获取个个小区的url
	def get_link(self,citycode,page=1,t=0):
		
		ip= random.sample(ip_data,1)[0]
		se.proxies = {'http': ip,'https': ip}
		while True:
			try:
				req=se.get('http://tj.58.com/xiaoqu/%s/pn_%s/?PGTID=0d011138-0001-2fcd-199b-2869076ae60b&ClickID=2'%(citycode,page),headers=headers,timeout=10)
				print req.status_code
				if req.status_code!=200:
					return self.get_link(citycode,page)
			except Exception as e:
				return self.get_link(citycode,page)		
			try:
				text=etree.HTML(req.content)
				name=text.xpath('//tr[@class=" "]/td[@class="info"]/ul')
			except AttributeError:
				return self.get_link(citycode,page)
			# print len(name)
			if page==1:
				print  page,'dsds'
				try:
					self.shuliang=re.findall(r'共&nbsp;<b class="filternum">(\d+)</b>&nbsp;条小区信息',req.content)[0]
				except Exception as e:
					y=self.get_link2(citycode,page+1)
					if y:
						return self.get_link(citycode,page)
					else:
						break	
			if t==5:
				break				
			page+=1
			if len(name)==0:
				if len(self.datas)<int(self.shuliang):
					t+=1
					return self.get_link(citycode,page,t)
				else:	
					break
					
			for i in name:
				name=i.xpath('./li[@class="tli1"]/a/text()')[0].replace('\r\n','').replace(' ','')
				link=i.xpath('./li[@class="tli1"]/a/@href')[0]
				adress=i.xpath('./li[@class="tli2"]/text()')[0]
				if name!='':
					data=[name,adress,link]
					with codecs.open(path1,'ab') as f:
						w = csv.writer(f)
						w.writerow(data)
					self.datas.append(data)
			print page,len(self.datas),self.shuliang

	def get_link2(self,citycode,page):	
		ip= random.sample(ip_data,1)[0]
		se.proxies = {'http': ip,'https': ip}
		try:
			req=se.get('http://wh.58.com/xiaoqu/%s/pn_%s/?PGTID=0d011138-0009-e99b-5b19-facc9acb7d26&ClickID=2'%(citycode,page),headers=headers,timeout=10)
			print req.status_code
			if req.status_code!=200:
				return self.get_link2(citycode,page)
		except Exception as e:
			return self.get_link2(citycode,page)		
		try:
			text=etree.HTML(req.content)
			name=text.xpath('//tr[@class=" "]/td[@class="info"]/ul')
		except AttributeError:
			return self.get_link2(citycode,page)
		# print len(name)
		shu=re.findall(r'共&nbsp;<b class="filternum">(\d+)</b>&nbsp;条小区信息',req.content)
		if len(shu)==0:
			return 
		else:
			self.shuliang=shu[0]	
			return 1









class Get_info():
	def __init__(self):
		self.data=[]
		with codecs.open(path1,'r') as f:
			reads = csv.reader(f)
			for i in reads:
				lit=[i[0].decode('utf-8'),i[1].decode('utf-8'),i[2].decode('utf-8')]
				if lit not in self.data:
					self.data.append(lit)



	#获取小区图片连接
	def get_infoid(self):
		while True:
			lock.acquire()
			if len(self.data)==0:
				lock.release()
				break
			else:
				url=self.data.pop(0)
				ip= random.sample(ip_data,1)[0]
				se.proxies = {'http': ip,'https': ip}
				lock.release()
				print url[2],len(self.data)
				try:
					req=se.get(url[2],headers=headers,timeout=10)
					if req.status_code!=200:	
						self.two_infoid(url)
						continue
					infoid=re.findall('infoid: "(.*?)",',req.content)[0]
				except Exception as e:
					
					self.two_infoid(url)
					continue	
				lat=re.findall('lat: "(.*?)",',req.content)[0]
				lon=re.findall('lon: "(.*?)",',req.content)[0]
				data=[url[0],url[1],lat,lon,url[2],infoid]
				with codecs.open(path2,'ab') as f:
					w = csv.writer(f)
					w.writerow(data)


	def two_infoid(self,url):
		ip= random.sample(ip_data,1)[0]
		se.proxies = {'http': ip,'https': ip}
		print url[2]
		try:
			req=se.get(url[2],headers=headers,timeout=10)
			if req.status_code!=200:
				
				return self.two_infoid(url)
			
		except Exception as e:
			
			return self.two_infoid(url)	
		try:
			infoid=re.findall('infoid: "(.*?)",',req.content)[0]	
			lat=re.findall('lat: "(.*?)",',req.content)[0]
			lon=re.findall('lon: "(.*?)",',req.content)[0]
		except Exception as e:
			return	
		data=[url[0],url[1],lat,lon,url[2],infoid]
		with codecs.open(path2,'ab') as f:
			w = csv.writer(f)
			w.writerow(data)



def thread2():
	ip_sql()
	info= Get_info()
	tasks = [] 
	for x in range(10):
		t= threading.Thread(target=info.get_infoid) 
		t.setDaemon(True) 
		tasks.append(t)
	for t in tasks:
		t.start() 
	for t in tasks:
		t.join()



# 
def main():
	# ip_sql()

	# da=Beijing58()

	thread2()
	# os.remove(path1)

if __name__ == '__main__':
	main()
