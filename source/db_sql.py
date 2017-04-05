#!/usr/bin/env python
#--*-- coding:utf-8 --*--
#
import time,math
from config import config

def select_page_host(conn,page):
    #根据请求页数，获取数据，并返回数据数典和总的页数。 如果有问题，则返回 False和错误信息。
    try:
        cur = conn.cursor()
        cur.execute(r'select count(hid) from dm_host')
    except Exception,err:
        return False,err.message
    try:
        page = int(page)
    except: page = 1

    rows = cur.fetchone()[0]
    page_per = config.PAGE_PER
    pages = math.ceil(rows / float(page_per))
#three select style, first :if range of part from top is nearly. second: if range of part from end is nearly.  third : 最后一页, 是否正好一页.     
    if page == 1:
        sql = u'select hid,hostname,service_ip,data_ip,monitor_ip,item,service,system,admin,phone,status,date_str from dm_host order by dateline desc limit %d' % page_per

    elif page <= (rows / 2):
        first_select = page_per * (page + 1)
        sql = u'select hid,hostname,service_ip,data_ip,monitor_ip,item,service,system,admin,phone,status,date_str from (select * from (select * from dm_host order by dateline desc limit %d;) order by dateline limit %d;) order by dateline desc' % (first_select,page_per)
    elif page == pages:
        end_page = rows % page_per
        if end_page:
            sql = u'select hid,hostname,service_ip,data_ip,monitor_ip,item,service,system,admin,phone,status,date_str from dm_host order by dateline desc limit %d' % (end_page)
        else:
            sql = u'select hid,hostname,service_ip,data_ip,monitor_ip,item,service,system,admin,phone,status,date_str from dm_host order by dateline desc limit %d' % (page_per)
    else:
        end_page = rows % page_per
        page = pages - page
        if end_page:
            first_select = page_per * (page) + end_page
        else:
            first_select = page_per * (page + 1)
        first_select = page_per * (page + 1)
        sql = u'select hid,hostname,service_ip,data_ip,monitor_ip,item,service,system,admin,phone,status,date_str from (select * from dm_host order by dateline limit %d;) order by dateline desc limit %d)' % (first_select,page_per)
        
    try:
        cur.execute(sql)
        data = cur.fetchall()
        id = 1
        data_list = [dict(id=id+1,hid=row[0],hostname=row[1],service_ip=row[2],data_ip=row[3],monitor_ip=row[4],item=row[5],service=row[6],system=row[7],admin=row[8],phone=row[9],status=row[10],data_str=row[11]) for row in data]
    except Exception,err:
        return False,err.message
    else:
        return data_list,pages

def select_page_cabinet(conn,page):
    #根据请求页数，获取数据，并返回数据数典和总的页数。 如果有问题，则返回 False和错误信息。
    try:
        cur = conn.cursor()
        cur.execute(r'select count(cid) from dm_host')
    except Exception,err:
        return False,err.message
    try:
        page = int(page)
    except: page = 1

    rows = cur.fetchone()[0]
    page_per = config.PAGE_PER
    pages = math.ceil(rows / float(page_per))
#three select style, first :if range of part from top is nearly. second: if range of part from end is nearly.  third : 最后一页, 是否正好一页.     
    if page == 1:
        sql = u'select cid,motor,cabinet,row,col,height,dateline,date_str from dm_cabinet order by dateline desc limit %d' % page_per

    elif page <= (rows / 2):
        first_select = page_per * (page + 1)
        sql = u'select cid,motor,cabinet,row,col,height,dateline,date_str from (select * from (select * from dm_cabinet order by dateline desc limit %d;) order by dateline limit %d;) order by dateline desc' % (first_select,page_per)
    elif page == pages:
        end_page = rows % page_per
        if end_page:
            sql = u'select cid,motor,cabinet,row,col,height,dateline,date_str from dm_cabinet order by dateline desc limit %d' % (end_page)
        else:
            sql = u'select cid,motor,cabinet,row,col,height,dateline,date_str from dm_cabinet order by dateline desc limit %d' % (page_per)
    else:
        end_page = rows % page_per
        page = pages - page
        if end_page:
            first_select = page_per * (page) + end_page
        else:
            first_select = page_per * (page + 1)
        first_select = page_per * (page + 1)
        sql = u'select cid,motor,cabinet,row,col,height,dateline,date_str from (select * from dm_cabinet order by dateline limit %d;) order by dateline desc limit %d)' % (first_select,page_per)
        
    try:
        cur.execute(sql)
        data = cur.fetchall()
        id = 1
        data_list = [dict(id=id+1,cid=row[0],motor=row[1],cabinet=row[2],row=row[3],col=row[4],height=row[5],date_str=row[6]) for row in data]
    except Exception,err:
        return False,err.message
    else:
        return data_list,pages

def select_page_motor(conn,page):
    #根据请求页数，获取数据，并返回数据数典和总的页数。 如果有问题，则返回 False和错误信息。
    try:
        cur = conn.cursor()
        cur.execute(r'select count(mid) from dm_host')
    except Exception,err:
        return False,err.message
    try:
        page = int(page)
    except: page = 1

    rows = cur.fetchone()[0]
    page_per = config.PAGE_PER
    pages = math.ceil(rows / float(page_per))
#three select style, first :if range of part from top is nearly. second: if range of part from end is nearly.  third : 最后一页, 是否正好一页.     
    if page == 1:
        sql = u'select mid,motor,address,admin,phone,date_str from dm_motor order by dateline desc limit %d' % page_per

    elif page <= (rows / 2):
        first_select = page_per * (page + 1)
        sql = u'select mid,motor,address,admin,phone,date_str from (select * from (select * from dm_motor order by dateline desc limit %d;) order by dateline limit %d;) order by dateline desc' % (first_select,page_per)
    elif page == pages:
        end_page = rows % page_per
        if end_page:
            sql = u'select mid,motor,address,admin,phone,date_str from dm_motor order by dateline desc limit %d' % (end_page)
        else:
            sql = u'select mid,motor,address,admin,phone,date_str from dm_motor order by dateline desc limit %d' % (page_per)
    else:
        end_page = rows % page_per
        page = pages - page
        if end_page:
            first_select = page_per * (page) + end_page
        else:
            first_select = page_per * (page + 1)
        first_select = page_per * (page + 1)
        sql = u'select mid,motor,address,admin,phone,date_str from (select * from dm_motor order by dateline limit %d;) order by dateline desc limit %d)' % (first_select,page_per)
        
    try:
        cur.execute(sql)
        data = cur.fetchall()
        id = 1
        data_list = [dict(id=id+1,hid=row[0],hostname=row[1],service_ip=row[2],data_ip=row[3],monitor_ip=row[4],item=row[5],service=row[6],system=row[7],admin=row[8],phone=row[9],status=row[10],data_str=row[11]) for row in data]
    except Exception,err:
        return False,err.message
    else:
        return data_list,pages

def sql_filter(data,table_name,op='insert'):
    if op.lower() == 'insert':
        sql = 'insert into ' + table_name + '('
        value = 'values('

    for key in dict_data:
        if dict_data[key].isspace():
            del dict_data[key]
    for key in dict_data:
        sql = sql + key + ','
        value = value + '%(' + key + ')' + ','

    return sql.strip(',') + ')' + value.strip(',') + ')'
    
