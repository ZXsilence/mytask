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
from db_pool.conf.settings import RDS1,RDS2,RDS3,RDS4
from DBUtils.PooledDB import PooledDB

class PoolUtil(object):
    _conn_pool = {}
    _conn_num = 0

    @classmethod
    def _get_db_pool(self,db_name,RDS):
        self._conn_num += 1
        if self._conn_num %100 ==0:
            print 'use conn:%s' % self._conn_num
        if db_name in self._conn_pool:
            return self._conn_pool[db_name]
        db_set = RDS['pool_addr']
        pool = PooledDB(creator = MySQLdb, 
            maxusage=1000,
            mincached = 0,
            maxcached = 50,
            maxshared  = 0,
            maxconnections = 200,
            blocking = True,
            host=db_set['HOST'],
            port=db_set['PORT'],
            user=db_set['USER'],
            passwd=db_set['PASSWD'], 
            db=db_name,
            charset="utf8")
        self._conn_pool[db_name] = pool
        return pool

    #@classmethod
    #def _get_cursor_by_rds(self,db_name,RDS):
    #    pool = self._get_db_pool(db_name,RDS)
    #    conn = pool.connection()
    #    cursor = conn.cursor()
    #    return(conn,cursor)

    @classmethod
    def _get_cursor_by_rds(self,db_name,RDS):
        db_set = RDS['pool_addr']
        conn=MySQLdb.connect(host=db_set['HOST'],port=int(db_set['PORT']),\
                user=db_set['USER'],passwd=db_set['PASSWD'],db=db_name,charset="utf8")
        cursor = conn.cursor()
        return (conn,cursor)

    @classmethod
    def get_cursor(self,db_name):
        rds1_db_list= RDS1['db_list']
        rds2_db_list= RDS2['db_list']
        rds3_db_list= RDS3['db_list']
        rds4_db_list= RDS4['db_list']
        if db_name in rds1_db_list:
            return PoolUtil._get_cursor_by_rds(db_name,RDS1)
        elif db_name in rds2_db_list:
            return PoolUtil._get_cursor_by_rds(db_name,RDS2)
        elif db_name in rds3_db_list:
            return PoolUtil._get_cursor_by_rds(db_name,RDS3)
        elif db_name in rds4_db_list:
            return PoolUtil._get_cursor_by_rds(db_name,RDS4)
        else:
            raise Exception('can not find db_name in rds settings,current db_name is %s'%db_name)

    @classmethod
    def close_cursor(self,conn,cursor):
        cursor.close()
        conn.close()

