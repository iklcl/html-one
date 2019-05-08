#coding=utf-8

#文件名称：IHG.py
#作者：huanghong
#创建日期：2018-3-30
#功能描述：洲际酒店集团信息搜索
#网页地址：https://www.ihg.com/content/cn/zh/make-a-reservation#
#处理进度：已完成（待优化）

import requests,random,time,json
from lxml import etree
import sys
import codecs,csv
import re
import os.path
import sqlite3
import MySQLdb 
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf-8')
se = requests.session()
hotellist=[]
headers1={

'accept':'application/json, text/plain, */*',
'accept-encoding':'gzip, deflate, br',
'accept-language':'zh-CN,zh;q=0.9',
'origin':'https://www.ihg.com',
'referer':'https://www.ihg.com/hotels/cn/zh/find-hotels/hotel/list?qDest=Ningxia,%20China&qCiMy=22018&qCiD=30&qCoMy=22018&qCoD=31&qAdlt=1&qChld=0&qRms=1&qRtP=6CBARC&qAkamaiCC=US&qSrt=sDD&qBrs=ic.ki.ul.in.cp.vn.hi.ex.cv.rs.cw.sb.&qAAR=6CBARC&srb_u=1',
'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
'x-ihg-api-key':'se9ym5iAzaW8pxfBjkmgbuGjJcr3Pj6Y'
}
headers2={
'accept':'application/json, text/plain, */*',
'accept-encoding':'gzip, deflate, br',
'accept-language':'zh-CN,zh;q=0.9',
'content-length':'352',
'content-type':'application/json; charset=UTF-8',
'ihg-language':'zh-CN',
'origin':'https://www.ihg.com',
'referer':'https://www.ihg.com/hotels/cn/zh/find-hotels/hotel/list?qDest=SHANGHAI,China,People%27s%20Republic%20of&qCiMy=22018&qCiD=30&qCoMy=22018&qCoD=31&qAdlt=1&qChld=0&qRms=1&qRtP=6CBARC&qAkamaiCC=US&qSrt=sDD&qBrs=ic.ki.ul.in.cp.vn.hi.ex.cv.rs.cw.sb.&qAAR=6CBARC&srb_u=1',
'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Mobile Safari/537.36',
'x-ihg-api-key':'se9ym5iAzaW8pxfBjkmgbuGjJcr3Pj6Y',
'x-ihg-mws-api-token':'58ce5a89-485a-40c8-abf4-cb70dba4229b'
}
city=[
	'北京市',
	'天津市',
	'上海市',
	'重庆市',
	'河北省',
	'山西省',
	'辽宁省',
	'吉林省',
	'黑龙江省',
	'江苏省',
	'浙江省',
	'安徽省',
	'福建省',
	'江西省',
	'山东省',
	'河南省',
	'湖北省',
	'湖南省',
	'广东省',
	'海南省',
	'四川省',
	'贵州省',
	'云南省',
	'陕西省',
	'甘肃省',
	'青海省',
	'内蒙古自治区',
	'广西壮族自治区',
	'西藏自治区',
	'宁夏回族自治区',
	'新疆维吾尔自治区']


def get_ctjwd(i):
	data=[]
	params={
		'destination':i
	}	
	req=se.get('https://apis.ihg.com/locations/v1/destinations',params=params,headers=headers1).content
	text=json.loads(req)[0]
	data=[text["longitude"],text["latitude"],text["clarifiedLocation"]]
	return data
def get_data(cicode):
	# cicode
	a={"lng": cicode[0], "lat": cicode[1], "location":cicode[2] }
	
	data={
	'bulkAvailability':'true',
	'checkDailyPointsCost':"true",
	'corporateId':"",
	'location':a,
	'stay':{"travelAgencyId": "", "dateRange": {"start": "2018-03-30", "end": "2018-03-31"}, "rateCode": "6CBARC","rooms":1,"adults":1,"children":0},	
	'version':"1.3"
	}	
	data=json.dumps(data)
	da=se.post('https://apis.ihg.com/guest-api/v1/ihg/cn/zh/searchLight',headers=headers2,data=data).content
	string=re.findall('"hotels":(\[.*?\]),"radius"',da)
	if len(string)==0:
		return
	text=json.loads(string[0])
	print len(text)
	for i in text:
		# test(i['hotelCode'])
		hotellist.append(i['hotelCode'])
	# print da


def test(cid):
	headerss={
	'Accept':'application/json, text/plain, */*',
	'IHG-Language':'zh-CN',
	'Origin':'https://www.ihg.com',
	# 'Referer':'https://www.ihg.com/hotels/cn/zh/find-hotels/hotel/list?qDest=SHANGHAI,China,People%27s%20Republic%20of&qCiMy=22018&qCiD=30&qCoMy=22018&qCoD=31&qAdlt=1&qChld=0&qRms=1&qRtP=6CBARC&qAkamaiCC=US&qSrt=sDD&qBrs=ic.ki.ul.in.cp.vn.hi.ex.cv.rs.cw.sb.&qAAR=6CBARC&srb_u=1',
	'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Mobile Safari/537.36',
	'x-ihg-api-key':'se9ym5iAzaW8pxfBjkmgbuGjJcr3Pj6'
	}
	try:
		req=se.get('https://apis.ihg.com/hotels/v1/profiles/%s/details'%cid,headers=headerss).content
		adr=re.findall('\{"hotelInfo":(\{.*\})\}',req)[0]
		text1=json.loads(adr)
	except Exception as e:
		print cid
		return
	
	adress=text1['address']['street1']
	city=text1['address']['city']
	name=text1['profile']['name']
	lat=text1['profile']['latitude']
	lng=text1['profile']['longitude']
	try:
		tel=text1['contact'][0]['faxNumber']
	except Exception as e:
		tel=''
	
	Id=text1['brandInfo']['brandName'].replace(' ','').lower().replace('hotels','')
	url='https://www.ihg.com/%s/hotels/cn/zh/shanghai/%s/hoteldetail'%(Id,cid.lower())
	data=[city,name,adress,tel,lat,lng,url]
	savesql_hotel(data,'洲际酒店.db')

def savesql_hotel(data,savepoint_name):
    #创建数据库
    con=sqlite3.connect(savepoint_name)
    con.execute('''CREATE TABLE IF NOT  EXISTS data
        (
        hoteltype varchar(200) NOT NULL,
        -- province varchar(200) NOT NULL,
        city varchar(200) NOT NULL,
        name varchar(1000) DEFAULT NULL,
        address varchar(1000) DEFAULT NULL,
        salesTel varchar(100) DEFAULT NULL, 
        lat varchar(100) DEFAULT NULL,
        lng varchar(100) DEFAULT NULL,
        Url  varchar(1000) DEFAULT NULL);''')
    # 插入数据
    sql='insert into data(hoteltype,city,name,address,salesTel,lat,lng,Url)\
    values("%s","%s","%s","%s","%s","%s","%s","%s")'%(u'洲际酒店',data[0],data[1],data[2],data[3],data[4],data[5],data[6])
    con.execute(sql)
    con.commit()
    con.close()

def main():
	for i in city:
		print i
		data=get_ctjwd(i)
		get_data(data)
	for i in hotellist:
		test(i)
if __name__ == '__main__':
	main()