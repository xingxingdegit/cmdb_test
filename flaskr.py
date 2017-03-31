# all the imports
#--*-- coding:utf-8 --*--
import os
import psycopg2
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from config import *

app = Flask(__name__)
app.config.from_object(config)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.before_request
def before_request():
    g.db = db.connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/',methods=['GET','POST'])
def show_entries():
    if request.method == 'POST':
        return redirect(url_for('login'))
    try:
        cur = g.db.cursor()
        cur.execute('select title,text from entries order by id desc')
#        return str(cur.fetchall())
    except Exception,err:
        return 'error'
    entries = [dict(title=row[0],text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', **entries[-1])

@app.route('/add',methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    cur = g.db.cursor()
    cur.execute('insert into entries(title,text) values (%s,%s)',[request.form['title'],request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] not in app.config['USERNAME']:
#            return str((request.form['username'],app.config['USERNAME'])
            error = u'用户名错误'
        elif request.form['password'] != app.config['PASSWORD']:
            error = u'密码错误'
        else:
#            session['logged_in'] = True
#            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html',error=error)







if __name__ == '__main__':
    app.run('0.0.0.0',8000)
