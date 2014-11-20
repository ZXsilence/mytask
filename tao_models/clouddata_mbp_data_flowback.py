#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumc
@contact: liumingchao@maimiaotech.com
@date: 2014-06-09 14:27
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ClouddataMbpDataFlowbackRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService 
from api_server.common.util import change_obj_to_dict_deeply
import datetime
import simplejson as json


class ClouddataMbpDataFlowback(object):
    
    @classmethod
    @tao_api_exception()
    def __encode_data(cls, input_data):
        """
        [{'shop_id':123,'nick':'abc'}, {'shop_id':456, 'name':'def'}]
        upload-multi-line;column1,column2,column3,dt;11,12,13,20140726;21,,23,20140727;31,,33,201
        40728...
        """
        encode_data = 'upload-multi-line;'
        keys = []
        for k in input_data[0].keys():
            if k == "dt":
                continue
            keys.append(k)
        keys.append('dt')
        encode_data += ','.join(keys) + ';'
        dt_value = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y%m%d')
        for e in input_data:
            values_one = []
            for k in keys:
                if k != 'dt':
                    values_one.append(str(e.get(k, '')))
                else:
                    values_one.append(dt_value)
            encode_data += ','.join(values_one) + ';'
        return encode_data
    
    @classmethod
    @tao_api_exception()
    def flowback_data(cls, table_name, input_data):
        """获取省油宝thedate新增店铺"""
        encode_data = cls.__encode_data(input_data)

        req = ClouddataMbpDataFlowbackRequest() 
        req.table_name = table_name 
        req.data = encode_data 
        rsp = ApiService.execute(req)
        print rsp
        return rsp.status



if __name__ == '__main__':
    input_data = [
        {'shop_id': 57501318, 'resv':''},
        {'shop_id': 73228923, 'resv':''},
        {'shop_id': 67807749, 'resv':''},
        {'shop_id': 110094078, 'resv':''},
        {'shop_id': 110271147, 'resv':''},
        {'shop_id': 73259890, 'resv':''},
        {'shop_id': 64116298, 'resv':''}
    ]
    status = ClouddataMbpDataFlowback.flowback_data('pri_upload.shop_id_sld', input_data)
