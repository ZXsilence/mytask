#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import logging
import logging.config
import json
import datetime
from copy import deepcopy


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaRtrptBidwordGetRequest 
from tao_models.common.decorator import  tao_api_exception, rt_check_retry
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num, KEYS_INT, KEYS_FLOAT, KEYS_RT

logger = logging.getLogger(__name__)

class SimbaRtRptBidwordGet(object):
    
    @classmethod
    def get_bidword_rt_rpt_list(cls, nick, campaign_id, adgroup_id, the_date,source="SUMMARY"):
        """
        获取关键词实时报表
        """
        keywords_rpt_list = cls.get_bidword_rt_detail_rpt_list(nick, campaign_id, adgroup_id, the_date,source)
        keywords_rpt_dict = {}
        for keyword_rpt in keywords_rpt_list:
            keyword_id = keyword_rpt['keyword_id']
            if not keywords_rpt_dict.has_key(keyword_id):
                keywords_rpt_dict[keyword_id] = keyword_rpt
            else:
                sum_keyword_rpt = keywords_rpt_dict[keyword_id]
                for key in keyword_rpt:
                    if key not in KEYS_INT and key not in KEYS_FLOAT:
                        continue
                    if not sum_keyword_rpt.has_key(key):
                        sum_keyword_rpt[key] = keyword_rpt[key]
                    else:
                        sum_keyword_rpt[key] += keyword_rpt[key]
        
        for keyword_rpt in keywords_rpt_dict.values():
            keyword_rpt['cpc'] = 0 if keyword_rpt['click'] <= 0 else\
                keyword_rpt['cost'] / keyword_rpt['click']
            keyword_rpt['ctr'] = 0 if keyword_rpt['impressions'] <= 0 else\
                100.0*keyword_rpt['click'] / keyword_rpt['impressions']
            keyword_rpt['coverage'] = 0 if keyword_rpt['click'] <= 0 else \
                100.0*(keyword_rpt['directtransactionshipping'] + \
                     keyword_rpt['indirecttransactionshipping']) / keyword_rpt['click']
            keyword_rpt['cpm'] = 0 if keyword_rpt['impressions'] <= 0 else\
                1000.0*keyword_rpt['cost'] / keyword_rpt['impressions']
            keyword_rpt['roi'] = 0 if keyword_rpt['cost'] <= 0 else\
                (keyword_rpt['directtransaction'] + keyword_rpt['indirecttransaction']) \
                / float(keyword_rpt['cost'])

        keywords_rpt_list = keywords_rpt_dict.values()
        return keywords_rpt_list
    
    @classmethod
    @rt_check_retry()
    @tao_api_exception()
    def get_bidword_rt_detail_rpt_list(cls, nick, campaign_id, adgroup_id, the_date,source="SUMMARY"):
        """
        获取关键词实时报表,分来源和类型
        """
        req = SimbaRtrptBidwordGetRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.adgroup_id = adgroup_id
        req.the_date = datetime.datetime.strftime(the_date, '%Y-%m-%d')

        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        rpt_list = rsp.results
        if not rpt_list:
            return []

        keywords_rpt_list = change2num(change_obj_to_dict_deeply(rpt_list))
        for keyword_rpt in keywords_rpt_list:
            for key in KEYS_RT:
                if not keyword_rpt.has_key(key):
                    keyword_rpt[key] = 0
            keyword_rpt['campaign_id'] = int(keyword_rpt['campaignid'])
            keyword_rpt['adgroup_id'] = int(keyword_rpt['adgroupid'])
            keyword_rpt['keyword_id'] = int(keyword_rpt['bidwordid'])
            keyword_rpt['impressions'] = keyword_rpt.get('impression',0)
            keyword_rpt['cvr'] = keyword_rpt.get('coverage',0)
        keywords_rpt_dict = {}
        for keyword_rpt in keywords_rpt_dict:
            if not keywords_rpt_dict.has_key(keyword_rpt['source']):
                keywords_rpt_dict[keyword_rpt['source']] = [keyword_rpt]
            else:
                keywords_rpt_dict[keyword_rpt['source']].append(keyword_rpt)
        if source == "SUMMARY":
            return keywords_rpt_list
        else:
            return keywords_rpt_dict.get(keyword_rpt['source'],[])
        return keywords_rpt_list


if __name__ == '__main__':
    nick = sys.argv[1]
    campaign_id = int(sys.argv[2])
    adgroup_id = int(sys.argv[3])
    keyword_id = int(sys.argv[4])
    the_date = datetime.datetime.now()
    rpt_list = SimbaRtRptBidwordGet.get_bidword_rt_rpt_list(nick, campaign_id, adgroup_id, the_date)
    for rpt in rpt_list:
        if rpt['keyword_id'] == keyword_id:
            print rpt
        
