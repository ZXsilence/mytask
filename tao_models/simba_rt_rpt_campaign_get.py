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

from TaobaoSdk import SimbaRtrptCampaignGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num, KEYS_INT, KEYS_FLOAT, KEYS_RT

logger = logging.getLogger(__name__)

class SimbaRtRptCampaignGet(object):

    @classmethod
    def get_campaign_rt_rpt_list(cls, nick, the_date,source="SUMMARY"):
        """
        获取计划实时报表
        """
        campaigns_rpt_list = cls.get_campaign_rt_detail_rpt_list(nick, the_date,source)
        campaigns_rpt_dict = {}
        for campaign_rpt in campaigns_rpt_list:
            campaign_id = campaign_rpt['campaign_id']
            if not campaigns_rpt_dict.has_key(campaign_id):
                campaigns_rpt_dict[campaign_id] = campaign_rpt
            else:
                sum_campaign_rpt = campaigns_rpt_dict[campaign_id]
                for key in campaign_rpt:
                    if key not in KEYS_INT and key not in KEYS_FLOAT:
                        continue
                    if not sum_campaign_rpt.has_key(key):
                        sum_campaign_rpt[key] = campaign_rpt[key]
                    else:
                        sum_campaign_rpt[key] += campaign_rpt[key]
        
        for campaign_rpt in campaigns_rpt_dict.values():
            campaign_rpt['cpc'] = 0 if campaign_rpt['click'] <= 0 else\
                campaign_rpt['cost'] / campaign_rpt['click']
            campaign_rpt['ctr'] = 0 if campaign_rpt['impressions'] <= 0 else\
                100.0*campaign_rpt['click'] / campaign_rpt['impressions']
            campaign_rpt['cvr'] = 0 if campaign_rpt['click'] <= 0 else \
                100.0*(campaign_rpt['directtransactionshipping'] + \
                     campaign_rpt['indirecttransactionshipping']) / campaign_rpt['click']
            campaign_rpt['cpm'] = 0 if campaign_rpt['impressions'] <= 0 else\
                1000.0*campaign_rpt['cost'] / campaign_rpt['impressions']
            campaign_rpt['roi'] = 0 if campaign_rpt['cost'] <= 0 else\
                (campaign_rpt['directtransaction'] + campaign_rpt['indirecttransaction']) \
                / float(campaign_rpt['cost'])
        campaigns_rpt_list = campaigns_rpt_dict.values()
        return campaigns_rpt_list

    @classmethod
    @tao_api_exception()
    def get_campaign_rt_detail_rpt_list(cls, nick, the_date,source="SUMMARY"):
        """
        获取计划实时报表,分来源和类型
        """
        req = SimbaRtrptCampaignGetRequest()
        req.nick = nick
        req.the_date = datetime.datetime.strftime(the_date, '%Y-%m-%d')

        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        l = rsp.resultss
        if not l:
            l = []
        campaigns_rpt_list = change2num(change_obj_to_dict_deeply(l))
        for campaign_rpt in campaigns_rpt_list:
            for key in KEYS_RT:
                if not campaign_rpt.has_key(key):
                    campaign_rpt[key] = 0
            campaign_rpt['campaign_id'] = int(campaign_rpt['campaignid'])
            campaign_rpt['impressions'] = campaign_rpt.get('impression',0)
            campaign_rpt['cvr'] = campaign_rpt.get('coverage',0)
        campaigns_rpt_dict = {}
        for campaign_rpt in campaigns_rpt_list:
            if not campaigns_rpt_dict.has_key(campaign_rpt['source']):
                campaigns_rpt_dict[campaign_rpt['source']] = [campaign_rpt]
            else:
                campaigns_rpt_dict[campaign_rpt['source']].append(campaign_rpt)
        if source == "SUMMARY":
            return campaigns_rpt_list
        else:
            return campaigns_rpt_dict.get(source,[])



if __name__ == '__main__':
    nick = sys.argv[1]
    campaign_id = int(sys.argv[2])
    the_date = datetime.datetime.now()
    rpt_list = SimbaRtRptCampaignGet.get_campaign_rt_rpt_list(nick, the_date)
    for rpt in rpt_list:
        if rpt['campaign_id'] == campaign_id:
            print rpt
        
