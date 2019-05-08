##-*- coding:utf-8 -*-

import requests
import re
import json
import codecs,csv
import time	
from bs4 import BeautifulSoup
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
	"Host":"www.a-hospital.com",
	"Upgrade-Insecure-Requests":"1",
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
}


def get_href():
		url = 'http://www.a-hospital.com/w/%E5%85%A8%E5%9B%BD%E5%8C%BB%E9%99%A2%E5%88%97%E8%A1%A8'

		res = requests.get(url,headers=headers)
		html=res.content
		pages = etree.HTML(html.decode('utf-8'))
		a = pages.xpath(u'//div[@id="bodyContent"]/p/b/a/@href')
		return a
def get_data(href):
		url= 'http://www.a-hospital.com'+href
		# return url
		d=[]
		htmlllll=requests.get(url,headers=headers)
		html=htmlllll.content
		pages = etree.HTML(html.decode('utf-8'))
		a = pages.xpath(u'//div[@id="bodyContent"]/ul/li/b/a/text()')
		soup=BeautifulSoup(html,'lxml')
		div=soup.select('div[id=bodyContent]')[0]
		ul=div.find_all('ul')[0]
		ul=ul.find_all('ul')
		
		for i in ul:
			v=[]
			li=i.find_all('li')
			for i in li:
			# 	print i
				t=i.text
				v.append(t)

			d.append(v)	
		d.append(a)	
		return d,a	
			
		
			
		
		
		# pages = etree.HTML(html.decode('utf-8'))
		# a = pages.xpath(u'//div[@id="bodyContent"]/ul/li/b/a/text()|//div[@id="bodyContent"]/ul/li/b/a/text()|//div[@id="bodyContent"]/ul/li/ul/li/text()|//div[@id="bodyContent"]/ul/li/ul/li/a/text()')

		# b=pages.xpath('//div[@id="bodyContent"]/ul/li/ul/li')
		# for i in b:
		# 	Name=i.xpath(u'//b/text()')
		#     print Name       
		# 	# 	d.append(i)
		# 	return	Name
		# c=pages.xpath(u'//div[@id="bodyContent"]/ul/li/ul/li/b/text()')
		# c=pages.xpath(u'//div[@id="bodyContent"]/ul/li/b/a/text()|//div[@id="bodyContent"]/ul/li/ul/li/text()|//div[@id="bodyContent"]/ul/li/ul/li/a/text()')

		# for i in a:
		# 	i=i.strip('：')
		# # 	print i
		# 	d.append(i)
		# return d		
		
	
def main():
	href=get_href()
	for i in href[:1]:
		# print i
		data,name=get_data(i)
		for i in name:
			print i
		# # 	i=i.replace(',',';')
			i=i.replace('\n',',')
			i=i.strip(',')
			c=i.split(',')
			dic={}
			for a in c:
				a=[a]
			d={item.split('：')[0]:item.split('：')[1] for item in i}
				
			print d
			
			
				hop_dz=i['医院地址']
				hop_cz=i['传真号码']
				hop_yx=i['电子邮箱']
				hop_dj=i['医院等级']
			for x in ['传真号码','电子邮箱','医院地址','重点科室' ,'医院网站','经营方式','医院等级','联系电话']:
				d.setdefault(x, None)
			for key,value in d.items():
				print key,value	


			

if __name__ == '__main__':
	main()