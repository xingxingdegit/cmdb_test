#!/usr/bin/env python
#--*-- coding:utf-8 --*--
#
import math,time_format
from config import config

def sql_filter(data,table,op):
    if op.lower() == 'insert':
        sql = 'insert into %s(' % table
        value = 'values('
        for key in data:
            sql = sql + key + ','
            value = value + ('%%(%s)s,' % key)
        sql = sql.strip(',') + ')' + value.strip(',') + ')'
    elif op.lower() == 'update':
        sql = 'update %s set ' % table
        for key in data:
            sql = sql + ("%s='%s'," % (key,data[key]))
        return sql.strip(',') + ' '
    else:
        sql =  u'不支持此操作'

    return sql


def select_page_host(conn,page,where='true'):
    #根据请求页数，获取数据，并返回数据数典和总的页数。 如果有问题，则返回 False和错误信息。 postgresql里面true为真，相当于没有加条件. 用于在作搜索的时候，传递条件.
    try:
        cur = conn.cursor()
        pages_sql = r'select count(hid) from dm_host where %s' % where
        cur.execute(pages_sql)
    except Exception,err:
        return False,err.message
    try:
        page = int(page)
    except: page = 1

    rows = cur.fetchone()[0]
    #在没有匹配的记录，随便返回一些空数据，不能是False。
    if rows == 0: return {},0,None
#    return False,str(rows)
    page_per = config.PAGE_PER
    pages = math.ceil(rows / float(page_per))
    if page > pages:
        page = pages

#three select style, first :if range of part from top is nearly. second: if range of part from end is nearly.  third : 最后一页, 是否正好一页.     
    if page == 1:
        sql = u'select hid,hostname,service_ip,data_ip,monitor_ip,item,service,system,admin,phone,status,date_str,motor from dm_host where %s order by dateline desc limit %d' % (where,page_per)

    elif page <= (pages / 2):
        first_select = page_per * page
        sql = u'select hid,hostname,service_ip,data_ip,monitor_ip,item,service,system,admin,phone,status,date_str,motor from (select * from (select * from dm_host where %s order by dateline desc limit %d)as a order by dateline limit %d)as b order by dateline desc' % (where,first_select,page_per)
    elif page == pages:
        end_page = rows % page_per
        if end_page:
            sql = u'select hid,hostname,service_ip,data_ip,monitor_ip,item,service,system,admin,phone,status,date_str,motor from dm_host where %s order by dateline desc limit %d' % (where,end_page)
        else:
            sql = u'select hid,hostname,service_ip,data_ip,monitor_ip,item,service,system,admin,phone,status,date_str,motor from dm_host where %s order by dateline desc limit %d' % (where,page_per)
    else:
        end_page = rows % page_per
        page = pages - page
        first_select = page_per * page + (end_page or page_per)
        sql = u'select hid,hostname,service_ip,data_ip,monitor_ip,item,service,system,admin,phone,status,date_str,motor from (select * from dm_host where %s order by dateline limit %d)as a order by dateline desc limit %d' % (where,first_select,page_per)
        
    try:
        cur.execute(sql)
        data = cur.fetchall()
        id = 1
        data_list = []
        for row in data:
            data_list.append(dict(id=id,hid=row[0],hostname=row[1],service_ip=row[2],data_ip=row[3],monitor_ip=row[4],item=row[5],service=row[6],system=row[7],admin=row[8],phone=row[9],status=row[10],data_str=row[11],motor=row[12]))
            id += 1

    except Exception,err:
        return False,err.message,None
    else:
        return data_list,pages,rows

def select_page_cabinet(conn,page,where='true'):
    #根据请求页数，获取数据，并返回数据数典和总的页数。 如果有问题，则返回 False和错误信息。
    try:
        cur = conn.cursor()
        pages_sql = r'select count(cid) from dm_cabinet where %s' % where
        cur.execute(pages_sql)
    except Exception,err:
        return False,err.message
    try:
        page = int(page)
    except: page = 1

    rows = cur.fetchone()[0]
    #在没有匹配的记录，随便返回一些空数据，不能是False。
    if rows == 0: return {},0,None
    page_per = config.PAGE_PER
    pages = math.ceil(rows / float(page_per))
    if page > pages:
        page = pages
#three select style, first :if range of part from top is nearly. second: if range of part from end is nearly.  third : 最后一页, 是否正好一页.     
    if page == 1:
        sql = u'select cid,motor,cabinet,row,col,height,date_str from dm_cabinet where %s order by dateline desc limit %d' % (where,page_per)

    elif page <= (pages / 2):
        first_select = page_per * page
        sql = u'select cid,motor,cabinet,row,col,height,date_str from (select * from (select * from dm_cabinet where %s order by dateline desc limit %d)as a order by dateline limit %d)as b order by dateline desc' % (where,first_select,page_per)
    elif page == pages:
        end_page = rows % page_per
        if end_page:
            sql = u'select cid,motor,cabinet,row,col,height,date_str from dm_cabinet where %s order by dateline desc limit %d' % (where,end_page)
        else:
            sql = u'select cid,motor,cabinet,row,col,height,date_str from dm_cabinet where %s order by dateline desc limit %d' % (where,page_per)
    else:
        end_page = rows % page_per
        page = pages - page
        first_select = page_per * page + (end_page or page_per)
        sql = u'select cid,motor,cabinet,row,col,height,date_str from (select * from dm_cabinet where %s order by dateline limit %d)as a order by dateline desc limit %d' % (where,first_select,page_per)
        
    try:
        cur.execute(sql)
        data = cur.fetchall()
        id = 1
        data_list = []
        for row in data:
            data_list.append(dict(id=id,cid=row[0],motor=row[1],cabinet=row[2],row=row[3],col=row[4],height=row[5],date_str=row[6]))
            id += 1
    except Exception,err:
        return False,err.message,None
    else:
        return data_list,pages,rows

def select_page_motor(conn,page,where='true'):
    #根据请求页数，获取数据，并返回数据数典和总的页数。 如果有问题，则返回 False和错误信息。
    try:
        cur = conn.cursor()
        pages_sql = r'select count(mid) from dm_motor where %s' % where
        cur.execute(pages_sql)
    except Exception,err:
        return False,err.message
    try:
        page = int(page)
    except: page = 1

    rows = cur.fetchone()[0]
    #在没有匹配的记录，随便返回一些空数据，不能是False。
    if rows == 0: return {},0,None
    page_per = config.PAGE_PER
    pages = math.ceil(rows / float(page_per))
    if page > pages:
        page = pages
#three select style, first :if range of part from top is nearly. second: if range of part from end is nearly.  third : 最后一页, 是否正好一页.     
    if page == 1:
        sql = u'select mid,motor,motorname,address,admin,phone,create_date_str from dm_motor where %s order by dateline desc limit %d' % (where,page_per)

    elif page <= (pages / 2):
        first_select = page_per * page
        sql = u'select mid,motor,motorname,address,admin,phone,create_date_str from (select * from (select * from dm_motor where %s order by dateline desc limit %d) as a order by dateline limit %d) as b order by dateline desc' % (where,first_select,page_per)
    elif page == pages:
        end_page = rows % page_per
        if end_page:
            sql = u'select mid,motor,motorname,address,admin,phone,create_date_str from dm_motor where %s order by dateline desc limit %d' % (where,end_page)
        else:
            sql = u'select mid,motor,motorname,address,admin,phone,create_date_str from dm_motor where %s order by dateline desc limit %d' % (where,page_per)
    else:
        end_page = rows % page_per
        page = pages - page
        first_select = page_per * page + (end_page or page_per)
        sql = u'select mid,motor,motorname,address,admin,phone,create_date_str from (select * from dm_motor where %s order by dateline limit %d)as a order by dateline desc limit %d' % (where,first_select,page_per)
        
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
        return False,err.message,None
    else:
        return data_list,pages,rows

def insert_all_host(conn,data):
    dateline,date_str = time_format.time_now()
    data['create_date'] = dateline
    data['create_date_str'] = date_str
    data['dateline'] = dateline
    data['date_str'] = date_str
    sql = sql_filter(data,'dm_host','insert')

    try:
        cur = conn.cursor()
        cur.execute(sql,data)
    except Exception,err:
        conn.rollback()
        info = err.message
        if 'already exists' in info:
            info = u'主机已存在, 创建失败'
        elif 'is not present in table' in info:
            info = u'机房或机柜不存在, 创建失败'
        return False,info
    else:
        conn.commit()
        return True,u'创建成功'

def insert_all_motor(conn,data):
    dateline,date_str = time_format.time_now()
    data['create_date'] = dateline
    data['create_date_str'] = date_str
    data['dateline'] = dateline
    data['date_str'] = date_str
    sql = sql_filter(data,'dm_motor','insert')
    try:
        cur = conn.cursor()
        cur.execute(sql,data)
    except Exception,err:
        conn.rollback()
        info = err.message
        if 'already exists' in info:
            info = u'机房已存在'
        return False,info
    else:
        conn.commit()
        return True,u'创建成功'

def insert_all_cabinet(conn,data):
    dateline,date_str = time_format.time_now()
    data['create_date'] = dateline
    data['create_date_str'] = date_str
    data['dateline'] = dateline
    data['date_str'] = date_str
    sql = sql_filter(data,'dm_cabinet','insert')

    try:
        cur = conn.cursor()
        cur.execute(sql,data)
    except Exception,err:
        conn.rollback()
        info = err.message
        if 'is not present in table "dm_motor"' in info:
            info = u'机房不存在'
        elif 'already exists' in info:
            info = u'机房中此机柜已存在'
        return False,info

    else:
        conn.commit()
        return True,u'创建成功'

def select_all_host(conn,hid):
    sql = r'select host.hostname,host.service_ip,host.service_mac,host.data_ip,host.data_mac,host.monitor_ip,host.monitor_mac,host.idrac_ip,host.idrac_mac,host.rest_ip,host.memory,host.disk,host.cpu,host.server_model,host.system,host.bios_version,host.board_model,host.board_serial,host.item,host.service,host.port,host.admin,host.phone,host.motor,host.cabinet,host.pos,host.status,host.date_str,host.create_date_str,host.description,motor.motorname,cabinet.row,cabinet.col from dm_host as host,dm_motor as motor,dm_cabinet as cabinet where host.hid = %s and host.motor = motor.motor and host.cabinet = cabinet.cabinet and host.motor = cabinet.motor' % hid

    try:
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
    except Exception,err:
        return False,err.message
    data_dict = dict(hid=hid,hostname=data[0],service_ip=data[1],service_mac=data[2],data_ip=data[3],data_mac=data[4],monitor_ip=data[5],monitor_mac=data[6],idrac_ip=data[7],idrac_mac=data[8],rest_ip=data[9],memory=data[10],disk=data[11],cpu=data[12],server_model=data[13],system=data[14],bios_version=data[15],board_model=data[16],board_serial=data[17],item=data[18],service=data[19],port=data[20],admin=data[21],phone=data[22],motor=data[23],cabinet=data[24],pos=data[25],status=data[26],date_str=data[27],create_date_str=data[28],description=data[29] or '',motorname=data[30],row=data[31],col=data[32])
    return True,data_dict

def select_all_motor(conn,mid):
    sql = r'select dm_motor.motor,motorname,address,admin,phone,date_str,create_date_str,description,host.motor_host from dm_motor left join (select motor,count(hid) as motor_host from dm_host group by motor) as host on dm_motor.motor = host.motor where dm_motor.mid = %s' % mid

    try:
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
    except Exception,err:
        conn.rollback()
        return False,err.message
    data_dict = dict(mid=mid,motor=data[0],motorname=data[1],address=data[2],admin=data[3],phone=data[4],date_str=data[5],create_date_str=data[6],description=data[7] or '',motor_host=data[8] or 0)
    return True,data_dict

def select_all_cabinet(conn,cid):
    sql = r'select dm_cabinet.motor,dm_cabinet.cabinet,row,col,height,date_str,create_date_str,description,motor_cabinet_host from dm_cabinet left join (select motor,cabinet,count(hid) as motor_cabinet_host from dm_host group by motor,cabinet) as host on dm_cabinet.motor = host.motor and dm_cabinet.cabinet = host.cabinet where cid = %s' % cid
    try:
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        cur.execute('select motorname from dm_cabinet,dm_motor where dm_cabinet.motor = dm_motor.motor and dm_cabinet.cid = %s' % cid)
    except Exception,err:
        conn.rollback()
        return False,err.message
    data_dict = dict(cid=cid,motor=data[0],cabinet=data[1],row=data[2],col=data[3],height=data[4],date_str=data[5],create_date_str=data[6],description=data[7] or '',motor_cabinet_host=data[8] or 0)
    data_dict['motorname'] = cur.fetchone()[0]
    return True,data_dict

def update_item(conn,id,table,data):
    dateline,date_str = time_format.time_now()
    data['dateline'] = dateline
    data['date_str'] = date_str
    sql = sql_filter(data,table,'update')
    if table == 'dm_host':
        sql = sql + (' where hid=%s' % id)
    elif table == 'dm_motor':
        sql = sql + (' where mid=%s' % id)
    else:
        sql = sql + (' where cid=%s' % id)

    try:
        cur = conn.cursor()
        cur.execute(sql)
    except Exception,err:
        conn.rollback()
        return False,err.message
    else:
        conn.commit()
        return True,u'更新完成'

def search_host(conn,data,page):
#这里的true只是用来占位，方便下面sql语句中的and添加。
    where = 'true'
    if 'ip' in data:
        if data['ip'].strip():
            ip = data.pop('ip')
            where = "(service_ip='%s' or data_ip='%s' or monitor_ip='%s' or rest_ip='%s')" % (ip,ip,ip,ip)

    for key,value in data.items():
        if value.strip():
            where = where + ' and ' + key + '=' + "'" + value + "'"
#            where = where + ' and ' + key + ' like ' + "'" + '%' + value + '%' + "'"
    #浏览器搜索完以后，搜索栏还会显示搜索条件，是由服务端回传回去的，所以data字典中的内容不能变，把ip再加回去。
    try:
        data['ip'] = ip
    except: pass
    data_dict,pages,rows = select_page_host(conn,page,where)
    return data_dict,pages,rows

def search_motor(conn,data,page):
#这里的true只是用来占位，方便下面sql语句中的and添加。
    where = 'true'
    for key,value in data.items():
        if value.rstrip():
#            where = where + ' and ' + key + '=' + "'" + value + "'"
            where = where + ' and ' + key + ' like ' + "'" + '%' + value + '%' + "'"
    data_dict,pages,rows = select_page_motor(conn,page,where)
    #return False,data_dict,None
    return data_dict,pages,rows

def search_cabinet(conn,data,page):
#这里的true只是用来占位，方便下面sql语句中的and添加。
    where = 'true'
    for key,value in data.items():
        if value.strip():
#            where = where + ' and ' + key + '=' + "'" + value + "'"
            where = where + ' and ' + key + ' like ' + "'" + '%' + value + '%' + "'"
    data_dict,pages,rows = select_page_cabinet(conn,page,where)
    return data_dict,pages,rows
