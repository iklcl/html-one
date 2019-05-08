#-*- coding:utf-8 -*-
#网址：http://www.ccgp-shaanxi.gov.cn/
#文件名：ccgp_shanxi.py
#作者: huanghong
#创建日期: 2017-011-28
#功能描述: 陕西省政府采购网
#完成状况：完成
import logging
from ccgp.Auxiliary import Saving
import time,datetime
import requests
from pymongo import MongoClient
from bson.binary import Binary
import sys
import codecs,csv
from bs4 import BeautifulSoup
import re
import urllib
reload(sys)
sys.setdefaultencoding('utf-8')

se = requests.session()
headers2={
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Cookie':'JSESSIONID=C35ABC90E9C4DFC2A6C80D9AE555A528',
	'Referer': 'http://www.ccgp-shaanxi.gov.cn/',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
}
headers={

	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',

'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
}

def get_link(nd,keyword):
	dates=[]
	datas1={
	'radiobutton':urllib.unquote('%D5%D0%B1%EA'),
	'sm.keyType':'sm.keyType',
	'prefern':keyword.encode('utf-8').decode('utf-8-sig').encode('gbk')
	}
	datas2={
		'radiobutton':urllib.unquote('%D6%D0%B1%EA'),
		'sm.keyType':'sm.keyType',
		'prefern':keyword.encode('utf-8').decode('utf-8-sig').encode('gbk')
	}
	for dat in 	[datas1,datas2]:
		w=se.post('http://www.ccgp-shaanxi.gov.cn/PreferenSearchAction',headers=headers2,data=dat)	
		t=0
		bia=[1]
		while True:
			t+=1
			params={
			'pages':str(t)
			}
			req=se.get('http://www.ccgp-shaanxi.gov.cn/perfern_result.jsp',headers=headers,params=params).content.decode('gbk')
			soup=BeautifulSoup(req,'lxml')
			table=soup.find_all('table',height="390")[0]
			tr=table.find_all('tr')
			if bia[-1]==tr[0]:
				break
			# print len(tr)	
			bia.append(tr[0])
			for i in range(len(tr)-1):
				ti=tr[i].find_all('td',width="16%")[0].text.replace('[','').replace(']','')
				datime=datetime.datetime.strptime(str(ti),'%Y-%m-%d')
				nowtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
				ntime=datetime.datetime.strptime(nowtime,'%Y-%m-%d')
				if abs((ntime-datime).days)<=nd:
					# print abs((ntime-datime).days)	
					em=tr[i].find_all('td',width="90%")[0].find_all('a')[0]
					title=em.text.replace(' ','').replace('\r','').replace('\n','')
					link='http://www.ccgp-shaanxi.gov.cn/'+em.get('href')
					dates.append({'url':link,'title':title,'updatetime':datime,'unopenable':'YES'})
				else:
					return dates

class Crawler():
	def __init__(self):
		self.url = 'http://www.ccgp-shaanxi.gov.cn/'
		self.mongo=Saving()
	
	def __call__(self,nd,keyword):
		self.nd=nd
		self.keyword=keyword		
		try:
			updatelists=get_link(self.nd,self.keyword)		
		except Exception as e:
			logging.error(e)
		# print len(updatelists)	
		self.mongo.save(self.url,updatelists)
		logging.info(u'陕西省政府采购网,更新:(%s)'%len(updatelists))
		return True
def main():
	test = Crawler()
	result =test(60,u'地图')	
	logging.info(result)
if __name__ == '__main__':
	main()


	
