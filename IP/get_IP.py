#-*- coding:utf-8 -*-
#网址：
#文件名：get_IP.py
#作者: huanghong
#创建日期: 2017-010-15
#功能描述: 获取网站免费ip
#完成状况：完成
import test_IP
import random
import time
import requests
from lxml import etree
import lxml.html
import sys
import codecs,csv
from bs4 import BeautifulSoup
import re
import sqlite3
import MySQLdb 
import os.path
from datetime import datetime
import multiprocessing
reload(sys)
sys.setdefaultencoding('utf-8')
headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }
#存入数据库
def save_sql(datas):
	# 打开数据库连接
	db = MySQLdb.connect("127.0.0.1","root","123456","IP" )
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	# 创建数据表SQL语句
	# cursor.execute("""CREATE TABLE IF NOT  EXISTS data (
 #        IP varchar(100) NOT NULL);""")
	for data in datas:
		# sql=
		print data
		cursor.execute('insert into data(IP) values( "%s")' % \
             (data))
	db.commit()	
	# 关闭数据库连接
	db.close()





def get_ip_list2(): 
    date=[]
    for i in xrange(20):
        url= 'http://www.66ip.cn/mo.php?tqsl=%s'%i  
        web_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(web_data.text, 'lxml')
        try:
            ips = soup.find_all('p')[0].text
        except Exception as e:
            break
        # data=re.findall('(\d+.\d+.\d+.\d+:\d+)<br>',ips)
        data=ips.replace(' ','').replace('$(function(){','').replace("$('#adarea').slideDown(500);",'').replace("$('#adarea').slideUp(500);",'').replace("$('#adclose').click(function(){",'').replace('});','').replace('\r','').replace('\t','').split('\n')
        data_ip=['http://'+x for x in data if x!='']
        check=test_IP.ClassName(data_ip)
        ip=check.thread()
        try:
            for i in check.ipdata:
                date.append(i)
        except Exception as e:
            pass
    print len(set(date))        
    # savesql_db_ip(set(date),'IP.db') 
    save_sql(data)
    
    



#西刺代理
class Xici_ip():
    
    def __init__(self,ip):
        self.ip=ip


    def get_ip_list(self,url,i=0):
        i+=1
        ip_list = []
        proxies=random.choice(self.ip) 
    	proxy = {'https': proxies} 
        try:
            web_data = requests.get(url, headers=headers,proxies=proxy)
        except Exception as e:
            if i>5:
                return ip_list
            else:
                time.sleep(1)   
                return self.get_ip_list(url,i)     
        if web_data.status_code ==200:
            soup = BeautifulSoup(web_data.text, 'lxml')
            ips = soup.find_all('tr')           
            for i in range(1, len(ips)):
                ip_info = ips[i]
                tds = ip_info.find_all('td')
                http=tds[5].text.lower()
                if http=='http':
                    ip_list.append(http+'://'+tds[1].text + ':' + tds[2].text)         
            return ip_list
        else:
            return self.get_ip_list(url,i)
            time.sleep(1)
            if i>5:
                return ip_list    


    def get_data(self):
        mun=0
        date=[]
        while True:          
            mun+=1    
            url = 'http://www.xicidaili.com/nn/'+str(mun)
            print url 
            ip_list = self.get_ip_list(url)
            if len(ip_list)<10:
                break
            check=test_IP.ClassName(ip_list)
            ip=check.thread()
            try:
                for i in check.ipdata:
                    date.append(i)
            except Exception as e:
                pass
        print len(set(date))        
        save_sql(data) 
            

#快代理
class gao_ip():
    def __init__(self,ip):
        self.ip=ip
              
    def get_ip_list(self,url,i=0):
        i+=1
        ip_list = []
        proxies=random.choice(self.ip) 
        proxy = {'http': proxies} 
        try:
            web_data = requests.get(url, headers=headers)
            print url
        except Exception as e:
            time.sleep(1)
            if i<5:
                return self.get_ip_list(url,i)
            else:
                return ip_list
        print web_data.status_code
        if web_data.status_code ==200:
            soup = BeautifulSoup(web_data.text, 'lxml')
            ips = soup.find_all('tr')
            # print len(ips)
            for i in range(1, len(ips)):
                ip_info=ips[i]                  
                tds = ip_info.find_all('td')
                http=tds[3].string.lower()
                if http=='http':
                    ip_list.append(http+'://'+tds[0].text+ ':' + tds[1].text)
            time.sleep(2)
            # print len(ip_list)
            return ip_list
        else:
            return ip_list    

    def get_data(self):
        mun=0
        date=[]
        while True:
            mun+=1   
            url = 'http://www.kuaidaili.com/free/inha/%s/'%str(mun)    
            ip_list = self.get_ip_list(url)         
            if len(ip_list)<1:
                break         
            check=test_IP.ClassName(ip_list)
            ip=check.thread()
            print len(check.ipdata)
            try:
                for i in check.ipdata:
                    date.append(i)
            except Exception as e:
                pass
        print len(set(date)) 
        save_sql(data)
            



#66代理
class six_ip():
    def __init__(self,ip):
        self.ip=ip   
        
    def get_ip_list(self,url,i=0):
        i+=1
        ip_list = []
        proxies=random.choice(self.ip) 
        proxy = {'https': proxies}  
        try:
            web_data = requests.get(url, headers=headers,proxies=proxy)
            print url
        except Exception as e:
            time.sleep(1)
            return self.get_ip_list(url,i)
            if i>5:
                return ip_list
        print web_data.status_code
        if web_data.status_code ==200:
            soup = BeautifulSoup(web_data.text, 'lxml')
            table=soup.find_all('table',width="100%")[0]
            ips = table.find_all('tr')
            for i in range(1, len(ips)):
                ip_info=ips[i]                  
                tds = ip_info.find_all('td')               
                ip_list.append('http'+'://'+tds[0].text+ ':' + tds[1].text)
            return list(set(ip_list))
            print len(list(set(ip_list)))
        else:
            return ip_list 

    def get_data(self):
        date=[]
        for mun in range(1,35):
            for page in range(1,5):   
                url = 'http://www.66ip.cn/areaindex_%s/%s.html'%(str(mun),str(page))
                ip_list = self.get_ip_list(url)                                         
                check=test_IP.ClassName(ip_list)
                ip=check.thread()
                try:
                    for i in check.ipdata:
                        date.append(i)
                except Exception as e:
                    pass
        print len(set(date))        
        save_sql(data)



#读取ip数据库，调用ip
def savesql_ip():
    data=[]  
    con=sqlite3.connect('IP.db')
    datas=con.execute('SELECT IP from data')
    for i in datas:
        data.append(i[0])   
    con.commit()
    con.close()
    return data



def main():
    get_ip_list2()


    # ip=savesql_ip()
    #西刺
    # get_xici=Xici_ip(ip)    
    # get_xici.get_data()
    # # # #快代理
    # get_gao=gao_ip(ip)    
    # get_gao.get_data()
    # # #66代理 
    # get_six=six_ip(ip)    
    # get_six.get_data()  




if __name__ == '__main__':
    main()
    