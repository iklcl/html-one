#-*- coding:utf-8 -*-
#网址：http://www.sgmw.com.cn/dealer_search.html
#文件名：baojun.py
#作者: huanghong
#创建日期: 2017-12-8
#功能描述: 俊宝经销商
#完成状况：完成
import requests
import sys
from bs4 import BeautifulSoup
import re
import sqlite3

from datetime import datetime
import json
reload(sys)
sys.setdefaultencoding('utf-8')
headers={
	'ser-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest'
	}
def savesqlcar_4s(data,savepoint_name):
    #创建数据库
    con=sqlite3.connect(savepoint_name)
    con.execute('''CREATE TABLE IF NOT  EXISTS date_table
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

    sql='insert into date_table(province,city,company,salesTel,address,jwd,classify)\
    values("%s","%s","%s","%s","%s","%s","%s")'%(data[0],data[1],data[2],data[3],data[4],data[5],'俊宝经销商')
    con.execute(sql)
    con.commit()
    con.close()		
def get_city():
	date=[]
	req=requests.get('http://www.sgmw.com.cn/js/dealer_data.js?',headers=headers).content
	lis=re.findall(r'\"citylist\":(\[.*\])',req)[0]
	jd = json.loads(lis)
	for cit in jd:
		sheng=cit["p"]
		print sheng
		for c in cit["c"]:
			city=c["n"]
			date.append((sheng,city))
	return date		
			
			
def getP(city):
   	params={
			'cname':city[1]			}
	dat=requests.get('http://www.sgmw.com.cn/ashx/dealerInfo.ashx?',headers=headers,params=params).content  
	lis=re.findall(r'\[.*\]',dat)[0]
	jd = json.loads(lis)
	print len(jd)
	for cit in jd:
		date=[city[0],city[1],cit['company'],cit['tel'],cit['address'],cit['point']]
		savesqlcar_4s(date,'俊宝经销商.db')
def main():
	city=get_city()
	for i in city:
		getP(i)	
if __name__ == '__main__':
	main()