#-*- coding: utf8 -




import codecs,csv,sys
import re
import os.path


reload(sys)
sys.setdefaultencoding('utf-8')

path2=unicode(os.path.join(sys.path[0],'政务机关电话添加.csv'),'utf-8')
path3=unicode(os.path.join(sys.path[0],'政务机关电话验证.csv'),'utf-8')

# def read_path2():
# 	date=[]
# 	with codecs.open(path2,'rb') as f:
# 	    reader = csv.DictReader(f)
#     	print reader.next()


	# 		a=f.readlines()
	# 		for i in a:

	# 			lit=i.split(',')
	# 			if len(lit)>12:
	# 				print lit[12]
	# 				date.append(lit)
				
	# print len(date)			
	# return date
def read_path3():

	date=[]
	with codecs.open(path3,'r') as f:
		read = csv.DictReader(f)
    	print dir(read)
    	print read.next()
	# 		a=f.readlines()
	# 		for i in a:
	# 			lit=i.split(',')
	# 			print lit[12]
	# 			date.append(lit)			
	# return date
def main():
	date1=read_path2()	
	date2=read_path3()
	for i in date2:
		for raw in date2:
			if raw[2]==i[2]:
				pass

if __name__ == '__main__':
	read_path3()


