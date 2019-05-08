#-*- coding:utf-8 -*-
#网址：http://www.ccgp-qinghai.gov.cn/
#文件名：ccgp_qinghai.py
#作者: huanghong
#创建日期: 2017-011-29
#功能描述: 青海省政府采购网
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

reload(sys)
sys.setdefaultencoding('utf-8')

se = requests.session()
headers2={
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Cookie':'JSESSIONID=C35ABC90E9C4DFC2A6C80D9AE555A528',
	'Referer': 'http://www.ccgp-qinghai.gov.cn/',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
}
headers={
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
}

def get_link(nd):
	dat=[]
	t=0
	while True:
		datas={
		'op':'more',
		'keyWord':'地图',
		'pageNo':t
		}
		req=se.post('http://www.ccgp-qinghai.gov.cn/searchContentController.form?',headers=headers,data=datas).content
		t+=1
		soup=BeautifulSoup(req,'lxml')
		div=soup.find_all('div',class_='m_list_3')[0]
		ul=div.find_all('ul')[0]
		li=ul.find_all('li')
		if len(li)==0:
			break
		for i in li:
			ti=i.find_all('div',class_='news_date')[0].text.replace(u'年','-').replace(u'月','-').replace(u'日','')
			# print ti
			datime=datetime.datetime.strptime(str(ti),'%Y-%m-%d')
			nowtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
			ntime=datetime.datetime.strptime(nowtime,'%Y-%m-%d')
			if abs((ntime-datime).days)<=nd:
				# print abs((ntime-datime).days)
				em=i.find_all('div',class_='news_list')[0].find_all('a')[0]
				title=em.text
				link='http://www.ccgp-qinghai.gov.cn/'+em.get('href')	
				dat.append({'url':link,'title':title,'updatetime':datime})
	return dat

class Crawler():
	def __init__(self):
		self.url = 'http://www.ccgp-qinghai.gov.cn/'
		self.mongo=Saving()
		
	def __call__(self,nd=0):
		self.nd=nd
		try:
			updatelist=get_link(self.nd)
		except Exception as e:
			logging.error(e)
		self.mongo.save(self.url,updatelist)
		logging.info(u'青海省政府采购网,更新:(%s)'%len(updatelist)) 
		return True
def main():
	test = Crawler()
	result =test()	
	logging.info(result)
if __name__ == '__main__':
	main()
	
