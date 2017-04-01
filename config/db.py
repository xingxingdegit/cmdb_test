#/usr/bin/env python
#
import psycopg2
from config import *
#from contextlib import closing

user_table = r'create table dm_user(uid serial primary key,username char(30) not null unique, password varchar(50) not null,section char(20),phone char(20),email char(50),create_date int,create_date_str char(30),status char(3),offtime int)'
admin_table = r'create table dm_admin(uid serial primary key,username char(30) not null unique, password varchar(50) not null,section char(20),phone char(20),email char(50),create_date int,create_date_str char(30))'
motor_table = r'create table dm_motor(id serial primary key,motor char(30) not null unique,address varchar(100),admin char(15),phone char(20))'
host_table = r'create table dm_host(hid serial primary key,ip1 char(20),ip2 char(20),ip3 char(20),ip4 char(20),ip5 varchar(20),ip6 varchar(20),item char(20),service char(30),port char(20),admin char(15),motor char(30) REFERENCES dm_motor (motor),cabinet char(20),cabinet_row int)'

def connect_db():
    return psycopg2.connect(host=DBHOST,dbname=DBNAME,user=DBUSER, \
           password=DBPASSWORD,port=DBPORT)

def init_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(user_table)
    cur.execute(admin_table)
    cur.execute(motor_table)
    cur.execute(host_table)
    conn.commit()
    conn.close()

