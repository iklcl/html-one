#-*- coding:utf-8 -*-

import random
from datetime import datetime,timedelta
from pymongo import MongoClient
import datetime,time
import logging
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')


#配置log
logging.basicConfig(
                level    = logging.INFO,
                format   = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                datefmt  = '%Y-%m-%d %H:%M',
                filename = "crawler.log",
                filemode = 'a');
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler();
console.setLevel(logging.WARNING);
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s');
# tell the handler to use this format
console.setFormatter(formatter);
logging.getLogger('').addHandler(console);


USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
]

#IP代理模块
class Proxy():
    def __init__(self):
        self.host = "127.0.0.1"
        self.database = "spidertools"
        self.username = "root"
        self.password = "123456"
        self.connect()
        self.length = len(self.ips)

    #链接并获取IP
    def connect(self):
        con = db.connect(host=self.host,db=self.database,user=self.username,passwd=self.password,charset='utf8')
        cur = con.cursor()
        sql = "select protocol,ip,port from proxyippool where score=(select max(score) from proxyippool) and failtimes<=1"
        cur.execute(sql)
        res = cur.fetchall()
        self.ips = map(lambda x:x[0]+'://'+x[1]+':'+x[2],res)
        cur.close()
        con.close()

    #移除无用的IP
    def removeIp(self,ip):
        self.ips.remove(ip)
        self.length = len(self.ips)
        if self.length==0:
            self.connect()

    #获取一个随机IP
    def randIp(self):
        return random.choice(self.ips)

    #返回所有IP
    def allIp(self):
        return self.ips


#mongo数据库存储
class Saving():
	def __init__(self):
		self.client = MongoClient()
		self.db = self.client.govSpider.mapkwd

	def finder(self,url,url2):
		result = self.db.find_one({"_id":url,"datas.url":url2})
		res = False
		if not result:
			pass
		else:
			res = True
		return res

	#接收一个url为主键id,传入一个list
	def save(self,url,data): 
		if not isinstance(data,list):
			raise ValueError('aguments error ,data must be a list.')
		for d in data:
			u = d.get('url')
			result = self.db.update({"_id":url},{"$addToSet":{"datas":d}},upsert=True) #主键查询是否存在数据数组，向数组内添加数据，如果数据存在则不添加
			logging.debug("%s,%s"%(u,str(result)))


def test():
	pass

if __name__ == '__main__':
	test()

