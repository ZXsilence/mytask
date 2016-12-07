#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumingchao
@contact: liumingchao@maimiaotech.com
@date: 2016-10-26 15:34
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import datetime

def split_date(sdate,edate):
    date_list = []
    sdate = datetime.datetime.combine(sdate,datetime.time())
    edate= datetime.datetime.combine(edate,datetime.time())
    date_list.append((sdate,edate))
    return date_list
   # while True:
   #     tmp_edate = min(sdate + datetime.timedelta(days=6),edate)
   #     date_list.append((sdate,tmp_edate))
   #     if tmp_edate >= edate:
   #         return date_list
   #     else:
   #         sdate = tmp_edate + datetime.timedelta(days=1)



if __name__ == '__main__':
    edate = datetime.datetime(2016,11,1,10,10)
    sdate =  edate - datetime.timedelta(days = 6)
    res = split_date(sdate,edate)
    for item in res:
        print item

