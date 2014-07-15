#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wulingping
@contact: wulingping@maimiaotech.com
@date: 2014-07-14 14:48
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import os,sys,random
import MySQLdb
currDir = os.path.normpath(os.path.dirname(__file__))
os.path.normpath(os.path.join(currDir, '../../../'))
from db_pool.conf.settings import RDS1,RDS2

class PoolUtil(object):

    @classmethod
    def _get_cursor_by_rds(self,db_name,RDS):
        db_set = RDS['pool_addr']
        conn=MySQLdb.connect(host=db_set['HOST'],user=db_set['USER'],passwd=db_set['PASSWD'],db=db_name,charset="utf8")
        cursor = conn.cursor()
        return (conn,cursor)

    @classmethod
    def get_cursor(self,db_name):
        rds1_db_list= RDS1['db_list']
        rds2_db_list= RDS2['db_list']
        if db_name in rds1_db_list:
            return PoolUtil._get_cursor_by_rds(db_name,RDS1)
        elif db_name in rds2_db_list:
            return PoolUtil._get_cursor_by_rds(db_name,RDS2)
        else:
            raise Exception('can not find db_name in rds settings,current db_name is %s'%db_name)

    @classmethod
    def close_cursor(self,conn,cursor):
        cursor.close()
        conn.close()

