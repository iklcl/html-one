#-*- coding:utf-8 -*-
import argparse
import importlib
import logging
import os,sys
from ccgp import Auxiliary

reload(sys)
sys.setdefaultencoding('utf-8')

basedir = os.path.abspath(os.path.dirname(__file__))

#查询spiders目录下所有的py文件并执行它
def runSpiders(nd=10):
	logging.info(u'>>>>>>>>>>>>>>>>>>>>>>>>开始运行>>>>>>>>>>>>>>>>>>>>>>>>')
	#删选目录下的.py文件
	fs = os.listdir('C:\Users\Administrator\Desktop\gov1')
	mods = []
	for f in fs:
		if f.startswith('ccgp_') and f.endswith('.py'):
			mods.append(f.split('.')[0])
	logging.info(u'发现模块数:%d'%len(mods)),'==============================='

	kwdfile = os.path.join(basedir,'keywords.txt')
	if not os.path.exists(kwdfile):
		kwds.append(u'地图')
	else:
		with open(kwdfile,'rb') as f:
			data = f.readlines()
		kwds=map(lambda x:x.strip().decode('utf-8'),filter(lambda x:x.strip(),data))
	if len(kwds)==0:
		logging.error(u'没有关键词提供搜索，请再当前目录下建立关键词txt文件，每行一个关键词')
		return False
	#循环执行
	for mod in mods:
		try:
			#使用importlib动态导入模块
			data = importlib.import_module('%s'%mod)
			logging.info(u'导入模块: %s'%mod)
			for kwd in kwds: #循环查询多个关键词
				print kwd,'==========',mod
				d = data.Crawler()
				logging.info(u'查询关键词: %s'%kwd)
				# print d
				d(nd,keyword=kwd)
		except Exception,e:
			# print e
			logging.error(u'执行模块失败,name=%s,reason=%s'%(mod,str(e)))
	logging.info(u'<<<<<<<<<<<<<<<<<<<<<<<<运行结束<<<<<<<<<<<<<<<<<<<<<<<<')

#使用argparse模块去支持命令行模式的调用
parser = argparse.ArgumentParser()
parser.add_argument('-d',type=int,help='search,how many days would you want') #调用方式:python 模块名 -d 天数
args = parser.parse_args()
#如果当前调用带着参数，则传递参数，否则直接使用默认参数运行
if args.d:
	runSpiders(args.d)
else:
	runSpiders()
