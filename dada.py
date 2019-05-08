#encoding:utf-8
#!/usr/bin/python
# s=[' abcde','g']
# f='gfdgg'

# for i in zip(s,f):
# 	print i[0]
# print s.sort()

# for i in [None]+range(-len(s),-1):

# 	print s[:i],i
# print range(1,5)

# aList = [123, 'xyz', 'zara', 'abc', 'xyz'];

# aList.reverse();
# print "List : ", aList;
# d={'l':'dsd','l':'fdgf'}
# for i in d:
# 	print i
# print [('xy'[i-1],i) for i in range(1,3)]

# print hash('gd')
# a=set('fdsfsfsfgfds')
# b=frozenset('hgjkkghkg')
# print a^b,a|b
# d={}

# print dict([('xy'[i-1],i) for i in range(1,3)]).items()

# -*- coding: utf8 -*-
import csv
# l = [['1', 'Wonderful Spam'],['2', 'Lovely Spam']]
# #模拟数据写入一个csv
# with open('eggs.csv', 'w') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=',',
#                             quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     for row in l:
#         spamwriter.writerow(row)
# #从文件读取
# l=[]
# with open('eggs.csv') as csvfile:
#      spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
#      for row in spamreader:
#          l = l + [row]
#          print l
# #把两列拼接增加为第三列写回到文件
# with open('eggs.csv', 'w') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     for row in l:
#         print(row)
#         spamwriter.writerow(row + [row[0]+row[1]])
# i=10
# while True:
# 	if i<3:
# 		break
# 	else:
# 		print i,'==================='
# 		for t in range(i):
# 			if i<8:
# 				break
# 			else:	
# 				print t
# a=['1','2','3']
# b=['1']
# c=['2a']
# if b[0] in a and c[0] in a:
# 	print 'fdsfa'	
# headers={
# 	'Upgrade-Insecure-Requests':'1',
# 	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
# }
# import requests
# req1=requests.get('https://114.mingluji.com/minglu/拖顶派出所_0',headers=headers).content.decode('utf-8','ignore')
# print req1
# a=['dfs']
# print 
# '/'.join(a)
# a=iter(range(10))
# rows =[1,2,3]
# def cols():
# 	yield 1
# 	yield 2 
# 	yield 3
# a=cols()
# # 
import os,sys
print sys.path[0]

# for tmpdir in ('/tmp',r'c:/temp'):

# try:
# 	i=1/1
# 	raise 
# 	print 'l'
# except Exception as e:
# 	print 'c'
	# i=1/1
	

	
# finally:
# 	print 'a'

# proxies=random.choice(ip) 
# proxy = {'http': proxies}
# print proxy  
# a=requests.get('http://httpbin.org/get',headers=headers,proxies=proxy)
# b=a.text
# print 

# def counter(a=0):
# 	count=[a]
# 	def uncr():
# 		count[0]+=1
# 		return count[0]
# 	return uncr	

# count=counter(100)
# print count()
output ='<int %r id=%#0x val=%d>'

# w=x=y=z=1
# def f1():
# 	x=y=z=2
# def f2():
# 	y=z=3
# def f3():
# 	z=4
# print output%('w',id(w),w)
# print output%('x',id(x),x)
# print output%('y',id(y),y)	
# print output%('z',id(z),z)



# clo =f3.func_closure
# if clo:
# 	print [str(c) for c in clo]
# else:
# 	print 'fd'
# 	f3()

# clo =f2.func_closure
# if clo:
# 	print [str(c) for c in clo]
# else:
# 	print 'fd'
# 	f2()

# clo =f1.func_closure
# if clo:
# 	print [str(c) for c in clo]
# else:
# 	print 'fd'
# 	f1()



# x=10
# def foo():
# 	y=5
# 	bar=lambda y:x+y
# 	print bar(y)
# 	y=8
# 	print bar(y)
# foo()	

# names = ['Tom', 'Jerry', 'Marry']
#过滤: 遍历列表names, 将每个列表元素保存在str_name中, 如果符合'r' in str_name条件, 则返回str_name
#      最终将所有符合条件的元素过滤出来.
# result = filter(lambda str_name: 'r' in str_name, names)
# print(list(result))			
# class p(object):
# 	def __init__(self):
# 		print 'a'
# class c(object):
# 	def __init__(self):
# 		print 'b'
# class d(p):
# 	def __init__(self):
# 		super(d,self).__init__()
# 		print 'd'
# class e(c):
# 	def __init__(self):
# 		super(e,self).__init__()	
# 		print 'e'		
# class f(p):
# 	def __init__(self):
# 		super(c,self).__init__()
# 		print 'd'


# def MyGenerator():  
#     value = (yield 1)  
#     value = (yield value)  
#     value = (yield 1)
  
# gen = MyGenerator()  
# print gen.next()  
# print gen.send(3)  


import random
import time
# def stupid_fib(n):
# 	index = 0
# 	a = 0
# 	b = 1
# 	while index < n:
# 		sleep_cnt = yield b
# 		print('let me think {0} secs'.format(sleep_cnt))
# 		time.sleep(sleep_cnt)
# 		a, b = b, a + b
# 		index += 1
# print('-'*10 + 'test yield send' + '-'*10)
# N = 20
# sfib = stupid_fib(N)
# fib_res = next(sfib)
# while True:
# 	print(fib_res)
# 	try:
# 		fib_res = sfib.send(random.uniform(0, 0.5))
# 	except StopIteration:
# 		break


# from time import time,ctime
#  class Timwea(object):
#  	def __init__(self,obj):
#  		self.__data=obj
#  		self.__ctime=self.__mtime=self.__atime=time()
#  		def get(self):
#  			self.__atime=time()
#  			return self.__data
#  		def gettiimeval(self,t_type):
#  			if not isinstance(t_type,str) or t_type[0] not in 'cma':
#  				raise TypeError,'dsdsd'
#  


# l为平时加班，k为周末加班				
# def money(l,k):
# 	a=2200
# 	b=21.75
# 	c=a/b
# 	x=c*1.5
# 	y=c*2
# 	money=l*x+y*k+2200
# 	return money

# print money(4,7.3)
# a=[1,2,3,4,5]
# print a[0:2]

# def a(a=0):
# 	print a
# a(a=1)	

# import string
# from string import punctuation 
# #先制定一个对应的密码表，将标点符号转成相同长度的空格
# table = string.maketrans(punctuation, ' '*len(punctuation))
# sentence = 'I come from China, hello world! hi.'

# #根据制定的密码表开始 translate
# a=sentence.translate(table)
# #根据制定的密码表开始 translate,删除空
# a2=sentence.translate(table,' ')

# print a,a2
#coding=gbk
 
import zlib, urllib
 
fp = urllib.urlopen(u'prov.rar')    # 访问的到的网址。
data = fp.read()
fp.close()
 
#---- 压缩数据流
str1 = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
str2 = zlib.decompress(str1)
print len(str1),len(str2)


