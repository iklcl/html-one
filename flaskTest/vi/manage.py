#encoding:utf-8
#文件名称:manage.py
#作者：huanghong
#创建日期：2017-1-20

from flask_script import  Manager
from flask_migrate import  Migrate,MigrateCommand
from test4 import app
from exts import  db
import config
from models import User,Question
manager=Manager(app)
app.config.from_object(config)
db.init_app(app)

migrate = Migrate(app,db)



manager.add_command('db',MigrateCommand)

if __name__ =="__main__":
    manager.run()
 