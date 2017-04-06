#!/usr/bin/env python
#--*-- coding:utf-8 --*--
#
import math,time_format
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
        data_list = []
        for row in data:
            data_list.append(dict(id=id,hid=row[0],hostname=row[1],service_ip=row[2],data_ip=row[3],monitor_ip=row[4],item=row[5],service=row[6],system=row[7],admin=row[8],phone=row[9],status=row[10],data_str=row[11]))
            id += 1

    except Exception,err:
        return False,err.message
    else:
        return data_list,pages

def select_page_cabinet(conn,page):
    #根据请求页数，获取数据，并返回数据数典和总的页数。 如果有问题，则返回 False和错误信息。
    try:
        cur = conn.cursor()
        cur.execute(r'select count(cid) from dm_cabinet')
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
        sql = u'select cid,motor,cabinet,row,col,height,date_str from dm_cabinet order by dateline desc limit %d' % page_per

    elif page <= (rows / 2):
        first_select = page_per * (page + 1)
        sql = u'select cid,motor,cabinet,row,col,height,date_str from (select * from (select * from dm_cabinet order by dateline desc limit %d;) order by dateline limit %d;) order by dateline desc' % (first_select,page_per)
    elif page == pages:
        end_page = rows % page_per
        if end_page:
            sql = u'select cid,motor,cabinet,row,col,height,date_str from dm_cabinet order by dateline desc limit %d' % (end_page)
        else:
            sql = u'select cid,motor,cabinet,row,col,height,date_str from dm_cabinet order by dateline desc limit %d' % (page_per)
    else:
        end_page = rows % page_per
        page = pages - page
        if end_page:
            first_select = page_per * (page) + end_page
        else:
            first_select = page_per * (page + 1)
        first_select = page_per * (page + 1)
        sql = u'select cid,motor,cabinet,row,col,height,date_str from (select * from dm_cabinet order by dateline limit %d;) order by dateline desc limit %d)' % (first_select,page_per)
        
    try:
        cur.execute(sql)
        data = cur.fetchall()
        id = 1
        data_list = []
        for row in data:
            data_list.append(dict(id=id,cid=row[0],motor=row[1],cabinet=row[2],row=row[3],col=row[4],height=row[5],date_str=row[6]))
            id += 1
    except Exception,err:
        return False,err.message
    else:
        return data_list,pages

def select_page_motor(conn,page):
    #根据请求页数，获取数据，并返回数据数典和总的页数。 如果有问题，则返回 False和错误信息。
    try:
        cur = conn.cursor()
        cur.execute(r'select count(mid) from dm_motor')
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
        sql = u'select mid,motor,motorname,address,admin,phone,create_date_str from dm_motor order by dateline desc limit %d' % page_per

    elif page <= (rows / 2):
        first_select = page_per * (page + 1)
        sql = u'select mid,motor,motorname,address,admin,phone,create_date_str from (select * from (select * from dm_motor order by dateline desc limit %d;) order by dateline limit %d;) order by dateline desc' % (first_select,page_per)
    elif page == pages:
        end_page = rows % page_per
        if end_page:
            sql = u'select mid,motor,motorname,address,admin,phone,create_date_str from dm_motor order by dateline desc limit %d' % (end_page)
        else:
            sql = u'select mid,motor,motorname,address,admin,phone,create_date_str from dm_motor order by dateline desc limit %d' % (page_per)
    else:
        end_page = rows % page_per
        page = pages - page
        if end_page:
            first_select = page_per * (page) + end_page
        else:
            first_select = page_per * (page + 1)
        first_select = page_per * (page + 1)
        sql = u'select mid,motor,motorname,address,admin,phone,create_date_str from (select * from dm_motor order by dateline limit %d;) order by dateline desc limit %d)' % (first_select,page_per)
        
    try:
        cur.execute(sql)
        data = cur.fetchall()
        cur.execute('select motor,count(hid) from dm_host group by motor')
        #存储每个机房有多少机器。
        motor_host = dict(cur.fetchall())
        id = 1
        data_list = []
        for row in data:
            data_list.append(dict(id=id,mid=row[0],motor=row[1],motorname=row[2],address=row[3],admin=row[4],phone=row[5],motor_host=motor_host.get(row[1],0),create_date_str=row[6])) 
            id += 1 

    except Exception,err:
        return False,err.message
    else:
        return data_list,pages

def insert_all_host(conn,data):
    dateline,date_str = time_format.time_now()
    sql = r'insert into dm_host(hostname,service_ip,service_mac,data_ip,data_mac,monitor_ip,monitor_mac,idrac_ip,idrac_mac,rest_ip,memory,disk,cpu,server_model,system,bios_version,board_model,board_serial,item,service,port,admin,phone,motor,cabinet,pos,status,create_date,create_date_str,description) values (%(hostname)s,%(service_ip)s,%(service_mac)s,%(data_ip)s,%(data_mac)s,%(monitor_ip)s,%(monitor_mac)s,%(idrac_ip)s,%(idrac_mac)s,%(rest_ip)s,%(memory)s,%(disk)s,%(cpu)s,%(server_model)s,%(system)s,%(bios_version)s,%(board_model)s,%(board_serial)s,%(item)s,%(service)s,%(port)s,%(admin)s,%(phone)s,%(motor)s,%(cabinet)s,%(pos)s,%(status)s,%(create_date)s,%(create_date_str)s,%(description)s)'
    data['create_date'] = dateline
    data['create_date_str'] = date_str

    try:
        cur = conn.cursor()
        cur.execute(sql,data)
        conn.commit()
    except Exception,err:
        info = err.message
        if 'already exists' in info:
            info = u'主机已存在, 创建失败'
        elif 'is not present in table' in info:
            info = u'机房或机柜不存在, 创建失败'
        return False,info
    else:
        return True,u'创建成功'

def insert_all_motor(conn,data):
    dateline,date_str = time_format.time_now()
    sql = r'insert into dm_motor(motor,motorname,address,admin,phone,create_date,create_date_str,description) values (%(motor)s,%(motorname)s,%(address)s,%(admin)s,%(phone)s,%(create_date)s,%(create_date_str)s,%(description)s)'

    data['create_date'] = dateline
    data['create_date_str'] = date_str
    try:
        cur = conn.cursor()
        cur.execute(sql,data)
        conn.commit()
    except Exception,err:
        info = err.message
        if 'already exists' in info:
            info = u'机房已存在'
        return False,info
    else:
        return True,u'创建成功'

def insert_all_cabinet(conn,data):
    dateline,date_str = time_format.time_now()
    sql = r'insert into dm_cabinet(motor,cabinet,row,col,height,description) values (%(motor)s,%(cabinet)s,%(row)s,%(col)s,%(height)s,%(description)s)'
    data['create_date'] = dateline
    data['create_date_str'] = date_str
    try:
        cur = conn.cursor()
        cur.execute(sql,data)
        conn.commit()
    except Exception,err:
        info = err.message
        if 'is not present in table "dm_motor"' in info:
            info = u'机房不存在'
        elif 'already exists' in info:
            info = u'机房中此机柜已存在'
        return False,info

    else:
        return True,u'创建成功'

def select_all_host(conn,hid):
    sql = r'select hostname,service_ip,service_mac,data_ip,data_mac,monitor_ip,monitor_mac,idrac_ip,idrac_mac,rest_ip,memory,disk,cpu,server_model,system,bios_version,board_model,board_serial,item,service,port,admin,phone,motor,cabinet,pos,status,date_str,create_date_str,description from dm_host where hid = %d' % hid
    try:
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
    except Exception,err:
        return False,err.message
    data_dict = dict(hostname=data[0],service_ip=data[1],service_mac=data[2],data_ip=data[3],data_mac=data[4],monitor_ip=data[5],monitor_mac=data[6],idrac_ip=data[7],idrac_mac=data[8],rest_ip=data[9],memory=data[10],disk=data[11],cpu=data[12],server_model=data[13],system=data[14],bios_version=data[15],board_model=data[16],board_serial=data[17],item=data[18],service=data[19],port=data[20],admin=data[21],phone=data[22],motor=data[23],cabinet=data[24],pos=data[25],status=data[26],date_str=data[27],create_date_str=data[28],description=data[29])
    return True,data_dict

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
    
