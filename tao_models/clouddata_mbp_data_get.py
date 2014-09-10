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
        int_fields = ["shop_id", "seller_id", "auction_id", "impressions", "click", "uv", "alipay_winner_num", "alipay_auction_num", "alipay_trade_num"]
        date_fields = ["thedate", "dt"]
        float_fields = ["alipay_trade_amt"]
        for row in row_list:
            values = row.values
            rpt = {}
            for i in range(len(values)):
                key = column_list[i]
                if key in int_fields:
                    rpt[key] = int(values[i]) 
                elif key in date_fields:
                    rpt[key] = datetime.datetime.strptime(values[i], "%Y%m%d") 
                elif key in float_fields:
                    rpt[key] = float(values[i])
                else:
                    rpt[key] = values[i]
            elements.append(rpt)
        return elements

    @classmethod
    @tao_api_exception()
    def _get_data_list(cls,sid,sql_id,sdate,edate,sub_offset=0,sub_limit=5000):
        print sql_id
        n = datetime.datetime.now()
        dt = n-datetime.timedelta(days=1)
        dt_str = dt.strftime("%Y%m%d")
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        parameter = "shop_id="+str(sid)+",sdate="+sdate_str+",edate="+edate_str+",dt="+dt_str+",sub_offset="+str(sub_offset)+",sub_limit="+str(sub_limit)+',dt1='+sdate_str+',dt2='+edate_str
        req = ClouddataMbpDataGetRequest() 
        req.sid = sid
        req.sql_id = sql_id
        req.parameter = parameter
        rsp = ApiService.execute(req)
        return cls._decode_clouddata(rsp)

    '''有点击词'''
    @classmethod
    def get_query_rpt(cls,sid,sdate,edate):
        rpt_list = []
        limit = 5000
        offset = 0
        sql_id = '4946'
        while True:
            try:
                rpt_sub_list = cls._get_data_list(sid,sql_id,sdate,edate,offset,limit)
                rpt_list.extend(rpt_sub_list)
                if len(rpt_sub_list) < limit:
                    break
                offset = offset + limit
            except Exception,e:
                return []
        return rpt_list

    '''获取用户90天成交词'''    
    @classmethod
    def get_query_list_by_sid(cls, sid):
        rpt_list = []
        edate = datetime.datetime.now() - datetime.timedelta(days=1)
        sdate = edate - datetime.timedelta(days=90)
        sql_id = '3378'
        rpt_list = cls._get_data_list(sid,sql_id,sdate,edate)
        return rpt_list

    @classmethod
    def get_shop_rpt_hour_30d(cls,sid,sub_offset,sub_limit):
        rpt_list = []
        edate = datetime.datetime.now() - datetime.timedelta(days=1)
        sdate = edate - datetime.timedelta(days=30)
        sql_id = '3971'
        rpt_list = cls._get_data_list(sid,sql_id,sdate,edate)
        return rpt_list
    
    @classmethod
    def get_shop_rpt_region_30d(cls,sid,sub_offset,sub_limit):
        rpt_list = []
        edate = datetime.datetime.now() - datetime.timedelta(days=1)
        sdate = edate - datetime.timedelta(days=30)
        sql_id = '3973'
        rpt_list = cls._get_data_list(sid,sql_id,sdate,edate)
        return rpt_list

    @classmethod
    def get_shop_plot_data(cls,sid,sdate,edate):
        rpt_list = []
        limit = 5000
        offset = 0
        sql_id = '5179'
        while True:
            try:
                rpt_sub_list = cls._get_data_list(sid,sql_id,sdate,edate,offset,limit)
                rpt_list.extend(rpt_sub_list)
                if len(rpt_sub_list) < limit:
                    break
                offset = offset + limit
            except Exception,e:
                return []
        return rpt_list




if __name__ == '__main__':
    sid = 63643897 
    edate = datetime.datetime.now() - datetime.timedelta(days=1)
    sdate = edate - datetime.timedelta(days=30)
    rpt_list = ClouddataMbpDataGet.get_query_rpt(sid,sdate,edate)
    print len(rpt_list)
    for item in rpt_list:
        print item['query']
