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
from tao_models.common.decorator import  tao_api_exception, ysf_exception
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
    @ysf_exception()
    @tao_api_exception()
    def get_data_from_clouddata(cls, sql_id, query_dict):
        ret = []
        page_count = 0
        while True:
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
        query_dict = {"shop_id":sid, "dt":edate_str, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 6612
        #sql_id = 6335 #pc
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret
    
    @classmethod
    def get_shop_schedule_rpt(cls, sid, sdate, edate):
        #获取店铺分时报表

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":sid, "start_dt":sdate_str, "start_date":sdate_str, "end_dt":edate_str, "end_date":edate_str}
        result_list = []

        sql_id = 104099
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret

    @classmethod
    def get_shop_schedule_sum_rpt(cls, sdate, edate):
        #获取店铺汇总分时报表

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"start_dt":sdate_str, "start_date":sdate_str, "end_dt":edate_str, "end_date":edate_str}
        result_list = []

        sql_id = 104098 
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
    def get_shop_pc_nature_query(cls, sid, sdate, edate):
        """获取店铺pc自然query"""

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":sid, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 104233 
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret
    
    @classmethod
    def get_shop_wx_nature_query(cls, sid, sdate, edate):
        """获取店铺wx自然query"""

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":sid, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id_list = [101426, 101425, 101427, 101428]
        sql_id = sql_id_list[sid%4]
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret
    
    @classmethod
    def get_shop_order(cls, sid, sdate, edate):
        """获取店铺订单"""

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        dt_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":sid, "dt":dt_str, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 6333
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret

    @classmethod
    def get_shop_out_order_d(cls, sid, sdate, edate):
        """获取店铺站外订单日表详情"""

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        dt_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":sid, "dt":dt_str, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 101374 
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret

    @classmethod
    def get_all_pc_schedule_rpt(cls,sdate,edate):
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"dt1":sdate_str, "dt2":edate_str}
        result_list = []

        sql_id = 7842 
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret
    
    @classmethod
    def get_all_wx_schedule_rpt(cls,sdate,edate):
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"dt1":sdate_str, "dt2":edate_str}
        result_list = []

        sql_id = 7861 
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret
    
    @classmethod
    def get_item_traffic_src_info(cls,sdate):
        """获取商品流量来源维度信息"""

        sdate_str = sdate.strftime("%Y%m%d")
        query_dict = {'sdate':sdate_str}
        sql_id = 102915
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret 

    @classmethod
    def get_shop_out_effect_d(cls, sdate):
        """获取店铺站外效果日表"""

        sdate_str = sdate.strftime("%Y%m%d")
        query_dict = {'dt':sdate_str}
        sql_id = 103858 
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret 
    
    @classmethod
    def get_sid_keyword_query_report(cls, sid, sdate, edate, dt1=None, dt2=None, flag='pc'):
        """获取店铺pc付费query报表"""

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

    @classmethod
    def get_item_pc_traffic_info(cls,item_id,dt1=None,dt2=None):
        if not dt1 or not dt2:
            dt2 = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
            dt1 = (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%Y%m%d")
        sql_id = 104421
        query_dict = {"auction_id":item_id,"dt1":dt1,"dt2":dt2}
        res = ClouddataMbpDataGet.get_data_from_clouddata(sql_id,query_dict)
        return res

    @classmethod
    def get_item_comment(cls,item_id,sdate=None,edate=None):
        if not sdate or not edate:
            edate= (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
            sdate= (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%Y%m%d")
        sql_id = 104870
        query_dict = {"auction_id":item_id,"sdate":sdate,"edate":edate}
        res = ClouddataMbpDataGet.get_data_from_clouddata(sql_id,query_dict)
        return res

    @classmethod
    def get_item_asso_info(cls,sid,item_id,dt1=None,dt2=None):
        if not dt1 or not dt2:
            dt2 = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
            dt1 = (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%Y%m%d")
        sql_id_dict = {1:104426,0:104427,2:104428}
        sql_id = sql_id_dict[sid%3]
        query_dict = {"auction_id_1":item_id,"dt1":dt1,"dt2":dt2}
        res = ClouddataMbpDataGet.get_data_from_clouddata(sql_id,query_dict)
        return res

    @classmethod
    def get_shop_traffic_and_trade_info(cls,shop_id,sdate,edate):
        sql_id = 104820
        now = datetime.datetime.now()
        if type(sdate) == type(now):
            query_dict = {'shop_id':shop_id,'sdate':sdate.strftime("%Y%m%d"),'edate':edate.strftime("%Y%m%d")}
        else:
            query_dict = {'shop_id':shop_id,'sdate':sdate,'edate':edate}
        res = ClouddataMbpDataGet.get_data_from_clouddata(sql_id,query_dict)
        return res
    
    @classmethod
    def get_shop_item_traffic_and_trade_info(cls,shop_id,sdate,edate):
        sql_id = 104812
        now = datetime.datetime.now()
        if type(sdate) == type(now):
            query_dict = {'shop_id':shop_id,'sdate':sdate.strftime("%Y%m%d"),'edate':edate.strftime("%Y%m%d")}
        else:
            query_dict = {'shop_id':shop_id,'sdate':sdate,'edate':edate}
        res = ClouddataMbpDataGet.get_data_from_clouddata(sql_id,query_dict)
        return res


def get_shop(shop_id):
    date = datetime.datetime.now() - datetime.timedelta(days=2)
    ret = ClouddataMbpDataGet.get_sid_keyword_query_report(shop_id, date, date)
    for item in ret:
        for key in ['auction_id', 'gmv_auction_num','alipay_trade_amt','pay_status','gmv_time','alipay_time','orderdate']:
            item[key] = item.get(key, '')
        item['match_scope'] = ClouddataMbpDataGet.get_query_match_scope(item)
        #print "%(thedate)s,%(orderdate)s,%(shop_id)s,%(buyer_id)s,%(keyword)s,%(query)s,%(url_title)s,%(auction_id)s,%(gmv_auction_num)s,%(alipay_trade_amt)s,%(pay_status)s,%(gmv_time)s,%(alipay_time)s" % item
        print "%(keyword)s,%(query)s,%(match_scope)s,%(auction_id)s,%(gmv_auction_num)s" % item
    return len(ret)



if __name__ == '__main__':
    edate = datetime.datetime.now() - datetime.timedelta(days=1)
    sdate = datetime.datetime.now() - datetime.timedelta(days=1)
    #shop_id =111069814 
    shop_id = 63078762
    #res = ClouddataMbpDataGet.get_shop_item_traffic_and_trade_info(shop_id,sdate,edate)
    print ClouddataMbpDataGet.get_item_comment(524834187930)
