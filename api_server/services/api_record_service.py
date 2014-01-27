#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wulingping
@contact: wulingping@maimiaotech.com
@date: 2014-01-23 15:21
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
from datetime import datetime
from api_server.db_models.api_record import ApiRecord
from api_server.common.exceptions import ApiSourceError
from api_server.conf.settings import api_source,API_SOURCE
   
class ApiRecordService(object):

    @staticmethod
    def inc_success_record(source,method,date_str=None):
        if date_str is None:
            date_str = datetime.strftime(datetime.today(), '%Y-%m-%d')
        record = ApiRecord.find_api_record(date_str,source,method)
        if not record:
            record_new = {'date':date_str,'source':source,'method':method}
            record_new['success_times'] = 1
            record_new['fail_times'] = 0
            record_new['total_times'] = 1
            record_new['all_day_limit'] = False
            ApiRecord.insert_record(record_new)
        else:
            ApiRecord.inc_success_record(date_str,source,method)

    @staticmethod
    def inc_fail_record(source,method,date_str=None):
        if date_str is None:
            date_str = datetime.strftime(datetime.today(), '%Y-%m-%d')
        record = ApiRecord.find_api_record(date_str,source,method)
        if not record:
            record_new = {'date':date_str,'source':source,'method':method}
            record_new['success_times'] = 0
            record_new['fail_times'] = 1
            record_new['total_times'] = 1
            record_new['all_day_limit'] = False
            ApiRecord.insert_record(record_new)
        else:
            ApiRecord.inc_fail_record(date_str,source,method)

    @staticmethod
    def get_record(source,method,date_str=None):
        if date_str is None:
            date_str = datetime.strftime(datetime.today() , '%Y-%m-%d')
        return ApiRecord.find_api_record(date_str,source,method)


    @staticmethod
    def set_all_day_limit(method,source,flag,date_str=None):
        if date_str is None:
            date_str = datetime.strftime(datetime.today() , '%Y-%m-%d')
        ApiRecord.set_all_day_limit(date_str,method,source,flag)


