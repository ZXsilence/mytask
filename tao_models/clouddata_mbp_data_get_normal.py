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

from TaobaoSdk import ClouddataMbpDataGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService 
from api_server.common.util import change_obj_to_dict_deeply
import datetime
import simplejson as json

class ClouddataMbpDataGet(object):
    
    @classmethod
    def _decode_clouddata(cls,rsp):
        
        column_list = rsp.__dict__.get('column_list',[])
        row_list =  rsp.__dict__.get('row_list',[]) 
        elements = []
        if column_list == [] or row_list == []:
            return elements
        for row in row_list:
            values = row.values
            rpt = {}
            for i in range(len(values)):
                key = column_list[i]
                rpt[key] = values[i]
            elements.append(rpt)
        return elements


    @classmethod
    @tao_api_exception()
    def get_data_from_clouddata(cls, sql_id, query_dict):
        ret = []
        page_count = 0
        while page_count <= 20:
            query_dict_single = copy.copy(query_dict)
            query_dict_single['sub_limit'] = 5000
            query_dict_single['sub_offset'] = page_count*query_dict_single['sub_limit']
            parameter = ",".join([str(k)+"="+str(v) for k,v in query_dict_single.items()])

            #parameter = "shop_id="+str(sid)+",sdate="+sdate_str+",edate="+edate_str+",dt="+dt_str+",sub_offset="+str(sub_offset)+",sub_limit="+str(sub_limit)+',dt1='+sdate_str+',dt2='+edate_str
            req = ClouddataMbpDataGetRequest() 
            req.sql_id = sql_id
            req.parameter = parameter
            rsp = ApiService.execute(req)
            res = cls._decode_clouddata(rsp)
            ret.extend(res)
            if len(res) < query_dict_single['sub_limit']:
                break
            page_count += 1
            
        return ret
    

if __name__ == '__main__':
    sql_id = 6402
    query_dict = {"sdate":"20141128"}
    ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
    if len(ret) >= 1:
        print ",".join(ret[0].keys())
        for e in ret:
            print ",".join(e.values())
    exit(0)
