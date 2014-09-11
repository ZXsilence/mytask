# -*- coding: utf-8 -*-
'''
Created on 2012-11-5

@author: dk
'''
import sys
import os
import json
import datetime
import logging
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')
    
from TaobaoSdk import SimbaRptCampaigneffectGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaRptCampaigneffectGet(object):

    @classmethod
    @tao_api_exception()
    def get_camp_rpt_list_by_date(cls, nick, campaign_id, search_type, source, start_date, end_date):
        req = SimbaRptCampaigneffectGetRequest()
        req.nick = nick
        req.start_time = datetime.datetime.strftime(start_date, '%Y-%m-%d')
        req.end_time = datetime.datetime.strftime(end_date, '%Y-%m-%d')
        req.campaign_id = campaign_id
        req.source = source
        req.search_type = search_type   
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        l = json.loads(rsp.rpt_campaign_effect_list.lower())
        if l == {}:
            l = []
        #if not isinstance(l, list) and  l.has_key('code') and l['code'] == 15:
        #    raise TBDataNotReadyException(rsp.rpt_campaign_effect_list)
        for rpt in l:
            rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')
        return change_obj_to_dict_deeply(l)
        
    @classmethod
    def get_campaign_effect_accumulate(cls, nick, campaign_id, search_type, source, sdate, edate):
        rpt_effect_list = SimbaRptCampaigneffectGet.get_camp_rpt_list_by_date(
                nick, int(campaign_id), search_type, source, sdate, edate)
        pay_accumlate = 0 
        pay_count_accumlate = 0 
        fav_accumlate = 0 
        for effect in rpt_effect_list:
            if not(effect.has_key('directpay') and effect.has_key('indirectpay') \
                    and effect.has_key('indirectpaycount') and effect.has_key('directpaycount') \
                    and effect.has_key('favshopcount') and effect.has_key('favitemcount') \
                    ):  
                continue
            for key in effect.keys():
                if effect[key] == None:
                    effect[key] = 0
            pay_accumlate += int(effect['indirectpay'])
            pay_accumlate += int(effect['directpay'])
            pay_count_accumlate += int(effect['indirectpaycount'])
            pay_count_accumlate += int(effect['directpaycount'])
            fav_accumlate += int(effect['favitemcount'])
            fav_accumlate += int(effect['favshopcount']) 
        return {'pay':pay_accumlate, 'pay_count':pay_count_accumlate, 'fav':fav_accumlate}


if __name__ == "__main__":
    nick = 'chinchinstyle'
    campaign_id = 3367748
    adgroup_id = 336844923
    search_type = 'SEARCH,CAT'
    source = '1,2'
    start_time = datetime.datetime.now() - datetime.timedelta(days=10)
    end_time = datetime.datetime.now() - datetime.timedelta(days=1)
    print SimbaRptCampaigneffectGet.get_campaign_effect_accumulate(nick, campaign_id, search_type, source, start_time, end_time)
