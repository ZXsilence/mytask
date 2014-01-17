#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wulingping
@contact: wulingping@maimiaotech.com
@date: 2013-10-30 16:54
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
from datetime import datetime
from tao_models.conf import settings 
from tao_models.common.decorator import  mongo_exception

class ApiRecord(object):

    _conn = settings.api_conn
    coll = _conn['api_record']['api_record']
    
    '''  ————————  api_record字段  ————————————
        
            date:调用日期，字符串
            source:调用来源
            method:调用的api方法名
            total_times:调用API总次数
            success_times:调用API成功次数
            error_times:调用API失败次数
    '''
    @classmethod
    @mongo_exception
    def inc_success_record(cls,date_str,source,method):
        cls.coll.update({'date':date_str,'source':source,'method':method},{'$inc':{'success_times':1,'total_times':1}})

    @classmethod
    @mongo_exception
    def inc_fail_record(cls,date_str,source,method):
        cls.coll.update({'date':date_str,'source':source,'method':method},{'$inc':{'fail_times':1,'total_times':1}})

    @classmethod
    @mongo_exception
    def find_api_record(cls,date_str,source,method):
        doc = cls.coll.find_one({'source':source,'method':method,'date':date_str})
        if not doc:
            return None
        return doc

    @classmethod
    @mongo_exception
    def insert_record(cls,record_dict):
        filter = {'date':record_dict['date'],'method':record_dict['method'],'source':record_dict['source']}
        cls.coll.update(filter,record_dict,upsert=True)

