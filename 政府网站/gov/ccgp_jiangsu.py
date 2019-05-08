#-*- coding:utf-8 -*-
#网址：http://www.ccgp-jiangsu.gov.cn
#文件名：ccgp_jiangsu.py
#作者: huanghong
#创建日期: 2017-12-01
#功能描述: 江苏政府采购网
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
headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
}
def get_link(nd):
	datas=[]
	t=0
	while True:
		t+=1
		params={
		'page':t,
		'channelid':'204408',
		'searchword':'地图',
		'keyword':'地图',
		'orderby':'-DocrelTime',
		'was_custom_expr':'doctitle=(地图)',
		'perpage':'10',
		'outlinepage':'10',
		'searchscope':'doctitle',
		'timescope':'',
		'timescopecolumn':'',
		'orderby':'-DocrelTime',
		'andsen':'',
		'total':'',
		'orsen':'',
		'exclude':''
		}
		
		req=requests.get('http://www.ccgp-jiangsu.gov.cn/was5/web/search?',headers=headers,params=params).content
		soup=BeautifulSoup(req,'lxml')
		ul=soup.find_all('ol',style="width:820px;")[0]
		li=ul.find_all('li')
		if len(li)==0:
			break
		for i in li:
			tis=i.find_all('div',class_="pubtime")[0]
			ti=re.findall('(\d+.\d+.\d+)',tis.text)[0].replace('.','-')		
			datime=datetime.datetime.strptime(str(ti),'%Y-%m-%d')
			nowtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
		
			ntime=datetime.datetime.strptime(nowtime,'%Y-%m-%d')
			if abs((ntime-datime).days)<=nd:
				# print abs((ntime-datime).days)	
				em=i.find_all('a')[0]
				title=em.text.replace(' ','')
				link=em.get('href')
				datas.append({'url':link,'title':title,'updatetime':datime})
	return datas
		



class Crawler():
	def __init__(self):
		self.url = 'http://www.ccgp-jiangsu.gov.cn'
		self.mongo=Saving()
		
	def __call__(self,nd=0):
		self.nd=nd							
		try:
			updatelists=get_link(self.nd)
		except Exception as e:
			logging.error(e)
		# print len(updatelists)
		self.mongo.save(self.url,updatelists)
		logging.info(u'江苏政府采购网,更新:(%s)'%len(updatelists))
		return True
def main():
	test = Crawler()
	result =test(60)	
	logging.info(result)
if __name__ == '__main__':
	main()	
