#/usr/bin/env python
#
import psycopg2
from config import *
#from contextlib import closing

dm_user = r'create table dm_user(id serial PRIMARY KEY,username char(30) NOT NULL UNIQUE, password varchar(50) NOT NULL,section char(20),phone char(20),email char(50),create_date int,create_date_str char(30),status char(3),offtime int,level int NOT NULL)'
dm_motor = r'create table dm_motor(id serial PRIMARY KEY,motor char(30) NOT NULL UNIQUE,address varchar(100),admin char(15),phone char(20))'
dm_cabinet = r'create table dm_cabinet(id serial PRIMARY KEY,motor char(30) REFERENCES dm_motor (motor),cabinet char(30) NOT NULL,row char(10),col char(10),size int,UNIQUE (motor,cabinet))'
dm_host = r'create table dm_host(id serial PRIMARY KEY,hostname char(20) NOT NULL UNIQUE,ip1 char(20),ip2 char(20),ip3 char(20),ip4 char(20),ip5 varchar(20),ip6 varchar(20),item char(20),service char(30),port char(20),admin char(15),phone char(20),motor char(30),cabinet char(30),pos_start int,pos_end int,status char(10),FOREIGN KEY (motor,cabinet) REFERENCES dm_cabinet (motor,cabinet))'

def connect_db():
    return psycopg2.connect(host=DBHOST,dbname=DBNAME,user=DBUSER, \
           password=DBPASSWORD,port=DBPORT)

def init_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(dm_user)
    cur.execute(dm_motor)
    cur.execute(dm_cabinet)
    cur.execute(dm_host)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
