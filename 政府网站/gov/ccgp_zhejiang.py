#-*- coding:utf-8 -*-
#网址：http://www.ccgp-zhejiang.gov.cn/
#文件名：ccgp_zhejiang.py
#作者: huanghong
#创建日期: 2017-12-01
#功能描述: 浙江政府采购网
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
import json
reload(sys)
sys.setdefaultencoding('utf-8')
headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
}
def get_link(nd):
	datas=[]
	t=0
	while True:
		t+=1
		params={
		'pageSize':'15',
		'pageNo':t,
		'url':'http://notice.zcy.gov.cn/new/noticeSearch',
		'keyword':'地图',
		'noticeType':'0'
		}
		# print t
		req=requests.get('http://manager.zjzfcg.gov.cn/cms/api/cors/getRemoteResults?',headers=headers,params=params).content
		lis = re.findall('(\[.*\])',req)[0]#.replace('[','').replace(']','').split(',')
		jd = json.loads(lis)
		if len(jd)==0:
			break
		
		for i in jd:
			
			ti=time.strftime('%Y-%m-%d',time.localtime(int(i['pubDate'])/1000))
			

			datime=datetime.datetime.strptime(str(ti),'%Y-%m-%d')
			nowtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
			ntime=datetime.datetime.strptime(nowtime,'%Y-%m-%d')
			if abs((ntime-datime).days)<=nd:
				# print abs((ntime-datime).days)
				title=i['title']
				link=i['url']
				datas.append({'url':link,'title':title,'updatetime':datime})		
	return datas
		



class Crawler():
	def __init__(self):
		self.url = 'http://www.ccgp-zhejiang.gov.cn/'
		self.mongo=Saving()
		
	def __call__(self,nd=0):
		self.nd=nd								
		try:
			updatelists=get_link(self.nd)
		except Exception as e:
			logging.error(e)
		# print updatelists
		self.mongo.save(self.url,updatelists)
		logging.info(u'浙江政府采购网,更新:(%s)'%len(updatelists))
		return True
def main():
	test = Crawler()
	result =test(20)	
	logging.info(result)
if __name__ == '__main__':
	main()
