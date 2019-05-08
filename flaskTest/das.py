#-*- coding=utf-8 -*-  
# import time
# import gevent
# from gevent.threadpool import ThreadPool

# def sum(i):
#     i = 0
#     for i in xrange(100000000):
#         i += i+1 * 20 / 10 * 10 /10

# def test(n,m):
#     m=m
#     vals = []
#     keys = []
#     for i in xrange(m):
#         vals.append(i)
#         keys.append('a%s'%i)
#     d = None
#     for i in xrange(n):
#         d = dict(zip(keys, vals))
#     return d

# pool = ThreadPool(20)
# start = time.time()
# # for _ in xrange(10):
# #     pool.spawn(test, 1000000,100)
# # gevent.wait()
# test(1000000,100)
# delay = time.time() - start
# print 'Running "time.sleep(1)" 4 times with 3 threads. Should take about 2 seconds: %.3fs' % delay

# for (a,b) in [(1,2),(3,4)]:
# 	print a,b
# for ((a,b),c) in [((1,2),3),('xy',6)]:
# 	print a,b,c	
# for (a, *b) in [(1,2,3),(4,5,6)]:
# 	print a,b
# M=[[1,2,3],[4,5,6],[7,8,9]]
# res=[sum(row) for row in M]
# print res
# res2=[c*2 for c in 'spam']
# print res2
# res3=[a*b for a in [1,2] for b in [4,5]]
# print res3
# res4=[a for a in [1,2,3] if a<2]
# print res4
# for teama,teamb in zip([1,2],[3,4]):
# 	print teama
# for teama,teamb in enumerate([1,2,3,4,5]):
# 	print teama,teamb

# def keyonly(**b):
# 	print b
# keyonly(q=1,b=2)	

# f=lambda x,y,z:x+y+z
# print f(1,2,3)


# print map((lambda x :x+1),[1,2,3,4])
# print filter((lambda x :x>1),[1,2,3,4])

# #生成器函数
# def a(w):
# 	for i in range(w):
# 		yield i**2
# for i in a(5):
# 	print i	
# x=a(5)
# print next(x)		

# g=(x**2 for x in range(5))
# print next(g)

# x=22
# def text():
# 	global x
# 	print x
# 	x=88
# 	if False:
# 		x=88
# text()	



# def foo(list=[]):
# 	list.append(9)
# 	print list
# foo()
# foo()
# foo()	


# class c1:
# 	def __init__(self,name):
# 		self._name=name
# 	def _str_(self):
# 		return "self .name =%s"%self._name
# I=c1('tom')
# print I	
# print I._name


# class B():
# 	def imeth(self,x):
# 		print (self,x)
# 	def smeth(x):
# 		print x
# 	def cmeth(cls,x):
# 		print (cls,x)
# 	smeth =staticmethod(smeth)
# 	cmeth= classmethod(cmeth)
# obj =B()
# obj.imeth(1)
# B.imeth(obj,2)
# B.smeth(3)
# obj.smeth(4)
# B.cmeth(5)



# class C1():
# 	def __init__(self,name):
# 		self.__name=name
# 	def __str__(self):
# 		return 	
# obj.cmeth(6)



# print {True:'yes',1:'no',1.0:'maybe'}
def a1(b,a=0):

	l=a*b

	if l==0:
		print l
		a+=1
		return a1(b,a)
	print l	
a1(6,0)	