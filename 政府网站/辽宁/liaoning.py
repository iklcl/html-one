##-*- coding:utf-8 -*-

import requests
import re
import json
import codecs,csv
import time
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
}


def get_href():
		url = 'http://www.lngs.gov.cn/ecdomain/framework/lngs/anlfaiemapdbbbofiohcpgjmokfngfef.jsp'

		res = requests.get(url,headers=headers)
		html=res.content
		pages = etree.HTML(html.decode('utf-8'))
		a = pages.xpath(u'//div[@class="anou_nscrl"]/ul/li/a/@href')
		return a
	
	
def get_data(href):
		url= 'http://www.lngs.gov.cn'+href
		
		htmlllll=requests.get(url)
		html=htmlllll.content
		pages = etree.HTML(html.decode('utf-8'))
		a = pages.xpath(u'//div[@id="newscontent"]/text()[position()>3]')
		return a


def main():
	href=get_href()
	for i in href:
		print i
		data=get_data(i)
		for a in data:
			a=[a.split()]
			for i in a:
			# 	print i
			# b=[]
			# for i in range(0, len(a),3):
			# 	b.append(a[i:i+3])
				c=tuple(i)	
			with codecs.open(u'辽宁.csv', 'ab') as f:
				w = csv.writer(f)
				w.writerow(c)


if __name__ == '__main__':
		main()	

# http://www.lngs.gov.cn/ecdomain/framework/lngs/anlfaiemapdbbbofiohcpgjmokfngfef/mpddalcmapepbbofijlnmopmhoafpelk.do?isfloat=1&disp_template=kjicdckpjmfgbboellfgjcfmdpgegfkn&moduleIDPage=mpddalcmapepbbofijlnmopmhoafpelk&siteIDPage=lngs&infoChecked=0&ggname=4A47444E659B4C2BAC707F6550F2A8AF
