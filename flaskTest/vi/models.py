#encoding:utf-8
#文件名称:models.py
#作者：huanghong
#创建日期：2017-1-20
from exts import db
from datetime import  datetime
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.INTEGER,primary_key=True)
    username = db.Column(db.String(100),nullable=False)
    telephone = db.Column(db.String(11),nullable=False)
    password = db.Column(db.String(100),nullable=False)


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.INTEGER,primary_key=True)
    title = db.Column(db.String(100),nullable=False)#项目名
    content = db.Column(db.Text,nullable=False)#项目内容
    url = db.Column(db.Text,nullable=False)
    nub = db.Column(db.INTEGER,nullable=False)#优先级
    beizhu = db.Column(db.Text)#备注
    zhuangtai = db.Column(db.String(100))#状态
    filename = db.Column(db.String(100))#附件文件夹名
    data_name = db.Column(db.String(100))#附件文件名
    custom =db.Column(db.String(100),default='no') #是否自定义部署
    svnUrl = db.Column(db.String(100)) #svn地址(存储base64加密后的数据)
    progress = db.Column(db.String(100))#任务处理进度
    task = db.Column(db.String(100))#任务名
    create_time=db.Column(db.DateTime,default=datetime.now)#项目创建时间
    author_id = db.Column(db.INTEGER,db.ForeignKey('user.id'))#用户id
    author = db.relationship('User',backref=db.backref('questions'))


class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.INTEGER,primary_key=True)
    name = db.Column(db.String(100),nullable=False)#附件保存中文名
    content = db.Column(db.String(100),nullable=False)#附件保存名
    filename_id=db.Column(db.INTEGER,db.ForeignKey('question.id'))
    question = db.relationship('Question',backref=db.backref('file'))


# 另外创建一个轮询任务表whiletask，字段如下
# class Whiletask(db.Model):
#     __tablename__ = 'whiletask'
#     id = db.Column(db.INTEGER,primary_key=True)#主键索引       
#     status = db.Column(db.String(100))#状态，是否正在运行(无状态,休眠，等待，正在运行)/(null,sleep,pending,running)
#     projectid = db.Column(db.INTEGER,db.ForeignKey('question.id'))#在项目表中的id（唯一索引）
#     mode= db.Column(db.String(100))#运行模式二选一("timer","interval")
#     interval =db.Column(db.String(100)) #间隔
#     nexttime = db.Column(db.DateTime)#下次运行时间
#     lastRunTime = db.Column(db.DateTime)#上次运行时间
#     question = db.relationship('Question',backref=db.backref('whiletask'))
