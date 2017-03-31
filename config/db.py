#/usr/bin/env python
#
import psycopg2
from config import *
#from contextlib import closing

def connect_db():
    return psycopg2.connect(host=DBHOST,dbname=DBNAME,user=DBUSER, \
           password=DBPASSWORD,port=DBPORT)

def init_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(r'create table entries(id serial primary key,title varchar(50) not null,text text  not null)')
    conn.commit()
    conn.close()
#    with closing(connect_db()) as db:
#        db.cursor().execute(r'create table entries(id serial primary key,title varchar(50) not null,text text  not null)')
#        db.commit()
        

    
