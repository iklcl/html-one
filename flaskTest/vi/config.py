#encoding:utf-8
#文件名称:config.py
#作者：huanghong
#创建日期：2017-1-20
# dialect+driver://username:password@host:port/database
import os
USERNAME='root'
PASSWORD='123456'
HOST='127.0.0.1'
PORT='3306'
DATABASE='db_demo1'
DB_URI = "mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8".format(USERNAME,PASSWORD,HOST
                                                 ,PORT,DATABASE)

SQLALCHEMY_DATABASE_URI=DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG=True

SECRET_KEY = os.urandom(24)