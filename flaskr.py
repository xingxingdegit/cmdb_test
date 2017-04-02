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
            cur.execute('select hid,hostname,ip1,ip2,ip3,ip4,ip5,ip6,item,status,service,admin,phone from dm_host limit 100')
            all_data = cur.fetchall()
        except Exception,err:
            return err.message
        else:
            host_item = [dict(hid=row[0],hostname=row[1],ip=[ip for ip in row[2:8] if ip.strip()],item=row[8],status=row[9],service=row[10],admin=row[11],phone=row[12]) for row in cur.fetchall()]
#            abort(401)
            return render_template('host.html', host_item=host_item)
    else:
        pass

@app.route('/motor',methods=['GET','POST'])
def motor():
    name = request.cookies.get('name')
    if not check.check_login(name,session):
        return redirect(url_for('login'))
    if request.method == 'GET':
        try:
            cur = g.db.cursor()
            cur.execute('select id,motor,address,admin,phone from dm_motor limit 100')
        except Exception,err:
            g.db.close()
        else:
            motor_item = [dict(id=row[0],motor=row[1],address=row[2],admin=row[3],phone=row[4]) for row in cur.fetchall()]
            return render_template('motor.html', motor_item=motor_item)
    else:
        try:
            cur = g.db.cursor()
            sql = r"insert into dm_motor(motor,address,admin,phone)values(%(motor)s,%(address)s,%(admin)s,%(phone)s)"
            cur.execute(sql,request.form)
            g.db.commit()
        except Exception,err:
            info = err.message
            if 'already exists' in err.message:
                info = u'机房已存在'
        else: info = u'创建成功'
      #  return redirect(url_for('motor'))
        return render_template('motor.html',info=info,motor=request.form.get('motor'))


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
