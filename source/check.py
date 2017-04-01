#!/usr/bin/env python
#--*-- coding:utf-8 --*--
#
from config import db

def check_status():
    pass

def login(username,password):
    info = u'登录成功'
    try:
        conn = db.connect_db()
        cur = conn.cursor()
        sql = r"select username,password,status from dm_user WHERE username = '%s'" % username
        cur.execute(sql)
        user_data = cur.fetchone()
    except Exception,err:
        return False,err.message
    finally:
       conn.close()
    if not user_data:
        info = u'用户名错误'
    elif user_data[2] == 'OFF':
        info = u'用户被禁用'
    elif password != user_data[1]:
        info = u'密码错误'
    else:
        return True,info
    return False,info

