#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import simplejson
import MySQLdb

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    sys.path.append(os.path.join(os.path.dirname(__file__),'../..'))
    from api_server.conf import set_env
    set_env.getEnvReady()

from api_server.conf import settings 
from api_server.conf.settings import api_pool
from api_server.common.decorator import mysql_exception


class ApiRecord(object):
    '''  ————————  api_record字段  ————————————
        
            date:调用日期，字符串
            source:调用来源
            method:调用的api方法名
            total_times:调用API总次数
            success_times:调用API成功次数
            fail_times:调用API失败次数
            all_day_limit:标识API全天被限
            soft_code:应用名
            fail_detail_info:错误的详细记录
    '''
    _table = 'api_record'
    API_SETTINGS_MAX_EXECUTE_NUM = 1000 
    _fields = """source,soft_code,method,date,all_day_limit,\
            success_times,fail_times,total_times,fail_detail_info,\
            extend_field1,extend_field2,descr"""
    
    @classmethod
    def _get_cursor(cls):
        conn = api_pool.connection()
        cursor = conn.cursor()
        return (conn, cursor)

    @classmethod
    def _close_cursor(cls, conn, cursor):
        cursor.close()
        conn.close()

    @classmethod
    def _data_cleaning(cls, settings_dict):
        for k in settings_dict.keys():
            if type(settings_dict[k]) == type(u""):
                settings_dict[k] = settings_dict[k].encode("utf8")
        return settings_dict

    @classmethod
    def _row_to_dict(cls,row):
        (id,source,soft_code,method,date,all_day_limit,success_times,fail_times\
            ,total_times,fail_detail_info,extend_field1,extend_field2,descr) = row
        record_dict={}
        record_dict['id'] = id
        record_dict['source'] = source
        record_dict['method'] = method 
        record_dict['date'] = date
        record_dict['all_day_limit'] = bool(all_day_limit) 
        record_dict['success_times'] = success_times
        record_dict['fail_times'] = fail_times
        record_dict['total_times'] = total_times
        record_dict['fail_detail_info'] = simplejson.loads(fail_detail_info)
        return record_dict

    @classmethod
    @mysql_exception
    def inc_success_record(cls,id):
        set_str = "success_times=success_times+1,total_times=total_times+1"
        query = "UPDATE %s SET %s WHERE id=%s" % (cls._table, set_str, id)
        conn, cursor = cls._get_cursor()
        cursor.execute(query)
        conn.commit()
        cls._close_cursor(conn, cursor)

        #@classmethod
        #@mysql_exception
        #def inc_fail_record(cls,soft_code,source,method,date_str,sub_code):
        #    set_str = "fail_times=fail_times+1,total_times=total_times+1,fail_detail_info=%s"%simplejson.dumps(fail_detail_info)
        #    query = "UPDATE %s SET %s WHERE id=%s" % (cls._table, set_str, id)
        #    conn, cursor = cls._get_cursor()
        #    cursor.execute(query,value)
        #    conn.commit()
        #    cls._close_cursor(conn, cursor)


    @classmethod
    @mysql_exception
    def inc_fail_record(cls,id,fail_detail_info):
        set_str = "fail_times=fail_times+1,total_times=total_times+1,fail_detail_info='%s'"%simplejson.dumps(fail_detail_info)
        query = "UPDATE %s SET %s WHERE id=%s" % (cls._table, set_str, id)
        conn, cursor = cls._get_cursor()
        cursor.execute(query)
        conn.commit()
        cls._close_cursor(conn, cursor)


    @classmethod
    @mysql_exception
    def find_api_record(cls,soft_code,source,method,date_str):
        query = "SELECT  * FROM %s WHERE source='%s' AND method='%s'\
                AND date='%s'" %(cls._table,source,method,date_str)
        if soft_code:
            query += "AND soft_code='%s'"%soft_code
        conn, cursor = cls._get_cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        if not row:
            return None
        return ApiRecord._row_to_dict(row)

    @classmethod
    @mysql_exception
    def set_all_day_limit(cls,id,flag):
        set_str = "all_day_limit=%s"%int(flag)
        query = "UPDATE %s SET %s WHERE id=%s" % (cls._table, set_str, id)
        conn, cursor = cls._get_cursor()
        cursor.execute(query)
        conn.commit()
        cls._close_cursor(conn, cursor)

    @classmethod
    @mysql_exception
    def insert_record(cls,record_dict):
        record_dict = cls._data_cleaning(record_dict)
        value = (
                record_dict['source'],
                record_dict['soft_code'],
                record_dict['method'],
                record_dict['date'],
                int(record_dict['all_day_limit']),
                record_dict['success_times'],
                record_dict['fail_times'],
                record_dict['total_times'],
                simplejson.dumps(record_dict['fail_detail_info']),
                record_dict.get('extend_field1',None), 
                record_dict.get('extend_field2',None), 
                record_dict.get('descr',None) )
        query = "REPLACE INTO %s (%s) VALUES " % (cls._table, cls._fields)
        query += "(%s, %s, %s, %s, %s, %s, %s, %s , %s, %s ,%s ,%s)"
        conn, cursor = cls._get_cursor()
        cursor.execute(query, value)
        conn.commit()
        id = int(cursor.lastrowid)
        cls._close_cursor(conn, cursor)
        return id

    @classmethod
    @mysql_exception
    def create_table(cls):
        conn, cursor = cls._get_cursor()
        query = """ CREATE TABLE IF NOT EXISTS %s (\
            id int auto_increment primary key,
            source varchar(32) not null,
            soft_code varchar(32) not null,
            method varchar(64) not null,
            date varchar(32) not null,
            all_day_limit int not null,
            success_times int not null,
            fail_times int not null,
            total_times int not null,
            fail_detail_info text not null,

            extend_field1 varchar(32),
            extend_field2 varchar(32),
            descr text
            ) ENGINE = InnoDB
        """ % cls._table
        cursor.execute(query)
        conn.commit()
        cls._close_cursor(conn, cursor)


if __name__ == "__main__":
    ApiRecord.create_table()
    record_new = {'soft_code':'SYB','date':'2014-06-12','source':'syb_webpage','method':'tes'}
    record_new['success_times'] = 1
    record_new['total_times'] = 1
    record_new['all_day_limit'] = False
    record_new['fail_times'] = 0
    record_new['fail_detail_info'] = {}
    ApiRecord.insert_record(record_new)


