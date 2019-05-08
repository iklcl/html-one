#-*- coding:utf-8 -*-
#网址：http://www.ccgp-sichuan.gov.cn
#文件名：ccgp_sichuan.py
#作者: huanghong
#创建日期: 2017-12-01
#功能描述: 四川政府采购网
#完成状况：完成
import logging
# from ccgp.Auxiliary import Saving
import time,datetime
import requests
# from pymongo import MongoClient
# from bson.binary import Binaryb
import sys
import codecs,csv
from bs4 import BeautifulSoup
import re,json

reload(sys)
sys.setdefaultencoding('utf-8')
headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
}
def get_link(year,nd,keyword):
	datas=[]
	word=json.dumps(keyword).strip('"')
	t=0
	while True:
		t+=1
		params={
		'method':'search',
		'years':year,
		'chnlCodes':'',
		'city':'',
		'town':'',
		'cityText':'',
		'townText':'',
		'searchKey':word,
		'distin':'',
		'type':'',
		'title':'',
		'beginDate':'',
		'endDate':'',
		'str1':'',
		'str2':'',
		'pageSize':'10',
		'curPage':t,
		'searchResultForm':'search_result_anhui.ftl'
		}
		# print year
		req=requests.get('http://www.ccgp-sichuan.gov.cn/CmsNewsController.do',headers=headers,params=params).content
		soup=BeautifulSoup(req,'lxml')
		div=soup.find_all('div',class_='colsList')[0]
		ul=div.find_all('ul')[0]
		li=ul.find_all('li')
		if len(li)==0:
			break
		# print len(li)	
		for i in li:
			ti=i.find_all('span',class_="date")[0].text		
			datime=datetime.datetime.strptime(str(ti),'%Y-%m-%d')
			nowtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
			ntime=datetime.datetime.strptime(nowtime,'%Y-%m-%d')
			if abs((ntime-datime).days)<=nd:
				# print abs((ntime-datime).days)	
				em=i.find_all('a')[0]
				title=em.text.replace(' ','')
				link='http://www.ccgp-sichuan.gov.cn'+em.get('href')
				datas.append({'url':link,'title':title,'updatetime':datime})
			else:
				return datas
		



class Crawler():
	def __init__(self):
		self.url = 'http://www.ccgp-sichuan.gov.cn'
		self.mongo=Saving()
		
	def __call__(self,nd,keyword):
		self.nd=nd
		self.keyword=keyword
		updatelists=[]
		for self.ear in xrange(2019,2012):							
			try:
				updatelist=get_link(self.ear,self.nd,self.keyword)
				updatelists+=updatelist
			except Exception as e:
				logging.error(e)
		# print len(updatelists)
		self.mongo.save(self.url,updatelists)
		logging.info(u'四川政府采购网,更新:(%s)'%len(updatelists))
		return True
def main():
	test = Crawler()
	result =test(5,u'智慧')	
	logging.info(result)
if __name__ == '__main__':
	logging.info('dsdsd')
