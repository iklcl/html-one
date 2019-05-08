#coding=utf-8
import requests
from lxml import etree
import sys
import codecs,csv
from bs4 import BeautifulSoup
import urllib
import urllib2
import re

reload(sys)
sys.setdefaultencoding('utf-8')


headers={
		"Host":"www.tzgsj.gov.cn",
		"Referer":"http://www.tzgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=95000000&total=20806&queryType=1&pagenum=3&action=pagin&findWenhao=&findName=",
		"Upgrade-Insecure-Requests":"1",
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
		}
def get_page():
	r=requests.get('http://www.xzgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=95000000&queryType=6',headers=headers)
	# print r.content
	html=r.content
	soup=BeautifulSoup(html,'lxml')
	table=soup.select('table[width=90%]')[0]
	td=table.select('td[align=right]')[0].text
	page=re.findall(u'共(\d*)页',td)

	return page#总页数
def get_href(page):
	
	for  i in range(1,int(page)+1):
		b=[]
		url="http://www.tzgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=95000000&total=20806&queryType=1&pagenum="
		data="&action=gg.jsp?ssid=Z1G9SxxTkHjqWVSln1T01QRpjQ37RybJ3xyZZ01kH333kYCHtTWl!-1381989637!1500857981906&findWenhao=&findName=#	"
		
		# 定义url，传入数据


		r=requests.get(url+str(i)+data,headers=headers)
		html = r.content
		# print html
		pages = etree.HTML(html.lower().decode('utf-8'))
		a = pages.xpath(u"//table[@width='700']/tr[position()>1]/td/text()|//table[@width='700']/tr[position("
		                              u")>1]/td/a/text()")

		for i in range(0, len(a),3):
			b.append(a[i:i+3])		
		c=tuple(b)

		print c
		  	# 改为元组
			
		with codecs.open(u'常州.csv','ab') as f:
			w = csv.writer(f)
			for row in c:		
				w.writerow(row)