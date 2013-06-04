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
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('21065688', '74aecdce10af604343e942a324641891')
    #logging.config.fileConfig('conf/consolelogger.conf')
    
from TaobaoSdk.Request.SimbaRptCampaigneffectGetRequest import SimbaRptCampaigneffectGetRequest
from TaobaoSdk.Exceptions.ErrorResponseException import ErrorResponseException
from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception
from tao_models.common.exceptions import  TBDataNotReadyException
#logger = logging.getLogger(__name__)

class SimbaRptCampaigneffectGet(object):
    ''
    @classmethod
    @tao_api_exception()
    def get_yesterday_rpt_campeffect_list(cls, nick, campaign_id, search_type, source, access_token, subway_token):
        ''
        yesterday = datetime.date.today() - datetime.timedelta
        req = SimbaRptCampaigneffectGetRequest()
        req.nick = nick
        req.start_time = str(yesterday)
        req.end_time = str(yesterday)
        req.campaign_id = campaign_id
        req.source = source
        req.search_type = search_type   
        req.subway_token = subway_token
        
        rsp = tao_model_settings.taobao_client.execute(req, access_token)
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        l = json.loads(rsp.rpt_campaign_effect_list.lower())
        if l == {}:
            l = []
        if isinstance(l, dict):
            raise ErrorResponseException(code=l['code'], msg=l['msg'], sub_code=l['sub_code'], sub_msg=l['sub_msg'])

        for rpt in l:
            rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')

        return l
    
    @classmethod
    @tao_api_exception()
    def get_camp_rpt_list_by_date(cls, nick, campaign_id, search_type, source, start_date, end_date, access_token, subway_token):
        ''
        req = SimbaRptCampaigneffectGetRequest()
        req.nick = nick
        req.start_time = datetime.datetime.strftime(start_date, '%Y-%m-%d')
        req.end_time = datetime.datetime.strftime(end_date, '%Y-%m-%d')

        req.campaign_id = campaign_id
        req.source = source
        req.search_type = search_type   
        req.subway_token = subway_token
        
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        l = json.loads(rsp.rpt_campaign_effect_list.lower())
        if l == {}:
            l = []
        if not isinstance(l, list) and  l.has_key('code') and l['code'] == 15:
            raise TBDataNotReadyException(rsp.rpt_campaign_effect_list)
        for rpt in l:
            rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')
        return l
        
    @classmethod
    def get_campaign_effect_accumulate(cls, nick, campaign_id, search_type, source, sdate, edate
            , access_token, subway_token):
        rpt_effect_list = SimbaRptCampaigneffectGet.get_camp_rpt_list_by_date(
                nick, int(campaign_id), search_type, source, sdate, edate, access_token, subway_token)
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
    nick = 'dong笑口常开'
    access_token = '6201514d95ad5d2ae207fcegc017f3dfdd347661c4ef076314964732'
    subway_token = '1102875020-14926241-1365325223844-b7c4c660'
    campaign_id = '3656522'
    sdate = datetime.datetime.now() - datetime.timedelta(days=18)
    edate = datetime.datetime.now() - datetime.timedelta(days=1)
    print SimbaRptCampaigneffectGet.get_campaign_effect_accumulate(nick, campaign_id, 'SEARCH,CAT,NOSEARCH', '1,2'
            , sdate, edate, access_token, subway_token)
