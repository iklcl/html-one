#engcoding:utf-8
from flask_script import Manager
from test4 import  app
manager=Manager(app)



@manager.command()
def runderver():
    print '服务器跑起来了！！！'


if __name__=='__main__':
    manager.run()
