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

from TaobaoSdk import SimbaRtrptCreativeGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num, KEYS_INT, KEYS_FLOAT, KEYS_RT

logger = logging.getLogger(__name__)

class SimbaRtRptCreativeGet(object):

    @classmethod
    def get_creative_rt_rpt_list(cls, nick, campaign_id, adgroup_id, the_date,source="SUMMARY"):
        """
        获取创意实时报表
        """
        creatives_rpt_list = cls.get_creative_rt_detail_rpt_list(nick, campaign_id, adgroup_id, the_date,source)
        creatives_rpt_dict = {}
        for creative_rpt in creatives_rpt_list:
            creative_id = creative_rpt['creative_id']
            if not creatives_rpt_dict.has_key(creative_id):
                creatives_rpt_dict[creative_id] = creative_rpt
            else:
                sum_creative_rpt = creatives_rpt_dict[creative_id]
                for key in creative_rpt:
                    if key not in KEYS_INT and key not in KEYS_FLOAT:
                        continue
                    if not sum_creative_rpt.has_key(key):
                        sum_creative_rpt[key] = creative_rpt[key]
                    else:
                        sum_creative_rpt[key] += creative_rpt[key]
        
        for creative_rpt in creatives_rpt_dict.values():
            creative_rpt['cpc'] = 0 if creative_rpt['click'] <= 0 else\
                creative_rpt['cost'] / creative_rpt['click']
            creative_rpt['ctr'] = 0 if creative_rpt['impressions'] <= 0 else\
                100.0*creative_rpt['click'] / creative_rpt['impressions']
            creative_rpt['coverage'] = 0 if creative_rpt['click'] <= 0 else \
                100.0*(creative_rpt['directtransactionshipping'] + \
                     creative_rpt['indirecttransactionshipping']) / creative_rpt['click']
            creative_rpt['cpm'] = 0 if creative_rpt['impressions'] <= 0 else\
                1000.0*creative_rpt['cost'] / creative_rpt['impressions']
            creative_rpt['roi'] = 0 if creative_rpt['cost'] <= 0 else\
                (creative_rpt['directtransaction'] + creative_rpt['indirecttransaction']) \
                / float(creative_rpt['cost'])

        creatives_rpt_list = creatives_rpt_dict.values()
        return creatives_rpt_list
    
    @classmethod
    @tao_api_exception()
    def get_creative_rt_detail_rpt_list(cls, nick, campaign_id, adgroup_id, the_date,source="SUMMARY"):
        """
        获取创意实时报表,分来源和类型
        """
        req = SimbaRtrptCreativeGetRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.adgroup_id = adgroup_id 
        req.the_date = datetime.datetime.strftime(the_date, '%Y-%m-%d')

        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        l = rsp.results
        if not l:
            l = []

        creatives_rpt_list = change2num(change_obj_to_dict_deeply(l))
        for creative_rpt in creatives_rpt_list:
            for key in KEYS_RT:
                if not creative_rpt.has_key(key):
                    creative_rpt[key] = 0
            creative_rpt['campaign_id'] = int(creative_rpt['campaignid'])
            creative_rpt['adgroup_id'] = int(creative_rpt['adgroupid'])
            creative_rpt['creative_id'] = int(creative_rpt['creativeid'])
            creative_rpt['impressions'] = creative_rpt.get('impression',0)
        creatives_rpt_dict = {}
        for creative_rpt in creatives_rpt_list:
            if not creatives_rpt_dict.has_key(creative_rpt['source']):
                creatives_rpt_dict[creative_rpt['source']]= [creative_rpt]
            else:
                creatives_rpt_dict[creative_rpt['source']].append(creative_rpt)
        if source == "SUMMARY":
            return creatives_rpt_list
        else:
            return creatives_rpt_dict.get(source,[])

if __name__ == '__main__':
    nick = sys.argv[1]
    campaign_id = int(sys.argv[2])
    adgroup_id = int(sys.argv[3])
    the_date = datetime.datetime.now()
    rpt_list = SimbaRtRptCreativeGet.get_creative_rt_rpt_list(nick, campaign_id, adgroup_id, the_date)
    for rpt in rpt_list:
        print rpt
        
