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
from api_server.db_models.api_record import ApiRecord
from api_server.common.exceptions import ApiSourceError
from api_server.conf.settings import api_source,API_SOURCE
   
class ApiRecordService(object):

    @staticmethod
    def inc_success_record(soft_code,source,method,date_str):
        record = ApiRecord.find_api_record(soft_code,source,method,date_str)
        if not record:
            record_new = {'soft_code':soft_code,'date':date_str,'source':source,'method':method}
            record_new['success_times'] = 1
            record_new['total_times'] = 1
            record_new['all_day_limit'] = False
            record_new['fail_times'] = 0
            record_new['fail_detail_info'] = {}
            ApiRecord.insert_record(record_new)
        else:
            ApiRecord.inc_success_record(soft_code,source,method,date_str)

    @staticmethod
    def inc_fail_record(soft_code,source,method,date_str,sub_code):
        sub_code = sub_code.replace('.','/')
        record = ApiRecord.find_api_record(soft_code,source,method,date_str)
        if not record:
            record_new = {'soft_code':soft_code,'date':date_str,'source':source,'method':method}
            record_new['success_times'] = 0
            record_new['fail_times'] = 1
            record_new['total_times'] = 1
            record_new['all_day_limit'] = False
            record_new['fail_detail_info'] = {sub_code:1}
            ApiRecord.insert_record(record_new)
        else:
            if record['fail_detail_info'].has_key(sub_code):
                ApiRecord.inc_fail_record(soft_code,source,method,date_str,sub_code)
            else:
                ApiRecord.inc_fail_record_new(soft_code,source,method,date_str,sub_code)


    @staticmethod
    def get_record(soft_code,source,method,date_str):
        return ApiRecord.find_api_record(soft_code,source,method,date_str)

    @staticmethod
    def set_all_day_limit(soft_code,source,method,date_str,flag):
        ApiRecord.set_all_day_limit(soft_code,source,method,date_str,flag)



