#-*- coding:utf-8 -*-
#网址：http://www.ccgp-neimenggu.gov.cn/
#文件名：ccgp_neimenggu.py
#作者: huanghong
#创建日期: 2017-12-01
#功能描述: 内蒙古政府采购网
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
	for t in xrange(1,5):
		params={
			'r':'zfcgw/anndata',
			'type_name':'1',
			'keyword':'地图',
			'byf_page':t,
			'fun':'cggg'
			# _:1512273216732
		}
		# print t
		req=requests.get('http://www.nmgp.gov.cn/zfcgwslave/web/index.php?',headers=headers,params=params).content
		# print req
		lis = re.findall('(\[.*\])',req)
		# print lis	
		jd = json.loads(lis[0])[0]
		for i in jd:
			# print i['ENDDATE'],i['TITLE_ALL'],i['ay_table_tag'],i['wp_mark_id']
			ti=re.findall('(\d+-\d+-\d+)',i['ENDDATE'])[0]
			# print ti
			datime=datetime.datetime.strptime(str(ti),'%Y-%m-%d')
			nowtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
		
			ntime=datetime.datetime.strptime(nowtime,'%Y-%m-%d')
			if abs((ntime-datime).days)<=nd:
				# print abs((ntime-datime).days)
				title=i['TITLE_ALL']
				link='http://www.nmgp.gov.cn/ay_post/post.php?tb_id=%s&p_id=%s'%(i['ay_table_tag'],i['wp_mark_id'])
				datas.append({'url':link,'title':title,'updatetime':datime})
			
	return datas
		



class Crawler():
	def __init__(self):
		self.url = 'http://www.ccgp-neimenggu.gov.cn/'
		self.mongo=Saving()
		
	def __call__(self,nd=0):
		self.nd=nd								
		try:
			updatelists=get_link(self.nd)
		except Exception as e:
			logging.error(e)
		
		self.mongo.save(self.url,updatelists)
		logging.info(u'内蒙古政府采购网,更新:(%s)'%len(updatelists))
		return True
def main():
	test = Crawler()
	result =test(50)	
	logging.info(result)
if __name__ == '__main__':
	main()	
