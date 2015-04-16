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
        int_fields = ["shop_id", "seller_id", "auction_id", "impressions", "click", "uv", "alipay_winner_num", "alipay_auction_num", "alipay_trade_num",\
                      "session_num","pv","visit_repeat_num","shop_collect_num","auction_collect_num","ipv","iuv","visit_platform","gmv_trade_num"]
        date_fields = ["thedate", "dt"]
        float_fields = ["alipay_trade_amt","bounce_rate"]
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
    
    @classmethod
    @tao_api_exception()
    def _get_data_list2(cls,sid,sql_id,sdate,edate,sub_offset=0,sub_limit=5000):
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        parameter = "shop_id="+str(sid)+",sdate="+sdate_str+",edate="+edate_str+",sub_offset="+str(sub_offset)+",sub_limit="+str(sub_limit)
        req = ClouddataMbpDataGetRequest() 
        req.sid = sid
        req.sql_id = sql_id
        req.parameter = parameter
        rsp = ApiService.execute(req)
        return cls._decode_clouddata(rsp)

    @classmethod
    @tao_api_exception()
    def _get_data_list3(cls,auction_id,sql_id,sdate,edate):
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        parameter = "auction_id="+str(auction_id)+",sdate="+sdate_str+",edate="+edate_str
        req = ClouddataMbpDataGetRequest() 
        req.sql_id = sql_id
        req.parameter = parameter
        rsp = ApiService.execute(req)
        return cls._decode_clouddata(rsp)
    
    @classmethod
    @tao_api_exception()
    def _get_data_list4(cls,auction_id,sql_id,thedate):
        date_str = thedate.strftime("%Y%m%d")
        parameter = "auction_id="+str(auction_id)+",dt="+date_str+",thedate="+date_str
        req = ClouddataMbpDataGetRequest() 
        req.sql_id = sql_id
        req.parameter = parameter
        rsp = ApiService.execute(req)
        return cls._decode_clouddata(rsp)
    
    @classmethod
    @tao_api_exception()
    def _get_data_list5(cls,sid,sql_id,thedate,sub_offset=0,sub_limit=5000):
        date_str = thedate.strftime("%Y%m%d")
        parameter = "shop_id="+str(sid)+",thedate="+date_str+",sub_offset="+str(sub_offset)+",sub_limit="+str(sub_limit)
        req = ClouddataMbpDataGetRequest() 
        req.sid = sid
        req.sql_id = sql_id
        req.parameter = parameter
        rsp = ApiService.execute(req)
        return cls._decode_clouddata(rsp)
    
    @classmethod
    @tao_api_exception()
    def _get_data_list_with_dt(cls,sid,sql_id,sdate,edate,sub_offset=0,sub_limit=5000,other_param_dict=None):
        n = datetime.datetime.now()
        dt = n-datetime.timedelta(days=1)
        dt_str = dt.strftime("%Y%m%d")
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        parameter = "shop_id="+str(sid)+",sdate="+sdate_str+",edate="+edate_str+",dt="+dt_str+",sub_offset="+str(sub_offset)+",sub_limit="+str(sub_limit)
        if other_param_dict:
            for k,v in other_param_dict.iteritems():
                parameter += ",%s=%s" % (k,v)
        req = ClouddataMbpDataGetRequest() 
        req.sid = sid
        req.sql_id = sql_id
        req.parameter = parameter
        rsp = ApiService.execute(req)
        return cls._decode_clouddata(rsp)
    
    @classmethod
    @tao_api_exception()
    def _get_data_list_between_dt(cls,sid,sql_id,sdate,edate,sub_offset=0,sub_limit=5000,other_param_dict=None):
        sub_offset=10
        sdate -= datetime.timedelta(days=10)
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        parameter = "shop_id="+str(sid)+",sdate="+sdate_str+",edate="+edate_str+",sub_offset="+str(sub_offset)+",sub_limit="+str(sub_limit)
        if other_param_dict:
            for k,v in other_param_dict.iteritems():
                parameter += ",%s=%s" % (k,v)
        req = ClouddataMbpDataGetRequest() 
        req.sid = sid
        req.sql_id = sql_id
        req.parameter = parameter
        rsp = ApiService.execute(req)
        return cls._decode_clouddata(rsp)

    @classmethod
    @tao_api_exception()
    def get_shop_list_append(cls, thedate):
        """获取省油宝thedate新增店铺"""
        
        sql_id = 3473
        dt = thedate.strftime("%Y%m%d")
        parameter = "dt="+str(dt)
        req = ClouddataMbpDataGetRequest() 
        req.sql_id = sql_id
        req.parameter = parameter
        rsp = ApiService.execute(req)

        shop_list = cls._decode_clouddata(rsp)
        for shop in shop_list:
            print shop['shop_id']
        return cls._decode_clouddata(rsp)

    @classmethod
    def get_items_rpt_by_sid(cls, sid, sdate, edate):
        """获取店铺商品基本报表数据"""
        rpt_list = []
        sql_id = '5569'
        limit = 5000
        offset = 0
        while True:
            rpt_sub_list = cls._get_data_list2(sid, sql_id, sdate, edate, offset, limit)
            rpt_list.extend(rpt_sub_list)
            if len(rpt_sub_list) < limit:
                break
            offset = offset + limit
        return rpt_list
    
    @classmethod
    def get_item_rpt(cls, item_id, sdate, edate):
        """获取商品基本报表数据"""
        sql_id = '5568'
        rpt_list = cls._get_data_list3(item_id, sql_id, sdate, edate)
        return rpt_list
    
    @classmethod
    def get_item_rpt_sum(cls, item_id):
        sql_id = '5678'
        thedate = datetime.datetime.now() - datetime.timedelta(days=1)
        rpt_list = cls._get_data_list4(item_id, sql_id, thedate)
        return rpt_list

    @classmethod
    def get_item_rpt_sum_by_sid(cls, sid):
        rpt_list = []
        sql_id = '6344'
        limit = 5000
        offset = 0
        thedate = datetime.datetime.now() - datetime.timedelta(days=1)
        item_rpt_dict = {}
        while True:
            rpt_sub_list = cls._get_data_list5(sid, sql_id, thedate, offset, limit)
            for item in rpt_sub_list:
                item_rpt_dict[item['auction_id']] = item
            if len(rpt_sub_list) < limit:
                break
            offset = offset + limit
        return item_rpt_dict 

    @classmethod
    def get_items_page_pc_rpt_by_sid(cls, sid, sdate, edate):
        """获取店铺商品页面pc报表数据"""
        rpt_list = []
        sql_id = '6345'
        limit = 5000
        offset = 0
        item_page_rpt_dict = {}
        rpt_keys = ['iuv', 'ipv', 'page_duration', 'bounce_cnt', 'landing_cnt', 'landing_uv', 'exit_cnt']
        while True:
            rpt_sub_list = cls._get_data_list2(sid, sql_id, sdate, edate, offset, limit)
            for item in rpt_sub_list:
                if item_page_rpt_dict.has_key(item['auction_id']):
                    for key in rpt_keys:
                        item_page_rpt_dict[item['auction_id']][key] += item[key]
                else:
                    item_page_rpt_dict[item['auction_id']] = item

            if len(rpt_sub_list) < limit:
                break
            offset = offset + limit
        return item_page_rpt_dict
    
    @classmethod
    def get_item_page_pc_rpt(cls, item_id, sdate, edate):
        """获取商品页面pc报表数据"""
        sql_id = '5561'
        rpt_list = cls._get_data_list3(item_id, sql_id, sdate, edate)
        return rpt_list

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
        sql_id = '6367'
        limit = 5000
        offset = 0
        rpt_list = []
        while True:
            try:
                rpt_sub_list = cls._get_data_list(sid,sql_id,sdate,edate,offset,limit)
                rpt_list.extend(rpt_sub_list)
                if len(rpt_sub_list) < limit:
                    break
                offset = offset + limit
            except Exception,e:
                break
        keyword_dict = {}
        
        rpt_keys = ['impression', 'alipay_trade_num', 'uv', 'alipay_winner_num', 'alipay_trade_amt', 'alipay_auction_num', 'click']
        for keyword in rpt_list:
            if keyword_dict.has_key(keyword['query']):
                for key in rpt_keys:
                    keyword_dict[keyword['query']][key] = keyword.get(key, 0)
            else:
                keyword_dict[keyword['query']] = keyword
        
        rpt_list = keyword_dict.values()
        return rpt_list

    @classmethod
    def get_shop_rpt_hour_30d(cls,sid,sub_offset,sub_limit):
        rpt_list = []
        edate = datetime.datetime.now() - datetime.timedelta(days=1)
        sdate = edate - datetime.timedelta(days=30)
        sql_id = '6366'
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
    
    @classmethod
    def get_seller_dwb_shop_rpt_90d(cls,sid,sdate,edate):
        rpt_list = []
        limit = 5000
        offset = 0
        sql_id = '100147'
        while True:
            try:
                rpt_sub_list = cls._get_data_list_between_dt(sid, sql_id, sdate, edate, offset, limit)
                rpt_list.extend(rpt_sub_list)
                if len(rpt_sub_list) < limit:
                    break
                offset = offset + limit
            except Exception,e:
                return []
        return rpt_list
    
    @classmethod
    def get_shop_platform_view_90d(cls,sid,sdate,edate,platform_id):
        rpt_list = []
        limit = 5000
        offset = 0
        sql_id = '100148'
        while True:
            try:
                rpt_sub_list = cls._get_data_list_between_dt(sid, sql_id, sdate, edate, offset, limit,{'platform_id':platform_id})
                rpt_list.extend(rpt_sub_list)
                if len(rpt_sub_list) < limit:
                    break
                offset = offset + limit
            except Exception,e:
                return []
        return rpt_list
    
    @classmethod
    def get_shop_last_effect_src_90d(cls,sid,sdate,edate,src_id):
        rpt_list = []
        limit = 5000
        offset = 0
        sql_id = '100150'
        while True:
            try:
                rpt_sub_list = cls._get_data_list_between_dt(sid, sql_id, sdate, edate, offset, limit,{'src_id':src_id})
                rpt_list.extend(rpt_sub_list)
                if len(rpt_sub_list) < limit:
                    break
                offset = offset + limit
            except Exception,e:
                return []
        return rpt_list

    @classmethod
    def get_seller_dwb_auction_rpt_90d(cls,sid,sdate,edate,auction_id):
        rpt_list = []
        limit = 5000
        offset = 0
        sql_id = '100149'
        while True:
            try:
                rpt_sub_list = cls._get_data_list_between_dt(sid, sql_id, sdate, edate, offset, limit,{'auction_id':auction_id})
                rpt_list.extend(rpt_sub_list)
                if len(rpt_sub_list) < limit:
                    break
                offset = offset + limit
            except Exception,e:
                return []
        return rpt_list

if __name__ == '__main__':
    sid = int(sys.argv[1])
    #res = ClouddataMbpDataGet.get_shop_rpt_hour_30d(sid,0,5000)
    res = ClouddataMbpDataGet.get_query_list_by_sid(sid)
    for item in res:
        print item
    exit(0)

    item_id = int(sys.argv[1])
    edate = datetime.datetime.now() - datetime.timedelta(days=1)
    sdate = edate - datetime.timedelta(days=10)
    #rpt_list = ClouddataMbpDataGet.get_item_rpt(item_id,sdate,edate)
    rpt_list = ClouddataMbpDataGet.get_item_page_pc_rpt(item_id,sdate,edate)

    print len(rpt_list)
    sum_dict = {}

    #for key in ['ipv', 'iuv', 'page_duration', 'bounce_cnt', 'landing_cnt', 'landing_uv', 'exit_cnt']:
    for key in ['ipv', 'alipay_auction_num', 'iuv', 'bounce_rate']:
        sum_dict[key] = 0
    
    #print 'date page_duration iuv ipv bounce_cnt landing_cnt landing_uv exit_cnt'
    for item in rpt_list:
        #for key in sum_dict.keys():
        #    sum_dict[key] += float(item[key])
        item['page_duration'] = float(item['page_duration']) / int(item['ipv'])
        print item['thedate'],item['page_duration'],item['iuv'],item['ipv'],item['bounce_cnt'],item['landing_cnt'],item['landing_uv'],item['exit_cnt']
    #print sum_dict

