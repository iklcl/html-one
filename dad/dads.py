
#coding=utf-8

import requests,random,time,json
import urllib
from lxml import etree
import sys
import codecs,csv
import re
import os.path
import sqlite3
import MySQLdb 
from datetime import datetime
import threading
from multiprocessing import Pool,Lock,Process
import multiprocessing
reload(sys)
sys.setdefaultencoding('utf-8')



lock = threading.Lock()
Loc = Lock()



class D():
	def __init__(self):
		self.data=[]
		for i in range(100000):
			self.data.append(str(i))

	def dada(self):
		while True:
			lock.acquire()
			if len(self.data)==0:
				lock.release()
				break
			else:
				url=self.data.pop(0)
				lock.release()
				print len(self.data)
				with codecs.open('path1.csv','ab') as f:
					w = csv.writer(f)
					w.writerow([url])




def thread2():
	# with Loc:	
		da=D()
		tasks = [] 
		for x in range(20):
			t= threading.Thread(target=da.dada) 
			t.setDaemon(True) 
			tasks.append(t)
		for t in tasks:
			t.start() 
		for t in tasks:
			t.join()


def pool():
	pool = multiprocessing.Pool(processes = 4)
	pool.apply_async(thread2)
	pool.close()
	pool.join()

if __name__ == '__main__':
	# pool()		
	# thread2()
	t=[]
	a=[['1'],['2'],['3'],['1']]
	for i in a :
		if i not in t:
			t.append(i)
	print t