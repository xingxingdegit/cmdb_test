# all the imports
#--*-- coding:utf-8 --*--

#import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash,make_response
from config import *
from source import *
import time,re

app = Flask(__name__)
app.config.from_object(config)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.before_request
def before_request():
    g.db = db_init.connect_db()
    g.redis = db_init.connect_redis()

@app.teardown_request
def teardown_request(exception):
    g.db.close()
#def teardown_request(exception):
@app.route('/static/<filename>')
def static_(filename):
    extname = filename.split('.')[1]
#    return str(extname)
    image = ['png','gif','jpg','jpeg','ico','bmp']
    text = ['html','htm','shtml','css','xml']
    application = ['js']
    if extname in image:
        if extname in ['jpg','jpeg']:
            content_type = 'image/jpeg'
        elif extname == 'ico':
            content_type = 'image/x-icon'
        else: content_type = 'image/' + extname
    elif extname in text:
        if extname in ['html','htm','shtml']:
            content_type = 'text/html'
        else: content_type = 'text/' + extname
    elif extname in application:
        content_type = 'application/javascript'
        
    with open('static/' + filename) as fd:
         resp = make_response(fd.read())
         resp.content_type=content_type
    return resp

@app.route('/')
def index():
    name = request.cookies.get('name')
    if check.check_login(name,g.redis,request.remote_addr):
        frame_id = request.args.get('frame_id')
        return render_template('index.html',username=name,status=u'已登录',frame_id=frame_id)
    return redirect(url_for('login'))
        
@app.route('/host',methods=['GET','POST'])
def host():
#查看主机列表信息，分页显示
    name = request.cookies.get('name')
    if not check.check_login(name,g.redis,request.remote_addr):
        return redirect(url_for('login'))
    if request.method == 'GET':

        host_item,pages = db_sql.select_page_host(g.db,request.args.get('page',1))
        if host_item != False:
            return render_template('host.html', host_item=host_item,pages=int(pages))
        else:
            return str(pages)
#            abort(401)
    else:
        host_item,pages = db_sql.select_page(g.db,request.form('page',1))
        if host_item:
            return render_template('host.html', host_item=host_item,pages=pages)
        else:
            return pages

@app.route("/add/<filename>",methods=['GET','POST'])
def add_item(filename):
    #添加主机，机柜或机房。
    name = request.cookies.get('name')
    if not check.check_login(name,g.redis,request.remote_addr):
        return redirect(url_for('login'))
    if request.method == 'POST':
        if filename == 'host.html':
            data = dict(request.form.items())
            status,info = db_sql.insert_all_host(g.db,data)
            return render_template(url_for('add_item',filename=filename),status=status,info=info)
    
        elif filename == 'motor.html':
            data = dict(request.form.items())
            status,info = db_sql.insert_all_motor(g.db,data)
            return render_template(url_for('add_item',filename=filename),status=status,info=info)
    
        elif filename == 'cabinet.html':
            data = dict(request.form.items())
            status,info = db_sql.insert_all_cabinet(g.db,data)
            return render_template(url_for('add_item',filename=filename),status=status,info=info)
        else:
            return u'添加的是不存在的项目'

    else:
        if filename in ['host.html','motor.html','cabinet.html']:
            return render_template(url_for('add_item',filename=filename))
        else:
            return u'打开的是不存在的项目'
        
    

@app.route("/host/view",methods=['GET','POST'])
def host_view():
#编辑
    pass

@app.route('/motor',methods=['GET','POST'])
def motor():
#查看机房列表信息，分页显示
    name = request.cookies.get('name')
    if not check.check_login(name,g.redis,request.remote_addr):
        return redirect(url_for('login'))
    if request.method == 'GET':
        motor_item,pages = db_sql.select_page_motor(g.db,request.args.get('page',1))
        if motor_item != False:
            return render_template('motor.html', motor_item=motor_item,pages=int(pages))
        else:
            return str(pages)
#            abort(401)
    else:
        motor_item,pages = db_sql.select_page(g.db,request.form('page',1))
        if host_item:
            return render_template('motor.html', motor_item=motor_item,pages=pages)
        else:
            return pages


@app.route('/cabinet',methods=['GET','POST'])
def cabinet():
#查看机柜列表信息，分页显示
    name = request.cookies.get('name')
    if not check.check_login(name,g.redis,request.remote_addr):
        return redirect(url_for('login'))
    if request.method == 'GET':
        cabinet_item,pages = db_sql.select_page_cabinet(g.db,request.args.get('page',1))
        if cabinet_item != False:
            return render_template('cabinet.html', cabinet_item=cabinet_item,pages=int(pages))
        else:
            return str(pages)
#            abort(401)
    else:
        cabinet_item,pages = db_sql.select_page_cabinet(g.db,request.form('page',1))
        if host_item:
            return render_template('cabinet.html', cabinet_item=cabinet_item,pages=pages)
        else:
            return pages


@app.route('/login',methods=['GET','POST'])
def login():
    info = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        decide,info = check.login(username,password,g.db)

        if decide:
            nowtime = int(time.time())
            ip = request.remote_addr
            try:
                pre = app.config['PREFIX']
                g.redis.hmset(pre + username,{'active':'online','lasttime':nowtime,'lastip':ip})
            except Exception,err:
                return err.message
            
            response = make_response()
            response.set_cookie('name',username)
            response.location = url_for('index')
            response.status_code = 302
            return response
    return render_template('login.html',info=info)

@app.route('/logout')
def logout():
    pre = app.config['PREFIX']
    username = request.cookies.get('name')
    g.redis.hset(pre+username,'active','offline')
    
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/logup',methods=['GET','POST'])
def logup():
    info = ''
    if request.method == 'POST':
        if not (request.form['username'] and request.form['password'] and request.form['password_again']):
            if not request.form['username']:
                info = u'用户名为空'
            else:
                info = u'密码为空'
        elif request.form['password'] != request.form['password_again']:
            info = u'密码不匹配'
        else:
            dateline,date_str = time_format.time_now()
            data = dict(request.form.items())
            data['dateline'] = dateline
            data['date_str'] = date_str
            data['status'] = 'ON'
            data['level'] = 1
            sql = r"insert into dm_user(username,password,section,phone,email,dateline,date_str,status,level)values(%(username)s,%(password)s,%(section)s,%(phone)s,%(email)s,%(dateline)s,%(date_str)s,%(status)s,%(level)s)"
            try:
                cur = g.db.cursor()
                cur.execute(sql,data)
                g.db.commit()
            except Exception,err:
                if 'already exists' in err.message:
                    info = u'用户已存在'
                else: info = err.message
            else: 
                info = data["username"] + u'创建成功'

    return render_template('logup.html',info=info)

if __name__ == '__main__':
    app.run('0.0.0.0',8000)
#    app.run()
