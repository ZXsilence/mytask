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
            ApiRecord.inc_success_record(record['id'])

    @staticmethod
    def inc_fail_record(soft_code,source,method,date_str,sub_code):
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
            fail_detail_info = record['fail_detail_info']
            if fail_detail_info.has_key(sub_code):
                fail_detail_info[sub_code]+=1
            else:
                fail_detail_info[sub_code]=1
            ApiRecord.inc_fail_record(record['id'],fail_detail_info)

    @staticmethod
    def get_record(soft_code,source,method,date_str):
        return ApiRecord.find_api_record(soft_code,source,method,date_str)

    @staticmethod
    def set_all_day_limit(id,flag):
        ApiRecord.set_all_day_limit(id,flag)



