# -*-coding:utf-8-*-

# 文件名称: ccgp_ningbo.py
# 作者: lixue
# 创建日期: 2017-11-28
# 功能描述: 收集宁波政府采购网信息
# 抓取地址: http://www.ccgp-ningbo.gov.cn/index.aspx
# 处理进度：已完成

import re,os,sys
import requests
import time
import datetime
import random
from bs4 import BeautifulSoup
from ccgp import Auxiliary as au

reload(sys)
sys.setdefaultencoding('utf-8')

"""宁波政府采购网信息"""
class Crawler():
    def __init__(self):
        self.indexurl = 'http://www.ccgp-ningbo.gov.cn/index.aspx'#首页url
        self.headers = {"User-Agent":random.choice(au.USER_AGENTS)}#请求头
        
        self.updates = []#更新的信息
        self.mongos = au.Saving()#保存的类
        self.now = datetime.datetime.strptime(str(datetime.date.today()),'%Y-%m-%d')#当前时间
        

    def __call__(self,nd,keyword):
        self.searchword = keyword#搜索条件
        self.nd = nd
        try:
            self.getinfos()
        except Exception as e:
            raise
            # return False

    """获取查询后的信息宁波政府采购网信息"""
    def getinfos(self):
        for types in xrange(1,7):
            # print types
            if types==1 or types==2 or types==3:
                self.firsecth(types)
                # pass
            elif types==4:
                NoticeType = '1'
                self.forfiv(NoticeType)
            elif types==5:
                NoticeType = '2'
                self.forfiv(NoticeType)
            elif types==6:
                # self.sixinfo()#没有时间，没做更新，需要的时候就收集
                pass
        au.logging.info(u'宁波政府采购网信息-更新数量:(%s)'%(len(self.updates)))

    '''
    Function:请求网页信息
    args:网址,参数
    '''
    def requrl(self,url,params):
        res = requests.get(url,headers=self.headers,params=params)
        res.encoding = 'utf-8'
        content = res.content
        return content

    '''
    Function:保存信息
    args:table bs对象,拼接url的前段
    '''
    def saveinfo(self,tables,webh):
        if len(tables)>0:
            tds = tables[0].find_all('td')[:-2]#td
            for ti in xrange(len(tds)):
                uptime = ''#用于定义 日期
                try:
                    href = tds[ti].a['href']#链接
                    txts = tds[ti].a.string#公告名称
                except Exception as e:
                    # 没有a 标签 下的信息
                    times = tds[ti].string
                    if times!=None:
                        times = re.sub('\t|\r|\n| ','',times)
                    try:
                        uptime = datetime.datetime.strptime(times,'%Y-%m-%d')#用于得到 更新时间
                    except Exception as e:
                        pass
                infos = {}#存放公告信息
                # 当更新时间不为空
                if uptime!="":
                    # 判断是否是当天的，是否需要更新保存
                    # if datetime.datetime.now().isocalendar()==uptime.isocalendar():
                    if abs((self.now-uptime).days)<=self.nd:
                        # print '111111111111'
                        infos['title'] = txts
                        infos['url'] = webh + href
                        infos['updatetime'] = uptime
                        self.updates.append(infos)#把更新的信息放进infos
                        self.mongos.save(self.indexurl,self.updates)#保存进mongodb

    '''
    Function:1-资格预审公告,2-采购公告,3-采购结果公告
    args:类型编号
    '''
    def firsecth(self,types):
        searchurl = 'http://www.ccgp-ningbo.gov.cn/project/NoticeSearch.aspx'#搜索的url
        # 参数
        params = {
            "NoticeTitle":self.searchword,
            "Region":"",
            "TenderId":"",
            "Type":str(types)
        }
        content = self.requrl(searchurl,params)
        # 使用beautiful解析网页
        soup = BeautifulSoup(content,'html.parser')
        tables = soup.find_all(id='ctl00_ContentPlaceHolder3_gdvNotice3')#table
        webh = 'http://www.ccgp-ningbo.gov.cn/project/'
        self.saveinfo(tables,webh)
        
        return True
        
    '''
    Function:4-单一来源公示,5-需求征求意见
    args:类型编号
    '''
    def forfiv(self,NoticeType):
        searchurl = 'http://www.ccgp-ningbo.gov.cn/Project/DemandNotice.aspx'#搜索的url
        params = {
            "NoticeType":str(NoticeType),
            "NoticeTitle":self.searchword
        }
        content = self.requrl(searchurl,params)
        # 使用beautiful解析网页
        soup = BeautifulSoup(content,'html.parser')
        tables = soup.find_all(id="ctl00_ContentPlaceHolder3_gdvDemandNotice")#table
        webh = 'http://www.ccgp-ningbo.gov.cn/Project/'
        self.saveinfo(tables,webh)

        return True

    '''6-其他信息'''
    def sixinfo(self):
        searchurl = "http://www.ccgp-ningbo.gov.cn/sousuo.aspx"
        params = {
            "SearchName":self.searchword
        }
        content = self.requrl(searchurl,params)
        # 使用beautiful解析网页
        soup = BeautifulSoup(content,'html.parser')
        tables = soup.find_all(id="ctl00_ContentPlaceHolder2_SearchContentsList1_dtlContents")
        if len(tables)>0:
            aable = tables[0].find_all('td')
            for ai in xrange(len(aable)):
                aaa = ''
                try:
                    href = aable[ai].a['href']#链接
                    txts = aable[ai].a.b.font.get_text("")#公告名称
                except Exception as e:
                    aaa = '2'
                    pass
                infos = {}#存放公告信息
                if aaa!='2':
                    infos['title'] = txts
                    infos['url'] = 'http://www.ccgp-ningbo.gov.cn/'+href
                    infos['updatetime'] = datetime.datetime.strptime(time.strftime('%Y-%m-%d'),'%Y-%m-%d')#当前时间
                    self.updates.append(infos)#把更新的信息放进infos
                    self.mongos.save(self.indexurl,self.updates)#保存进mongodb
        return True


def main():
    cra = Crawler()
    cra(0,u'智慧')

if __name__ == '__main__':
    main()

