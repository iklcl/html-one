#coding=utf-8

#文件名称：baidu.py
#作者：huanghong
#创建日期：2018-3-11
#功能描述：百度搜索
#网页地址：https://www.baidu.com/
#处理进度：已完成（待优化）


import requests,random
from lxml import etree
import sys
import codecs,csv
import re
import os.path
from datetime import datetime
import gevent  
from multiprocessing import Pool,Lock
import multiprocessing
from gevent import monkey; monkey.patch_all()  
reload(sys)
sys.setdefaultencoding('utf-8')


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
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
]



Loc = Lock()
pages=[]



def main():
	data = read_file()
	for i in data:
		keyworld=i[0]
		# with codecs.open('uipat.csv','ab') as f:
		# 	w = csv.writer(f)
		# 	w.writerow([keyworld])
		for page in xrange(10):
			data={
				'wd':keyworld,
				'pn':'%s0'%page,
				'oq':keyworld,
				'bs':keyworld
				}
			pages.append([data,i[1],i[2]])
	print len(pages)	



		
def read_file():
	data=[]
	with codecs.open(u'互联网核实20171211.csv','r') as f:
		a=f.readlines()
		t=0
		for i in a[1:len(a)]:
			# t+=1
			# if t==101:
			# 	break
			name_list=i.replace('\n','').split(',')

			if name_list[5]!='':
				name=name_list[5]+name_list[6]
			elif name_list[4]!='':
				name=name_list[4]+name_list[6]
			else:
				name=name_list[3]+name_list[6]	
			data.append([name.replace(' ','').decode('gbk'),name_list[6].decode('gbk'),name_list[0]])
	return data	




def process_start(url_list): 
    # with Loc:
	    tasks = []  
	    for data in url_list:  
	        tasks.append(gevent.spawn(get_data,data))  
	    gevent.joinall(tasks)#使用协程来执行 	
	
def get_data(params):	
	headers={
		"User-Agent":random.sample(USER_AGENTS,1)[0],
		"X-Requested-With":"XMLHttpRequest"	
		}
	
	html=requests.get('https://www.baidu.com/s',headers=headers,params=params[0]).content
	# except Exception as e:
	# 	pass
	pages=etree.HTML(html.decode('utf-8').replace('<em>','').replace('</em>',''))
	href=pages.xpath(u'//div[@class="result c-container "]/h3[position()=1]')
	for i in href:
		title=i.xpath('a/text()')[0]
		if params[1] in title:
			data=[params[2],params[0]['wd'],title,i.xpath('a/@href')[0]]
			with codecs.open(u'数据.csv','ab') as f:
				w = csv.writer(f)
				w.writerow(data)

def run():
    main()
    url_list=[]
    i = 0 #计数器，记录添加了多少个url到协程队列  
    while True:  
        i += 1 
        if len(pages)==0:
        	break
        url=pages.pop()
        url_list.append(url)#每次读取出url，将url添加到队列  
        if i ==4:#一定数量的url就启动一个进程并执行  
            print i
            process_start(url_list)
            url_list = [] #重置url队列  
            i = 0 #重置计数器  
    if len(url_list)!=0:#若退出循环后任务队列里还有url剩余  
        process_start(url_list) 



if __name__ == '__main__':
	run()


