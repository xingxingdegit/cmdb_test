#!/usr/bin/env python
import time

def time_now():
    dateline = int(time.time())
    date_str = time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(dateline))
    return dateline,date_str
