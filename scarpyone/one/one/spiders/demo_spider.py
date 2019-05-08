#coding=utf-8
import scrapy
from one.items import DmozItem
class DmozSpider(scrapy.Spider):
    #爬虫名
    name = "dmoz"
    #允许爬虫作用的范围
    allowed_domains = ["dmoz.org"]
    #爬虫其实的url
    start_urls = [
        "http://www.itcast.cn/channel/teacher.shtml#ajavaee"
    ]

    #下载回来的数据，处理
    def parse(self, response):
        # data=[]
        for sel in response.xpath('//div[@class="li_txt"]'):
            item=DmozItem()
            #将匹配的结果转换成unicode对象
            title = sel.xpath('./h3/text()').extract()
            link = sel.xpath('./h4/text()').extract()
            desc = sel.xpath('./p/text()').extract()
            # print title[0], link[0], desc[0]
            item['title']=title[0]
            item['link']=link[0]
            item['desc']=desc[0]
            #如果是数据会返回到管道文件
            yield item

            # data.append(item)
        # return data    