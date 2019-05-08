#-*- coding:utf-8 -*-
#网址：http://www.ccgp-xizang.gov.cn/
#文件名：ccgp_xizang.py
#作者: huanghong
#创建日期: 2017-011-30
#功能描述: 西藏政府采购网
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
import re,json

reload(sys)
sys.setdefaultencoding('utf-8')
headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
}
def get_link(nd,keyword):
	datas=[]
	word=json.dumps(keyword).strip('"')
	t=0
	while True:
		t+=1
		data={
		'categoryId':'0',
		'keyWord':keyword,
		'pager.keyword':word,
		'pager.pageNumber':t
		}
		req=requests.post('http://www.ccgp-xizang.gov.cn/front/cmsArticle/searchArticle.action',headers=headers,data=data).content
		soup=BeautifulSoup(req,'lxml')
		div=soup.find_all('div',id='list_search')[0]
		ul=div.find_all('ul')[0]
		li=ul.find_all('li')
		if len(li)==0:
			break

		for i in li:
			tis=i.find_all('div')[0]
			ti=re.findall('(\d+-\d+-\d+)',tis.text)[0]		
			datime=datetime.datetime.strptime(str(ti),'%Y-%m-%d')
			nowtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
			ntime=datetime.datetime.strptime(nowtime,'%Y-%m-%d')
			if abs((ntime-datime).days)<=nd:
				# print abs((ntime-datime).days)
				em=tis.find_all('a')[0]
				title=em.text.replace(' ','')
				link='http://www.ccgp-xizang.gov.cn'+em.get('href')
				datas.append({'url':link,'title':title,'updatetime':datime})
	return datas

class Crawler():
	def __init__(self):
		self.url = 'http://www.ccgp-xizang.gov.cn/'
		self.mongo=Saving()	
	def __call__(self,nd,keyword):
		self.keyword=keyword
		self.nd=nd
		try:
			updatelist=get_link(self.nd,self.keyword)
		except Exception as e:
			logging.error(e)
		self.mongo.save(self.url,updatelist)
		logging.info(u'西藏政府采购网,更新:(%s)'%len(updatelist))
		return True
def main():
	test = Crawler()
	result =test(10,u'地图')	
	logging.info(result)
if __name__ == '__main__':
	main()	
