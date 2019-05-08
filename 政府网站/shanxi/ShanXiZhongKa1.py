#coding=utf-8

#文件名称：ShanXiZhongKa1.py
#作者：huanghong
#创建日期：2017-10-12
#功能描述：收集陕西重卡经销商信息
#网页地址：http://www.sxqc.com/jxswdRU/index_331.aspx
#处理进度：已完成（待优化）
import time
import requests
from bs4 import BeautifulSoup
import json
import re
import os.path
from datetime import datetime
import sqlite3
import MySQLdb as db
import sys
import codecs,csv
reload(sys)
sys.setdefaultencoding('utf-8')
se = requests.session()
headers={
	'Accept':'*/*',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Connection':'keep-alive',
	'Content-Length':'60',
	'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
	'Cookie':'ASP.NET_SessionId=5lh1muaruxcz13250wjq44iw',
	'Host':'www.sxqc.com',
	'Origin':'http://www.sxqc.com',
	'Referer':'http://www.sxqc.com/jxswdRU/index_331.aspx',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest'
}
def get_city():
	data=[[u'北京市',u'北京市'],[u'天津市',u'天津市'],[u'上海市',u'上海市'],[u'重庆市',u'重庆市']]
	js=se.get('http://www.sxqc.com/zqpc/scripts/area.js').content.replace('\n','').replace(' ','')
	lis=re.findall(r'\[.*\]',js)[0]
	jd = json.loads(lis)
	for i in jd:		
		level=i[u'level']
		if level=='1':
			shengfen=[i[u'name'],i[u'code']]
		if i[u'parentCode']== shengfen[1]:
			if shengfen[0] not in ['北京市','天津市','上海市','重庆市']:
				data.append([shengfen[0],i[u'name']])
	return data

def get_data(city):
	data={
	'cityName':city[1],
	'thisTypeId':'331'
	}
	req=se.post('http://www.sxqc.com/Ajax/GetMapDotInfo.ashx',headers=headers,data=data).content.replace('\n','')
	je=re.sub(r'\}(,)\{',';',req).replace(';','};{').split(';')
	jd=[i for i in je if i !='']
	# print jd
	print len(jd)
	if len(jd)!=0:
		for t in jd:
			i = eval(t)
			data=[city[0],city[1],i['title'],i['phone'],i['address'],i['point']]
			savesqlcar_4s(data,u'经销商.db')
def main():
	datas=get_city()
	for i in datas:
		print i[0]+'============='+i[1]
		get_data(i)
	
def savesqlcar_4s(data,savepoint_name):
    #创建数据库
    con=sqlite3.connect(savepoint_name)
    con.execute('''CREATE TABLE IF NOT  EXISTS buss_line
        (
        id integer primary key NOT NULL,
        province varchar(200) NOT NULL,
        city varchar(200) NOT NULL,
        district varchar(1000) DEFAULT NULL,
        company varchar(1000) DEFAULT NULL, 
        shopName varchar(1000) DEFAULT NULL,
        salesTel varchar(100) DEFAULT NULL,
        afterSalesTel varchar(100) DEFAULT NULL,
        RescueCall varchar(100) DEFAULT NULL,
        lng varchar(100) DEFAULT NULL,
        lat varchar(100) DEFAULT NULL,
        address varchar(1000) DEFAULT NULL,
        indexUrl varchar(100) DEFAULT NULL,
        fromUrl  varchar(100) DEFAULT NULL,
        others varchar(100) DEFAULT NULL, 
        jwd varchar(100) DEFAULT NULL,
        classify varchar(100) DEFAULT NULL);''')

    # 插入数据

    sql='insert into buss_line(province,city,company,salesTel,address,jwd,classify)\
    values("%s","%s","%s","%s","%s","%s","%s")'%(data[0],data[1],data[2],data[3],data[4],data[5],'陕西重型汽车有限公司经销商')
    con.execute(sql)
    con.commit()
    con.close()
main()	    