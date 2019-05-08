#coding=utf-8
#文件名称：xuzhou.py
#作者：huanghong
#创建日期：2017-8-3
#功能描述：徐州市新设立企业公告
#网页地址：http://www.xzgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=95000000&queryType=6
#处理进度：已完成（待优化）

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
	"Referer":"http://www.tzgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=95000000&total=20622&queryType=6&pagenum=3&action=pagin&findWenhao=&findName=",
	"Upgrade-Insecure-Requests":"1",
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
	}

def get_page():
	r=requests.get('http://www.tzgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=95000000&queryType=6',headers=headers)
	# print r.content
	html=r.content
	soup=BeautifulSoup(html,'lxml')
	table=soup.select('table[width=90%]')[0]
	td=table.select('td[align=right]')[0].text
	page=re.findall(u'共(\d*)页',td)

	return page#总页数
def get_data(page):	
	for  i in range(1,int(page)+1):
		b=[]
		url="http://www.tzgsj.gov.cn/baweb/show/shiju/gg.jsp?fenceid=95000000&total=20622&queryType=6&pagenum="
		data="&action=gg.jsp?ssid=Z1N0nkQx367gN16CqxGZ1ZGm5mGGhvQS5FQLtJC4CWT19LJH4ZX4!-1381989637!1500876276125&findWenhao=&findName="
		
		# 定义url，传入数据


		r=requests.get(url+str(i)+data,headers=headers)
		html = r.content
		# print html
		pages = etree.HTML(html.decode('utf-8'))
		a = pages.xpath(u"//table[@width='700']/tr[position("u")>1]/td/a/@onclick")
		for i in a:
			a=i.replace('javaScript:window.open(\'','').replace('\',\'a\',\'width=550 height=350\')','')
			
		



			url='http://www.tzgsj.gov.cn/baweb/show/shiju/'+a
			# print url
			r=requests.get(url,headers=headers)
			html = r.content
			pages = etree.HTML(html.lower().decode('utf-8'))
			a = pages.xpath(u"//table[@width='427']/tr/td[position()>1]/input/@value")
			b=[]
			for i in range(0, len(a),6):
				b.append(a[i:i+6])		
			c=tuple(b)

			print c

			
		# with codecs.open(u'泰州.csv','ab') as f:
		# 	w = csv.writer(f)
		# 	for row in c:		
		# 		w.writerow(row)

def main():
	with codecs.open(u'泰州.csv','wb') as f:
			f.write(codecs.BOM_UTF8)
			w = csv.writer(f)
			w.writerow([u'企业名称',u'地址',u'企业类型/经济性质'])
	pages=get_page()
	for i in pages:
		data=get_data(i)







if __name__ == '__main__':
	main()
		
