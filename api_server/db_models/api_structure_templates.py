#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-08-07 13:30
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import sys,os
import MySQLdb
import simplejson

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    sys.path.append(os.path.join(os.path.dirname(__file__),'../..'))
    from api_server.conf import set_env
    set_env.getEnvReady()
from db_pool.lib.pool_util import PoolUtil   
from api_server.common.decorator import mysql_exception

class ApiStructureTemplate(object):
    _db = "api_virtual"
    _table = "api_structure_templates"
    _fields = """api_name,api_input,api_output"""

    @classmethod
    def _get_cursor(cls):
        return PoolUtil.get_cursor(cls._db)

    @classmethod
    def _close_cursor(cls, conn, cursor):
        PoolUtil.close_cursor(conn,cursor)

    @classmethod
    def _row_to_dict(cls,row):
        (api_name,api_input,api_output) = row
        ret = {}
        ret['api_name'] = api_name
        ret['api_input'] = simplejson.loads(api_input)
        ret['api_output'] = simplejson.loads(api_output)
        return ret

    @classmethod
    def _data_cleaning(cls,settings_dict):
        for k ,v in settings_dict.iteritems():
            #if isinstance(v,dict):
            #    cls._data_cleaning(v)
            #if isinstance(v,list):
            #    for k1 in v:
            #        if isinstance(k1,dict):
            #            cls._data_cleaning(k1)
            if isinstance(v,unicode):
                settings_dict[k] = v.encode("utf-8")
        return settings_dict

    @classmethod
    @mysql_exception
    def get_api_structure_by_name(cls,api_name):
        sql = "select * from %s where api_name='%s' " % (cls._table,api_name)
        conn, cursor = cls._get_cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        if not row:
            return None
        return ApiStructureTemplate._row_to_dict(row)

    @classmethod
    @mysql_exception
    def set_api_structure(cls,api_name,api_input,api_output):
        api_input = cls._data_cleaning(api_input)
        api_output = cls._data_cleaning(api_output)
        sql = "replace into %s(%s) values " % (cls._table,cls._fields)
        sql  += "(%s,%s,%s)"
        values = (api_name,simplejson.dumps(api_input),simplejson.dumps(api_output))
        conn, cursor = cls._get_cursor()
        cursor.execute(sql,values)
        conn.commit()
        cls._close_cursor(conn, cursor)

    @classmethod
    @mysql_exception
    def create_table(cls):
        conn, cursor = cls._get_cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS %s(\
            api_name varchar(60) primary key,
            api_input text not null,
            api_output text not null
            )ENGINE = InnoDB default charset=utf8;
        """ % cls._table
        cursor.execute(sql)
        conn.commit()
        cls._close_cursor(conn, cursor)

if __name__ == "__main__":
    #ApiStructureTemplate.create_table()
    api_name = "taobao.simba.keywords.pricevon.set"
    api_input = {'keywordid_prices': [{"mobileIsDefaultPrice": 0, "maxMobilePrice": 99, "maxPrice": 100, "isDefaultPrice": 0, "keywordId": 359278253772, "matchScope": 4}], 'method': 'taobao.simba.keywords.pricevon.set', 'nick': 'chinchinstyle'}
    api_output = {'simba_keywords_pricevon_set_response': {'keywords': {'keyword': [{'word': '连衣裙', 'max_mobile_price': 54, 'match_scope': '4', 'campaign_id': 9214487, 'modified_time': '2017-08-04 09:17:29', 'nick': 'chinchinstyle', 'create_time': '2017-08-03 17:46:49', 'is_default_price': False, 'adgroup_id': 779381813, 'mobile_is_default_price': 0, 'keyword_id': 359278253772, 'audit_status': 'audit_pass', 'max_price': 100, 'is_garbage': False}]}, 'request_id': '2f9ueo8vyjlw'}}
    #ApiStructureTemplate.set_api_structure(api_name,api_input,api_output)

    api_name = "taobao.simba.keywordsbyadgroupid.get"
    api_input = {'timestamp': u'1502091427445', 'method': u'taobao.simba.keywordsbyadgroupid.get', 'adgroup_id': u'770370215', 'nick': u'chinchinstyle'}
    api_output = {'simba_keywordsbyadgroupid_get_response': {'keywords': {'keyword': [{'qscore': '7', 'word': u'\u5f00\u886b\u6bdb\u8863\u5916\u5957 \u5973', 'max_mobile_price': 52, 'match_scope': '4', 'campaign_id': 3442512, 'modified_time': '2017-08-07 15:35:31', 'nick': 'chinchinstyle', 'create_time': '2017-08-07 15:35:25', 'is_default_price': False, 'adgroup_id': 770370215, 'mobile_is_default_price': 0, 'keyword_id': 359905166893, 'audit_status': 'audit_pass', 'max_price': 40, 'is_garbage': False}]}, 'request_id': 'yfaebycvbm8'}}


    #ApiStructureTemplate.set_api_structure(api_name,api_input,api_output)
    res = ApiStructureTemplate.get_api_structure_by_name(api_name)
    print res
