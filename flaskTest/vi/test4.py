#encoding:utf-8
#文件名称:test4.py
#作者：huanghong
#创建日期：2017-1-20
from flask import Flask,render_template,request,redirect,url_for,send_from_directory,session,abort,jsonify,make_response
import config
from exts import db
from models import User,Question,File
import flask
from functools import  wraps
from sqlalchemy import or_
import os
import json
from werkzeug import secure_filename
from pypinyin import lazy_pinyin
import time
import hashlib,shutil
import sys
import logging
import datetime
# from proj.tasks import Scheduler
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datafmt='%a, %d %b %Y %H:%M:%S',
    filename='flask.log',
    filemode='a')

reload(sys)
sys.setdefaultencoding('utf-8')  


ALLOWED_EXTENSIONS = set(['db', 'csv', 'py','jpg','rar','txt','xls','doc','zip','pdf','png','xlsx','docx',''])
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


path3=os.path.join(os.getcwd(),'data')
# path4=os.path.join(os.getcwd(),'folder')
# app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(),'file')
#登入限制装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper
#首页路由
@app.route('/')
def index():
    context={
            'questions':Question.query.order_by('-create_time').all(),
        } 
    # if len(args)!=0:
    #     context['judge_resout']=args[0]
    return render_template('index.html',**context)





@app.route('/<finish>')
def return_index(finish):
    context={
            'questions':Question.query.order_by('-create_time').all(),
        } 
    # if len(args)!=0:
    context['judge_resout']=finish
    return render_template('index.html',**context)

#登入页面
@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method =='GET':
        return  render_template('login.html')
    else:
        username= request.form.get('telephone')
        password = request.form.get('password')

        user =User.query.filter(User.username==username,User.password==password).first()
        if user:
            session['user_id']=user.id
            session.permanent = True
            return  flask.redirect(flask.url_for('index'))
        else:
            return u'密码错误'

#注册登入
@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user =User.query.filter(User.telephone ==telephone).first()
        if user:
            return 'no'
        else:
            if password1!=password2:
                return 'no'
            else:
                user=User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                return  redirect(url_for('login'))


#注销
@app.route('/logout/',methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))



#全局收索session_id
@app.context_processor
def my_context_processor():
    user_id=session.get('user_id')
    if user_id:
        user=User.query.filter(User.id==user_id).first()
        if user:
            return {'user':user}
    return {}



#添加项目
@app.route('/append/',methods=['GET','POST'])
def append():
    if request.method == 'GET':
        # file_names=hashlib.md5(str(time.time())).hexdigest()[:15]
        return render_template('append.html')
    else:
        title=request.form.get('title')
        content=request.form.get('content')
        url=request.form.get('url')
        if 'http' and '://' not in url:
            return '网址无效,请确认再添加！'
        nub=request.form.get('nub')
        filename='_'.join(lazy_pinyin(title))+hashlib.md5(str(time.time())).hexdigest()[:15]
        question = Question(title=title,content=content,url=url,nub=nub,filename=filename)
        db.session.add(question)
        db.session.commit()
        path_file=os.path.join('data',filename)#项目目录
        os.makedirs(path_file)
        datas_path=os.path.join(path_file,'datas')   #数据保存目录
        os.makedirs(datas_path)
        code_path=os.path.join(path_file,'code') #代码存放目录
        os.makedirs(code_path)
        directory_path=os.path.join(path_file,'directory') #字典文件存放目录
        os.makedirs(directory_path)
    
    return redirect(url_for('index'))

#上传页面
@app.route('/input/<question_id>')
def input(question_id):
    question_model=Question.query.filter(Question.id==question_id).first()
    filename=question_model.filename
    datafile=os.path.join(os.getcwd(),'data')
    path_file=os.path.join(datafile,filename)#项目目录
    directory_path=os.path.join(path_file,'directory') #字典文件存放目录
    filenames=os.walk(directory_path)
    for i in filenames:
        content=i[2]
    context={
            'content':content,
            }
    return render_template('input.html',question=question_model,**context)



#文件后缀
def allowed_file(filename):
    return '.' in filename and  filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    
#上传附件
@app.route('/add_file/<question_id>',methods=['GET','POST'])
def add_file(question_id):
    if request.method == 'POST':
        question_model=Question.query.filter(Question.id==question_id).first()
        file_data=question_model.filename
        path_file=os.path.join('data',file_data)
        directory_path=os.path.join(path_file,'directory') #字典文件存放目录
        
        file = request.files['file']
        if file :
            name = file.filename.split('.')[0:-1]
            ext = file.filename.split('.')[-1]
            filenames = '_'.join(lazy_pinyin(name)) + '.' + ext
            filename = secure_filename(filenames)
            file.save(os.path.join(directory_path, filename))#存储附件到字典文件夹
        files = File(name=file.filename,content=filename,filename_id=question_id)
        db.session.add(files)
        db.session.commit() 
    # return contents       
    return  redirect(url_for('input',question_id=question_id))




#删除附件
@app.route('/delete_file/<file_name>/<question_id>')
def delete_file(file_name,question_id):
    question_model=Question.query.filter(Question.id==question_id).first()
    file_data=question_model.filename#获取附件文件夹名称
    path_file=os.path.join('data',file_data)
    directory_path=os.path.join(path_file,'directory') #字典文件存放目录
    file_path = os.path.join(directory_path, file_name)#找到附件文件路径
    os.remove(file_path)
    file=File.query.filter(File.content==file_name).first()#删除该条数据名
    db.session.delete(file)
    db.session.commit()
    return  redirect(url_for('input',question_id=question_id))




#删除项目
@app.route('/delete_data/<question_id>')
@login_required
def delete_data(question_id):
    question=Question.query.filter(Question.id==question_id).first() 
    filename=question.filename
    file_path=os.path.join(path3,filename)
    if  os.path.exists(file_path):
        shutil.rmtree(file_path)#强行删除文件夹   
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('index'))



#项目页面
@app.route('/detail/<question_id>')
def detail(question_id):
    question_model=Question.query.filter(Question.id==question_id).first()
    filename=question_model.filename
    datafile=os.path.join(os.getcwd(),'data')
    datafile2=os.path.join(os.getcwd(),'folder')
    filenames=os.walk(os.path.join(datafile,filename))
    for i in filenames:
        content=i[2]
    context={
            'content':content
            }
    return render_template('detail.html',question=question_model,**context)




# #附件下载
@app.route("/download/<path:filename>/<filedata>",methods=['GET'])
def download(filename,filedata):
    if request.method=="GET":
        path_file=os.path.join('data',file_data)
        directory_path=os.path.join(path_file,'directory') #字典文件存放目录
        if os.path.isfile(os.path.join(directory_path, filename)):
            file=File.query.filter(File.content==filename).first()
            response = make_response(send_from_directory(directory_path,filename,as_attachment=True))
            response.headers["Content-Disposition"] = "attachment; filename={}".format(file.name)
            return response
        abort(404)


# 文件下载
@app.route("/download_data/<question_id>",methods=['GET'])
def download_data(question_id):
    "下载数据"
    question_model=Question.query.filter(Question.id==question_id).first()
    filename = question_model.filename
    title =  question_model.title
    saveInfo(filename,title)
    if os.path.isfile(os.path.join(os.getcwd(),'savefile.bat')):
        response = make_response(send_from_directory(os.getcwd(),'savefile.bat',as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format('savefile.bat')
        return response
    abort(404)
    # return redirect(url_for('index'))



# 服务器项目名称， 本地文件名称
def saveInfo(projectName,filename):
    # filename ='的都是vkvkn'
    filename = filename.encode('GB2312')
    batext = 'xcopy /e /y \\\\192.168.201.91\\share\\%s\\code D:\\copyfile\\%s\\\n@pause'%(projectName.encode('GB2312'),filename)
    with open(os.path.join(os.getcwd(),'savefile.bat'),'w') as f:
        f.write(batext)






#编辑项目
@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    question_id =request.form.get('question_id')
    questions = Question.query.filter(Question.id==question_id).first()
    beizhu = request.form.get('content')
    zhuangtai = request.form.get('zhuangtai')
    questions.beizhu=beizhu
    # questions.data_name=data_name
    questions.zhuangtai=zhuangtai
    user_id =session['user_id']
    user = User.query.filter(User.id == user_id).first()
    questions.author = user
    # db.session.add(answer)
    db.session.commit()
    return flask.redirect(flask.url_for('index'))


#搜索
@app.route('/search/')
def search():
    q = flask.request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q)))
    context = {
        'questions': questions
    }
    return flask.render_template('index.html',**context)  


#管理页面
@app.route('/question/')
def question():
    context={
        'questions':Question.query.order_by('-create_time').all()
    }
    return  render_template("question.html",**context)


#设置界面
@app.route('/whiletask/',methods=['POST'])
def whiletask():
        question_id=request.form.get('question_id')
        start_time=request.form.get('time')
        # year=request.form.get('year')
        weeks=request.form.get('month')
        days=request.form.get('day')
        hours=request.form.get('hours')
        minute=request.form.get('minute')
        second=request.form.get('second')
        end_time=request.form.get('end_time')
        mode=request.form.get('mode')
        user_id =session['user_id']
        user = User.query.filter(User.id == user_id).first()
        password = user.password
        username = user.username
        if len(start_time)==0:
            return '初始化时间有误'
        if end_time!='':
            end_time = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
        if start_time!='':
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
        data={
        'password':password,
        'username':username,
        'question_id':question_id,
        'weeks':weeks,
        'days':days,
        'hours':hours,
        'minute':minute,
        'second':second,
        'mode':mode,
        'end_time':end_time,
        'start_time':start_time
        }
        start_time+=datetime.timedelta(minutes=10)
        logging.info(data) 
        logging.info(start_time)
        logging.info(dir(start_time))
        return json.dumps(data)

            
def judge(question_id,data):
    "判断是否需要运行"
    question_model=Question.query.filter(Question.id==question_id).first()
    task_id=question_model.task
    svnUrl = question_model.svnUrl
    project_path = question_model.filename
    data['project_path'] = project_path
    if task_id:
        logging.info(task_id)
        # return json.dumps(data)
        judge_resout='任务已存在设定，如需更改请先手动重置!'

  
    else:
        task_id=addTask(data)
        question_model.task=task_id
        db.session.commit()

        judge_resout='任务设定成功!'

    return flask.redirect(flask.url_for('return_index',finish=judge_resout))      


#添加调度任务
def addTask(datas):
    """添加一个定时或者立即运行的项目,接收参数为(定时数据字典,项目数据字典)
    """
#     taskid = None
#     scheduler = Scheduler()
#     mode = datas.get('mode','') #获取运行模式
#     if 'interval' == mode:#如果为间隔模式则添加间隔任务
#         weeks = datas.get('weeks') #周数/星期数
#         days = datas.get('days') #日
#         hours = datas.get('hours') #小时
#         minutes = datas.get('minutes') #分钟
#         start_date = datas.get('start_time') #开始时间
#         end_date = datas.get('end_time') #结束时间
#         t = {"args":[proj]} #创建一个字典,初始化项目到字典中
#         if weeks:
#             t.update({"weeks":int(weeks)})
#         if days:
#             t.update({"days":int(days)})
#         if hours:
#             t.update({"hours":int(hours)})
#         if minutes:
#             t.udpate({"minutes":int(minutes)})
#         if start_date:
#             t.update({"start_date":start_date})
#         if end_date:
#             t.update({"end_date":end_date})
#         #如果字典key的数量大于1则表示可以启动任务（因为字典已经有一个key表示项目参数，那么如果还有其他参数则表示有定时参数，否则没有定时）
#         if len(t)>1:
#             taskid = scheduler.add_interval_job(**t)
#     elif 'timer' == mode:#如果为定时模式,则添加定时任务
#         run_date = datas.get('run_date')
#         t = {"args":[proj]} #创建一个字典,初始化项目到字典中
#         if run_date:
#             t.update({"run_date":run_date})
#         if len(t)>1:
#             taskid = scheduler.add_date_job(**t)
#     else:
#         raise ValueError("mode should be interval/timer")
    return datas['question_id']

def test_whaike_scheduler():
    addTask({"minutes":1},'test')

#任务运行
@app.route('/run/<question_id>')
def run(question_id):
    # project=Whiletask.query.filter(Whiletask.projectid==question_id).first()
    # status=project.mode
    # if status=='timer':
    return '运行模式%s'%question_id
    
@app.route('/remove/<question_id>')


# def return_index(args):
#     context={
#             'questions':Question.query.order_by('-create_time').all(),
#             'judge_resout':args
#         }
#     return render_template('index.html',**context)
        
def delete_task(question_id):
    "删除一个任务"
    question_model=Question.query.filter(Question.id==question_id).first()
    idd=question_model.task
    
    # scheduler = Scheduler()
    # scheduler.remove(idd)
    
    question_model.task=''
    db.session.commit()
    judge_resout='任务已重置!'
    return flask.redirect(flask.url_for('return_index',finish=judge_resout)) 


@app.route('/run_time/<question_id>')
def run_time(question_id):
    judge_resout='此任务运行时间：%s'%('dsdad')
    return flask.redirect(flask.url_for('return_index',finish=judge_resout)) 



if __name__ == '__main__':
    app.run(port=8000,debug=True)

    
