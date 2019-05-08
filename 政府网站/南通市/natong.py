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


for  i in range(1,1518):
	b=[]
	url="http://www.ntgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=95000000&total=30331&queryType=6&pagenum="
	data="&action=gg.jsp?ssid=Z1KKyHjq59S5pnKD1vdLh48RQPpTJLTBXYQCny3ZLkcDs2NgSpFq!-2093807738!1500858954984&findWenhao=&findName="
	headers={
	"Host":"www.ntgsj.gov.cn",
	"Referer":"http://www.ntgsj.gov.cn/baweb/show/shiju/gg.jsp?ssid=Znl93nfL4J2MZ3lb9DhKjnQjcvn4zBFyVC7JrgfpNmyRJGCjjjlH!-1178932438!1500423677625&fenceid=95000000&queryType=6",
	"Upgrade-Insecure-Requests":"1",
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"

	}
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
			
	with codecs.open(u'南通市.csv','ab') as f:
		w = csv.writer(f)
		for row in c:		
			w.writerow(row)
