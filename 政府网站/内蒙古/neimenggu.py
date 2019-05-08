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


def get_href():
	b=[]
	
	for i in range(1,6):
		
		if i>4:
			url="http://www.nmgs.gov.cn/ggfb/qybggg/index.html"
		else:
			url="http://www.nmgs.gov.cn/ggfb/qybggg/index_"+str(i)+".html"
		r=requests.get(url)
		html = r.content
		# soup=BeautifulSoup(html)
		# links=soup.find_all('a',href=re.compile(r".+/(\d{6}/.*)".()))
		# for link in links:
		# 	print link['href']
		pages = etree.HTML(html.decode('utf-8'))
		a = pages.xpath(u'//td[@width="86%"]/a/@href')
		
		for i in a:
			i=i.strip('.')
			# print i
			b.append(i)
			
	return b	
	

# def get_data():
# 	hrefs=get_href()
def get_data(href):
		
		url="http://www.nmgs.gov.cn/ggfb/qybggg"+href
		re=requests.get(url)
		html=re.content
		pages = etree.HTML(html.lower().decode('utf-8'))
		a= pages.xpath(u"//td[@class='font_xl_tit_14']/text()")
		b= pages.xpath(u"//span[@style='font-family: 宋体; color: windowtext; font-size: 14pt']/text()|//span[@style='font-size: 16pt; font-family: 宋体']/text()|//span[@style='font-size: 16pt; line-height: 175%; font-family: 宋体']/text()")
		# for i in a:
		# 	print i+":\n\n\n"
		
		return b			# print i

		# 		b.append(a[i:i+3])		
		# 	c=tuple(b)
		# 	print html
	  	# 改为元组
		
		

def main():
	
	c=get_href()
	for i in c:
		data=get_data(i)
		for i in data[2:]:
			print i
			
	
if __name__ == '__main__':
	main()