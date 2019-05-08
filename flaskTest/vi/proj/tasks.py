#-*- coding:utf-8 -*-
from __future__ import absolute_import
from proj.celery import app
import time
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import logging



@app.task
def add(x,y):
    print '%s + %s = %s'%(x,y,x+y)
    return x+y

@app.task
def msg(data):
    print data

#桥接调度器与任务队列
def go(t):
    #异步任务
    msg.delay(t)

class Timer(object):
    '''定时调度配置模块
    BackgroundScheduler为后台运行调度方式
    SQLAlchemyJobStore配置sqlite数据库存储调度任务
    '''
    def __init__(self):
        jobstores = {
            #'mongo': MongoDBJobStore(),
            'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
        }
        executors = {
            'default': ThreadPoolExecutor(20), #线程数
            'processpool': ProcessPoolExecutor(5) #进程数
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 4
        }
        self.scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
        self.scheduler.start()


class Scheduler(object):
    '''调度器
    封装APScheduler的调度函数,修改时区为中国上海
    '''
    __instance = None
    def __new__(cls,*args,**kwargs):
        if cls.__instance==None:
            cls.__instance = object.__new__(cls,*args,**kwargs)
        return cls.__instance

    def __init__(self):
        self.__task = Timer()
        self.scheduler = self.__task.scheduler
        self.scheduler.add_listener(self.err_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self.scheduler._logger = logging
        self.msg = go
    
    def err_listener(event):
        if event.exception:
            logging.error(u'任务添加失败')

    def add_cron_job(self,*args,**kwargs):
        """添加cron定时调度,举例
        参数说明
        (int|str) 表示参数既可以是int类型，也可以是str类型
        (datetime | str) 表示参数既可以是datetime类型，也可以是str类型

        year (int|str) – 4-digit year -（表示四位数的年份，如2008年）
        month (int|str) – month (1-12) -（表示取值范围为1-12月）
        day (int|str) – day of the (1-31) -（表示取值范围为1-31日）
        week (int|str) – ISO week (1-53) -（格里历2006年12月31日可以写成2006年-W52-7（扩展形式）或2006W527（紧凑形式））
        day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun) - （表示一周中的第几天，既可以用0-6表示也可以用其英语缩写表示）
        hour (int|str) – hour (0-23) - （表示取值范围为0-23时）
        minute (int|str) – minute (0-59) - （表示取值范围为0-59分）
        second (int|str) – second (0-59) - （表示取值范围为0-59秒）
        start_date (datetime|str) – earliest possible date/time to trigger on (inclusive) - （表示开始时间）
        end_date (datetime|str) – latest possible date/time to trigger on (inclusive) - （表示结束时间）
        timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone) -（表示时区取值）
        
        举例
        #表示2017年3月22日17时19分07秒执行该程序
        sched.add_job(my_job, 'cron', year=2017,month = 03,day = 22,hour = 17,minute = 19,second = 07)
         
        #表示任务在6,7,8,11,12月份的第三个星期五的00:00,01:00,02:00,03:00 执行该程序
        sched.add_job(my_job, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')
         
        #表示从星期一到星期五5:30（AM）直到2014-05-30 00:00:00
        sched.add_job(my_job(), 'cron', day_of_week='mon-fri', hour=5, minute=30,end_date='2014-05-30')
         
        #表示每5秒执行该程序一次，相当于interval 间隔调度中seconds = 5
        sched.add_job(my_job, 'cron',second = '*/5')

        参数的取值格式：
        Expression    Field    Description
        *    any    Fire on every value
        */a    any    Fire every a values, starting from the minimum
        a-b    any    Fire on any value within the a-b range (a must be smaller than b)
        a-b/c    any    Fire every c values within the a-b range
        xth y    day    Fire on the x -th occurrence of weekday y within the month
        last x    day    Fire on the last occurrence of weekday x within the month
        last    day    Fire on the last day within the month
        x,y,z    any    Fire on any matching expression; can combine any number of any of the above expressions
        """
        kwargs.update({"timezone":"Asia/Shanghai"})
        pid = self.scheduler.add_job(self.msg,'cron',*args,**kwargs)
        return pid.id

    def add_interval_job(self,*args,**kwargs):
        """添加interval 间隔调度（每隔多久执行
        参数说明
        weeks (int) – number of weeks to wait
        days (int) – number of days to wait
        hours (int) – number of hours to wait
        minutes (int) – number of minutes to wait
        seconds (int) – number of seconds to wait
        start_date (datetime|str) – starting point for the interval calculation
        end_date (datetime|str) – latest possible date/time to trigger on
        timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations
        举例
        #表示每隔3天17时19分07秒执行一次任务
        sched.add_job(my_job, 'interval',days = 03,hours = 17,minutes = 19,seconds = 07)
        """
        kwargs.update({"timezone":"Asia/Shanghai"})
        pid = self.scheduler.add_job(self.msg,'interval',*args,**kwargs)
        return pid.id

    def add_date_job(self,*args,**kwargs):
        """添加date 定时调度,run_date接收datetime对象作为时间(作业只会执行一次)
        参数说明
        run_date (datetime|str) – the date/time to run the job at  -（任务开始的时间）
        timezone (datetime.tzinfo|str) – time zone for run_date if it doesn’t have one already
        举例
        # The job will be executed on November 6th, 2009
        sched.add_job(my_job, 'date', run_date=date(2009, 11, 6), args=['text'])
        # The job will be executed on November 6th, 2009 at 16:30:05
        sched.add_job(my_job, 'date', run_date=datetime(2009, 11, 6, 16, 30, 5), args=['text'])
        """
        kwargs.update({"timezone":"Asia/Shanghai"})
        pid = self.scheduler.add_job(self.msg,'date',*args,**kwargs)
        return pid.id

    # def get_statu(self,idd):
    #     "根据任务id查看任务状态"
    #     return self.scheduler.get_job(idd).pending



def test():
    pass


if __name__ == '__main__':
    # print 'start...'
    test()


