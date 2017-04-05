#/usr/bin/env python
#
import psycopg2
from config import *
import redis
#from contextlib import closing

dm_user = r'create table dm_user(uid serial PRIMARY KEY,username char(30) NOT NULL UNIQUE, password varchar(50) NOT NULL,section char(20),phone char(20),email char(50),dateline int,date_str char(30),status char(3),offtime int,level int NOT NULL,head_portrait varchar(150),description varchar(255))'
dm_user_notify = r'create table dm_notify(uid int REFERENCES dm_user (uid),notify varchar(255),dateline int,date_str char(30),status char(6))'
dm_motor = r'create table dm_motor(mid serial PRIMARY KEY,motor char(30) NOT NULL UNIQUE,address varchar(100),admin char(15),phone char(20),dateline int,description varchar(255))'
dm_cabinet = r'create table dm_cabinet(cid serial PRIMARY KEY,motor char(30) REFERENCES dm_motor (motor),cabinet char(30) NOT NULL,row char(10),col char(10),height char(2),dateline int,descriptioin varchar(255),UNIQUE (motor,cabinet))'

dm_host = r'create table dm_host(hid serial PRIMARY KEY,hostname char(20) NOT NULL UNIQUE,service_ip char(15),service_mac char(17),data_ip char(15),data_mac char(17),monitor_ip char(15),monitor_mac char(17),rest_ip char(60),idrac_ip char(15),idrac_mac char(17),memory char(10),disk char(10),cpu char(20),server_model char(20),system char(20),bios_version char(20),board_model char(20),board_serial char(20),item char(20),service char(30),port char(20),admin char(15),phone char(20),motor char(30),cabinet char(30),pos char(10),status char(10),dateline int,date_str char(30),description varchar(255),FOREIGN KEY (motor,cabinet) REFERENCES dm_cabinet (motor,cabinet))'

def connect_db():
    return psycopg2.connect(host=DBHOST,dbname=DBNAME,user=DBUSER, \
           password=DBPASSWORD,port=DBPORT)

def connect_redis():
    return redis.Redis(REDIS_HOST,REDIS_PORT)

def init_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(dm_user)
    cur.execute(dm_user_notify)
    cur.execute(dm_motor)
    cur.execute(dm_cabinet)
    cur.execute(dm_host)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
