#coding=utf-8

#文件名称：189mv.py
#作者：huanghong
#创建日期：2018-4-16
#功能描述：院线通电影院品牌收集
#网页地址：http://www.189mv.cn/cinema/
#处理进度：已完成（待优化）
import requests
from lxml import etree
from bs4 import BeautifulSoup
import sys
import codecs,csv
import re
import os.path
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf-8')
se=requests.session()

logg=unicode(sys.path[0]+'\\logs.log','utf-8')
headers={

'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest'
}

path=unicode(os.path.join(sys.path[0],'院线通.csv'),'utf-8')

def get_city():
	data=[]
	city=requests.post('http://www.189mv.cn/qryCitys.htm').content
	html = etree.HTML(city.decode('utf-8'))
	all_a=html.xpath(u"//div[@class='city city_all']/ul//li/p//a")
	for a in all_a:
		ci=a.xpath('./@href')
		name=a.xpath('./text()')
		cityid=re.findall(r"javaScript:changeCity\('(\d+)'\);",ci[0])[0]
		data.append([name[0],cityid])
	return data


def get_hotel(cityid):
	data1={
		'cityid':'%s'%cityid[1]
	}
	print cityid[0]
	se.post('http://www.189mv.cn/xhgCity.htm',headers=headers,data=data1)
	se.post('http://www.189mv.cn/isLogin.htm',headers=headers)
	data={
		'rid': 'all',
		'key': ''
	}

	req=se.post('http://www.189mv.cn/qryCinemas.htm',headers=headers,data=data)
	soup=BeautifulSoup(req.content,'html.parser')
	div=soup.find_all('div',class_='area_s mart10 com_b')
	for div2 in div:
		div3=div2.find_all('div',class_="area_c")[0]
		dl=div3.find_all('dl')
		for i in dl:
			h3=i.find_all('h3')[0]
			name=h3.text
			href=h3.find_all('a')[0].get('href')
			p=i.find_all('p')
			adress=p[0].text
			try:
				js=p[0].find_all('a')[0].get('href')
				jwd=re.findall("javascript:showMap\('(.*?)','(.*?)','.*?'\);",js)[0]
				lat=jwd[0]
				lng=jwd[1]
				tel=adress=p[1].text.replace(u'电话:','')
			except Exception as e:
				lat=''
				lng=''
				tel=''
			
			print name
			data=[cityid[0],name,adress,tel,lat,lng,href]
			with codecs.open(path,'ab') as f:
				w = csv.writer(f)
				w.writerow(data)

#log日志
def loggs(strs):
    with open(logg,'ab') as f:

        time = str(datetime.now())[:-7]
        t = os.linesep
        s = time+' : '+str(strs)
        print s
        f.write(s+t)
	
def main():
	with codecs.open(path,'wb') as f:

		w = csv.writer(f)

		w.writerow([u'城市',u'名称',u'地址',u'电话',u'经度',u'纬度',u'网址'])
	data=get_city()

	for city in data:

		get_hotel(city)


if __name__ == '__main__':
	main()
	

	