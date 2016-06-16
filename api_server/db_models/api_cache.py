#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: xieguanfu
@contact: xieguanfu@maimiaotech.com
@date: 2015-09-02 22:42
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""


import sys
import os
from datetime import  datetime
from api_server.conf import db_settings
from api_server.common.decorator import mongo_exception
 
class ApiCache(object):
 
    _conn = None 
    coll = None 
    _db = 'api_cache'

    @classmethod
    def get_coll_name(cls):
        now = datetime.now()
        return 'api_cache_%s' % now.strftime('%Y%m%d')

    @classmethod
    def check_conn(cls):
        if not cls._conn:
            cls._conn = db_settings.get_conn()

    @classmethod
    #@mongo_exception
    def upsert_api_cache(cls,cache_key,cache_data,add_info_dict = {}):
        cls.check_conn()
        now = datetime.now()
        table_name = cls.get_coll_name()
        data = {'_id':cache_key,'data':cache_data,'cache_time':now}
        data.update(add_info_dict)
        cls._conn[cls._db][table_name].save(data)

    @classmethod
    #@mongo_exception
    def get_api_cache(cls,cache_key):
        cls.check_conn()
        table_name = cls.get_coll_name()
        return cls._conn[cls._db][table_name].find_one({'_id':cache_key})

    @classmethod
    #@mongo_exception
    def clear_cache_by_cache_key(cls,cache_key):
        cls.check_conn()
        table_name = cls.get_coll_name()
        cls._conn[cls._db][table_name].remove({'_id':cache_key})

    @classmethod
    #@mongo_exception
    def clear_cache(cls,cache_name,nick,add_info_dict = {}):
        cls.check_conn()
        table_name = cls.get_coll_name()
        filter_dict = {'cache_name':cache_name,'nick':nick}
        filter_dict.update(add_info_dict)
        cls._conn[cls._db][table_name].remove(filter_dict)
