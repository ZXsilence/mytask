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

import urllib
import sys
import os
import copy
import logging
import logging.config
import datetime
import chardet

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
from comm_tools.string_tools import StringTools
import datetime
import simplejson as json
logger = logging.getLogger(__name__)

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

    @classmethod
    def get_sid_nosearch_query_report(cls, sid, sdate, edate, dt1=None, dt2=None):
        """获取关键词_query报表"""

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        if dt1 and dt2:
            query_dict = {"shop_id":sid, "dt1":dt1.strftime("%Y%m%d"), "dt2":dt2.strftime("%Y%m%d"), "sdate":sdate_str, "edate":edate_str}
        else:
            query_dict = {"shop_id":sid, "dt1":sdate_str, "dt2":edate_str, "sdate":sdate_str, "edate":edate_str}
        result_list = []
        sql_ids = [7391,7392,7393,7394,7395]
        index = int(sid) % 5
        sql_id = sql_ids[index]
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        result_list.extend(ret)
        word_set = StringTools.load_word_set()
        for item in result_list:
            query = urllib.unquote(item['query'])
            query = urllib.unquote(query)
            item['query'] = StringTools.keyword_decode(query, word_set)
            item['query'] = item['query'].replace('+', ' ')
        
        return result_list

    @classmethod
    def get_test_wc_web_log(cls, sid, sdate, edate):
        """获取测试无线web_log"""

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":sid, "dt":sdate_str, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 6612
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret

    @classmethod
    def get_pc_schedule_rpt(cls, sid, sdate, edate):

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":sid, "dt1":sdate_str, "dt2":edate_str}
        result_list = []

        sql_id = 7825 
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret
    
    @classmethod
    def get_sid_keyword_query_report(cls, sid, sdate, edate, dt1=None, dt2=None, flag='all'):
        """获取关键词_query报表"""

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        if dt1 and dt2:
            query_dict = {"shop_id":sid, "dt1":dt1.strftime("%Y%m%d"), "dt2":dt2.strftime("%Y%m%d"), "sdate":sdate_str, "edate":edate_str}
        else:
            query_dict = {"shop_id":sid, "dt1":sdate_str, "dt2":edate_str, "sdate":sdate_str, "edate":edate_str}
        
        result_list = []

        if flag == "all" or flag == "pc":
            sql_id = 7387 if sid % 2 == 0 else 7389
            ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
            result_list.extend(ret)

        if flag == "all" or flag == "wx":
            sql_id = 7388 if sid % 2 == 0 else 7390
            ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
            result_list.extend(ret)
        
        word_set = StringTools.load_word_set()
        for item in result_list:
            keyword = urllib.unquote(item['keyword'])
            keyword = urllib.unquote(keyword)
            query = urllib.unquote(item['query'])
            query = urllib.unquote(query)

            item['keyword'] = StringTools.keyword_decode(keyword, word_set)
            item['keyword'] = item['keyword'].replace('+', ' ')
            item['query'] = StringTools.keyword_decode(query, word_set)
            item['query'] = item['query'].replace('+', ' ')
        
        return result_list

    @classmethod
    def get_uniq_query(cls, result_list):
        uniq_dict = {}
        for query in result_list:
            key = query['thedate']+query['auction_id']+query.get('keyword','')+query['query']+query['buyer_id']
            uniq_query = uniq_dict.get(key,{})
            if not uniq_query:
                uniq_dict[key] = query
            else:
                if int(query.get('gmv_auction_num',0)) > int(uniq_query.get('gmv_auction_num',0)):
                    uniq_dict[key] = query
        
        result_list = uniq_dict.values()
        return result_list

    @classmethod
    def get_query_match_scope(cls, item):
        """获取query_dict匹配方式"""

        keyword = item['keyword'].replace(' ','')
        query = item['query'].replace(' ', '')

        keyword = sorted(keyword)
        keyword = ''.join(keyword)
        query = sorted(query)
        query = ''.join(query)

        if keyword == query:
            return 1

        if keyword.find('_') != -1:
            return -1

        return 4


def get_shop(shop_id):
    date = datetime.datetime.now() - datetime.timedelta(days=1)
    ret = ClouddataMbpDataGet.get_sid_keyword_query_report(shop_id, date, date)
    for item in ret:
        for key in ['auction_id', 'gmv_auction_num','alipay_trade_amt','pay_status','gmv_time','alipay_time','orderdate']:
            item[key] = item.get(key, '')
        item['match_scope'] = ClouddataMbpDataGet.get_query_match_scope(item)
        #print "%(thedate)s,%(orderdate)s,%(shop_id)s,%(buyer_id)s,%(keyword)s,%(query)s,%(url_title)s,%(auction_id)s,%(gmv_auction_num)s,%(alipay_trade_amt)s,%(pay_status)s,%(gmv_time)s,%(alipay_time)s" % item
        print "%(keyword)s,%(query)s,%(match_scope)s,%(auction_id)s,%(gmv_auction_num)s" % item
    return len(ret)

if __name__ == '__main__':
    shop_id = int(sys.argv[1])
    #print "thedate,orderdate,shop_id,buyer_id,keyword,query,url_title,auction_id,gmv_auction_num,alipay_trade_amt,pay_status,gmv_time,alipay_time"
    sdate = datetime.datetime.now() - datetime.timedelta(days=1)
    edate = datetime.datetime.now() 
    #res = ClouddataMbpDataGet.get_sid_nosearch_query_report(shop_id,sdate,edate)
    #print 'start_time:',datetime.datetime.now()
    #
    #dt = datetime.datetime.now()-datetime.timedelta(days=1)
    #edt = dt-datetime.timedelta(days=6)
    #sdate = dt-datetime.timedelta(days=2)
    #res = ClouddataMbpDataGet.get_sid_keyword_query_report(shop_id, sdate, dt, dt, dt)
    #
    #while dt > edt:
    #    dt = dt-datetime.timedelta(days=1)
    #    sdate = dt-datetime.timedelta(days=2)
    #    res.extend(ClouddataMbpDataGet.get_sid_keyword_query_report(shop_id, sdate, sdate, dt, dt))

    #res = ClouddataMbpDataGet.get_uniq_query(res)
    res = ClouddataMbpDataGet.get_pc_schedule_rpt(shop_id,sdate, edate)
    #print 'end_time:',datetime.datetime.now()
    sum_click = 0
    sum_pay = 0
    for item in res:
        sum_click += int(item['click'])
        sum_pay += int(item['pay'])
        print item

    print 'sum_click:',sum_click
    print 'sum_pay:',sum_pay
