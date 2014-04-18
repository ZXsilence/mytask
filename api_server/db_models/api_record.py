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
from api_server.conf import settings 
from api_server.common.decorator import  mongo_exception

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
            all_day_limit:标识API全天被限
            soft_code:应用名
            fail_detail_info:错误的详细记录
    '''
    @classmethod
    @mongo_exception
    def inc_success_record(cls,soft_code,source,method,date_str):
        cls.coll.update({'date':date_str,'source':source,'method':method,'soft_code':soft_code},\
                {'$inc':{'success_times':1,'total_times':1}})

    @classmethod
    @mongo_exception
    def inc_fail_record(cls,soft_code,source,method,date_str,sub_code):
        cls.coll.update({'date':date_str,'source':source,'method':method,'soft_code':soft_code},\
                {'$inc':{'fail_times':1,'total_times':1,'fail_detail_info.%s'%sub_code:1}})

    @classmethod
    @mongo_exception
    def inc_fail_record_new(cls,soft_code,source,method,date_str,sub_code):
        cls.coll.update({'date':date_str,'source':source,'method':method,'soft_code':soft_code},\
                {'$inc':{'fail_times':1,'total_times':1},'$set':{'fail_detail_info.%s'%sub_code:1}})

    @classmethod
    @mongo_exception
    def find_api_record(cls,soft_code,source,method,date_str):
        if soft_code:
            filter = {'source':source,'method':method,'date':date_str,'soft_code':soft_code}
        else:
            filter = {'source':source,'method':method,'date':date_str}
        doc = cls.coll.find_one(filter)
        if not doc:
            return None
        return doc

    @classmethod
    @mongo_exception
    def insert_record(cls,record_dict):
        filter = {'soft_code':record_dict['soft_code'],'date':record_dict['date'],'method':record_dict['method'],'source':record_dict['source']}
        cls.coll.update(filter,record_dict,upsert=True)


    @classmethod
    @mongo_exception
    def set_all_day_limit(cls,soft_code,source,method,date_str,flag):
        filter = {'soft_code':soft_code,'date':date_str,'method':method,'source':source}
        cls.coll.update(filter,{'all_day_limit':flag},upsert=False)


