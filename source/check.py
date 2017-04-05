#!/usr/bin/env python
#--*-- coding:utf-8 --*--
#
import time
from config import config

def check_login(name,conn,ip):
    if name:
       pre = config.PREFIX
       nowtime = int(time.time())
       user_data = conn.hgetall(pre+name)
       try:
           if user_data['active'] == 'online':
               if (nowtime - int(user_data.get('lasttime'))) <= 1800:
                   if user_data['lastip'] == ip:
                       conn.hset(name,'lasttime',nowtime)
                       return True
       except:
           return False
    return False

def login(username,password,conn):
    info = u'登录成功'
    try:
        cur = conn.cursor()
        sql = r"select username,password,status from dm_user WHERE username = '%s'" % username
        cur.execute(sql)
        user_data = cur.fetchone()
    except Exception,err:
        conn.close()
        if "does not exist" in err.message:
            return False,u'用户不存在'
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

