# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
class OnePipeline(object):
	#可选方法，作为类的初始化方法
	def __init__(self):
		self.filename = open('teacher.json','w')
	#处理数据，必须存在
	def process_item(self, item, spider):
		jsontext= json.dumps(dict(item),ensure_ascii=False)+"\n"
		self.filename.write(jsontext.encode('utf-8'))
		return item

	def closc_spider(self,spider):
		self.filename.close()