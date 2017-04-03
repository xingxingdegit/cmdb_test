# all the imports
#--*-- coding:utf-8 --*--

import os
import psycopg2
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash,make_response
from config import *
import time
from source import check

app = Flask(__name__)
app.config.from_object(config)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.before_request
def before_request():
    g.db = db.connect_db()

@app.teardown_request
def teardown_request(show_entries):
    g.db.close()
#def teardown_request(exception):
@app.route('/static/<filename>')
def static_(filename):
    with open('static/' + filename) as fd:
         resp = make_response(fd.read())
         resp.content_type = 'text/css'
    return resp

@app.route('/')
def index():
    name = request.cookies.get('name')
    if check.check_login(name,session):
        frame_id = request.args.get('frame_id')
        return render_template('index.html',username=name,status=u'已登录',frame_id=frame_id)
    return redirect(url_for('login'))
        
@app.route('/host',methods=['GET','POST'])
def host():
    name = request.cookies.get('name')
    if not check.check_login(name,session):
        return redirect(url_for('login'))
    if request.method == 'GET':
        try:
            cur = g.db.cursor()
            cur.execute(r'select id,hostname,ip1,ip2,ip3,ip4,ip5,ip6,item,service,port,admin,phone,motor,cabinet,pos,status from dm_host limit 100')
        except Exception,err:
            return err.message
        else:
            host_item = [dict(id=row[0],hostname=row[1],ip=[ip for ip in row[2:8] if ip and ip.strip()],item=row[8],service=row[9],port=row[10],admin=row[11],phone=row[12],motor=row[13],cabinet=row[14],pos=row[15],status=row[16]) for row in cur.fetchall()]
#            abort(401)
            return render_template('host.html', host_item=host_item)
    else:
        try:
            cur = g.db.cursor()
            data = dict(request.form.items())
                
            sql = r"insert into dm_host(hostname,item,service,port,admin,phone,motor,cabinet,pos,status"
            value = u"VALUES(%(hostname)s,%(item)s,%(service)s,%(port)s,%(admin)s,%(phone)s,%(motor)s,%(cabinet)s,%(pos)s,%(status)s"
            for ip,num in zip(data['ip'].split(','),(1,2,3,4,5,6)):
                col = 'ip{}'.format(num)
                data[col] = ip
                sql = sql + (',' + col)
                value = value + (',' + '%(' + col + ')s')
            sql = sql + ')' + value +')'

            cur.execute(sql,data)
            g.db.commit()
        except Exception,err:
            info = err.message
            if 'already exists' in info:
                info = u'主机已存在, 创建失败'
            elif 'is not present in table' in info:
                info = u'机房或机柜不存在, 创建失败'

        else: info = u'创建成功'
      #  return redirect(url_for('motor'))
        return render_template('host.html',info=info,hostname=request.form.get('hostname'))

@app.route('/motor',methods=['GET','POST'])
def motor():
    name = request.cookies.get('name')
    if not check.check_login(name,session):
        return redirect(url_for('login'))
    if request.method == 'GET':
        try:
            cur = g.db.cursor()
            cur.execute('select id,motor,address,admin,phone from dm_motor limit 100')
            all_data = cur.fetchall()
            cur.execute(r'select motor,count(*) from dm_host group by motor')
            motor_host_num = dict(cur.fetchall())
        except Exception,err:
            g.db.close()
            return err.message
        else:
            motor_item = [dict(id=row[0],motor=row[1],address=row[2],admin=row[3],phone=row[4],number=motor_host_num.get(row[1],0)) for row in all_data]
            return render_template('motor.html', motor_item=motor_item)
    else:
        try:
            cur = g.db.cursor()
            sql = r"insert into dm_motor(motor,address,admin,phone)values(%(motor)s,%(address)s,%(admin)s,%(phone)s)"
            cur.execute(sql,request.form)
            g.db.commit()
        except Exception,err:
            info = err.message
            if 'already exists' in info:
                info = u'机房已存在'
        else: info = u'创建成功'
      #  return redirect(url_for('motor'))
        return render_template('motor.html',info=info,motor=request.form.get('motor'))

@app.route('/cabinet',methods=['GET','POST'])
def cabinet():
    name = request.cookies.get('name')
    if not check.check_login(name,session):
        return redirect(url_for('login'))
    if request.method == 'GET':
        try:
            cur = g.db.cursor()
            cur.execute('select id,motor,cabinet,row,col,height from dm_cabinet limit 100')
        except Exception,err:
            g.db.close()
            return err.message
        else:
            cabinet_item = [dict(id=row[0],motor=row[1],cabinet=row[2],row=row[3],col=row[4],height=row[5]) for row in cur.fetchall()]
            return render_template('cabinet.html', cabinet_item=cabinet_item)
    else:
        try:
            cur = g.db.cursor()
            sql = r"insert into dm_cabinet(motor,cabinet,row,col,height)values(%(motor)s,%(cabinet)s,%(row)s,%(col)s,%(height)s)"
            cur.execute(sql,request.form)
            g.db.commit()
        except Exception,err:
            info = err.message
            if "is not present in table" in info:
                info = u'机房不存在'
            elif 'already exists' in info:
                info = u'机房中此机柜已存在'
        else: info = u'创建成功'
      #  return redirect(url_for('motor'))
        return render_template('cabinet.html',info=info,motor=request.form.get('cabinet'))


@app.route('/del',methods=['POST'])
def del_entry():
    if not session.get(request.cookies['name']):
        return redirect(url_for('login'))
    try:
        cur = g.db.cursor()
        sql = u"delete from entries where id = %s" % request.form['tid']
        cur.execute(sql)
        g.db.commit()
    except Exception,err:
        return err.message
    return redirect(url_for('show_entries'))

@app.route('/login',methods=['GET','POST'])
def login():
    info = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        decide,info = check.login(username,password)

        if decide:
            session[username] = True
            response = make_response()
            response.set_cookie('name',username)
            response.location = url_for('index')
            response.status_code = 302
    #            response.set_data(render_template('login.html',error=error))
            return response
#            return redirect(url_for('show_entries'))
    return render_template('login.html',info=info)

@app.route('/logout')
def logout():
    session.pop(request.cookies['name'],None)
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
            dateline = int(time.time())
            date_str = time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(dateline))
            data = dict(request.form.items())
            data['create_date'] = dateline
            data['create_date_str'] = date_str
            data['status'] = 'ON'
            data['level'] = 1
            sql = r"insert into dm_user(username,password,section,phone,email,create_date,create_date_str,status,level)values(%(username)s,%(password)s,%(section)s,%(phone)s,%(email)s,%(create_date)s,%(create_date_str)s,%(status)s,%(level)s)"
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
#    app.run('0.0.0.0',8000)
    app.run()
