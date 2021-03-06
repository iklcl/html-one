#-*- coding:utf-8 -*-
#网址：http://www.ccgp-hainan.gov.cn/
#文件名：ccgp_hainan.py
#作者: huanghong
#创建日期: 2017-011-27
#功能描述: 海南省政府采购网
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
		data={
		'currentPage':str(t),
		'begindate':'',
		'enddate':'',
		'title':'地图',
		'bid_type':'',
		'proj_number':'',
		'zone':''
		}
		req=requests.post('http://www.ccgp-hainan.gov.cn/cgw/cgw_list.jsp',headers=headers,data=data).content
		soup=BeautifulSoup(req,'lxml')
		div=soup.find_all('div',class_='nei02_04_01')[0]
		ul=div.find_all('ul')[0]
		li=ul.find_all('li')
		if len(li)==0:
			break
		for i in li:
			ti=i.find_all('i')[0].text.replace(' ','')
			datime=datetime.datetime.strptime(str(ti),'%Y-%m-%d')
			nowtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
			ntime=datetime.datetime.strptime(nowtime,'%Y-%m-%d')
			if abs((ntime-datime).days)<=nd:
				# print abs((ntime-datime).days)	
				em=i.find_all('em')[0].find_all('a')[0]
				title=em.text
				link='http://www.ccgp-hainan.gov.cn'+em.get('href')
				datas.append({'url':link,'title':title,'updatetime':datime})
	return datas



class Crawler():
	def __init__(self):
		self.url = 'http://www.ccgp-hainan.gov.cn/'
		self.mongo=Saving()
		
	def __call__(self,nd=0):
		self.nd=nd
		try:
			updatelist=get_link(self.nd)
		except Exception as e:
			logging.error(e)
		self.mongo.save(self.url,updatelist)	
		logging.info(u'海南省政府采购网,更新:(%s)'%len(updatelist))
		return True


def main():
	test = Crawler()
	result =test(90)	
	logging.info(result)
if __name__ == '__main__':
	main()	
