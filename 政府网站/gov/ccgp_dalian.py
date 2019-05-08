#-*- coding:utf-8 -*-
#网址：http://www.ccgp-dalian.gov.cn
#文件名：ccgp_dalian.py
#作者: huanghong
#创建日期: 2017-12-05
#功能描述: 大连政府采购网
#完成状况：完成
import logging
from ccgp.Auxiliary import Saving
import time,datetime
# import requests
from pymongo import MongoClient
from bson.binary import Binary
import sys
import codecs,csv
from bs4 import BeautifulSoup
import re
import urllib
from requests import Request, Session
reload(sys)
sys.setdefaultencoding('utf-8')

headers={
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.9',
	'Cache-Control':'max-age=0',
	'Connection':'keep-alive',
	'Cookie':'yunsuo_session_verify=c280372dadcf36e45342a1f1e828d79b; ASP.NET_SessionId=hlmyqmyknzygwmymdbam3k45',
	'Host':'www.ccgp-dalian.gov.cn',
	'Referer':'http://www.ccgp-dalian.gov.cn/dlweb/Template/Default/pagehead.htm',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
}
def get_link(nd):
		datas=[]
		s = Session()
		url="http://www.ccgp-dalian.gov.cn/dlweb/showinfo/searchresult.aspx?EpStr3=%u5730%u56FE&searchtype=title"
		req = Request('GET', url)
		prepped = s.prepare_request(req)
		prepped.url = prepped.url.replace('%25', '%')
		resp = s.send(prepped)
		html=resp.content.decode('gb2312')
		
		soup=BeautifulSoup(html,'lxml')
		table=soup.find_all('table',id="SearchResult2_DataGrid1")[0]
		tr=table.find_all('tr',valign="top")
		# if len(tr)==0:
		# 	break
		for i in tr:
			tis=i.find_all('td',align="right")[0]
			ti=re.findall('(\d+.\d+.\d+)',tis.text)[0].replace('.','-')	
				
			datime=datetime.datetime.strptime(str(ti),'%Y-%m-%d')
			nowtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
			ntime=datetime.datetime.strptime(nowtime,'%Y-%m-%d')
			if abs((ntime-datime).days)<=nd:
				# print abs((ntime-datime).days)	
				em=i.find_all('a')[0]
				title=em.text.replace(' ','')
				link='http://www.ccgp-dalian.gov.cn'+em.get('href')
				datas.append({'url':link,'title':title,'updatetime':datime})
		return datas
		



class Crawler():
	def __init__(self):
		self.url = 'http://www.ccgp-dalian.gov.cn'
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
	result =test(0)	
	logging.info(result)
if __name__ == '__main__':
	main()	
