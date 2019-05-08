
#-*- coding:utf-8 -*-
#网址：http://hozonauto.com/wdcx.html
#文件名：hezhong.py
#作者: huanghong
#创建日期: 2017-010-16
#功能描述: 合众汽车网点查询
#完成状况：完成
import sqlite3
import MySQLdb as db
import requests
import lxml.html
import sys
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"
}
def get_data():
	datas=[]
	req=requests.get('http://hozonauto.com/xswl/map.xml',headers=headers).content
	soup=BeautifulSoup(req,'lxml')
	item=soup.find_all('item')
	for i in item:
		print i.get('title')
		lis=i.find_all('list')
		if len(lis)!=0:
			for t in lis:
				data=[i.get('title'),t.get('title'),t.get('phone'),t.get('addd')]
				datas.append(data)
	savesqlcar_4s(datas,'合众汽车.db')
def savesqlcar_4s(datas,savepoint_name):
    #创建数据库
    con=sqlite3.connect(savepoint_name)
    con.execute('''CREATE TABLE IF NOT  EXISTS data
        (
        id integer primary key NOT NULL,
        province varchar(200) NOT NULL,
        city varchar(200) DEFAULT NULL,
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
    for data in datas:
	    sql='insert into data(province,company,salesTel,address,jwd,classify)\
	    values("%s","%s","%s","%s","%s","%s")'%(data[0],data[1],data[2],data[3],'无经纬度','合众汽车网点')
	    con.execute(sql)
    con.commit()
    con.close()					
def main():
	get_data()	
if __name__ == '__main__':
	main()