# -*- coding: utf-8 -*-
'''
Created on 2012-11-5

@author: dk
'''
import sys
import os
import datetime
import logging
import logging.config
import json
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception
from tao_models.common.exceptions import JsonDecodeException
from TaobaoSdk.Request.SimbaRptCampaigneffectGetRequest import SimbaRptCampaigneffectGetRequest
from TaobaoSdk.Exceptions.ErrorResponseException import ErrorResponseException

logger = logging.getLogger(__name__)

class SimbaRptCampaigneffectGet(object):
    """
    """
    @classmethod
    @tao_api_exception(6)
    def _get_rpt_campaigneffect_list(cls, nick, campaign_id, start_time, end_time, search_type, source, access_token, subway_token, page_no):
        """
        Notes:
                because of taobao API access-times limit,so we recommend that (end_time - start_time) do not more than a day
        """

        req = SimbaRptCampaigneffectGetRequest()
        req.nick = nick 
        req.campaign_id = campaign_id
        req.start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d') 
        req.end_time = datetime.datetime.strftime(end_time, '%Y-%m-%d')
        req.search_type = search_type
        req.source = source
        req.subway_token = subway_token
        req.page_no = page_no
        req.page_size = 500
        try:
            rsp = taobao_client.execute(req, access_token)[0]
        except Exception, data:
            raise ErrorResponseException(code=-1, msg='', sub_code=-1, sub_msg='')

        if not rsp.isSuccess():
            logger.info("api failed rsp.code %s", rsp.msg)
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        try:
            subeffect_list = json.loads(rsp.rpt_campaign_effect_list)
        except Exception, data:
            raise JsonDecodeException('json schema exception')
        return subeffect_list

    @classmethod
    def get_rpt_campaigneffect_list(cls, nick, campaign_id, start_time, end_time, search_type, source, access_token, subway_token):
        page_no = 1
        effect_list = []
        while True:  
            subeffect_list =  SimbaRptCampaigneffectGet._get_rpt_campaigneffect_list(\
                    nick, campaign_id, start_time, end_time, search_type,\
                    source, access_token, subway_token, page_no)
            effect_list.extend(subeffect_list)
            if len(subeffect_list) < 500:
                break
            page_no += 1
        return effect_list
    
    @classmethod
    def merge_effect_list(cls, effect_list):
        pay_accumlate = 0
        pay_count_accumlate = 0
        fav_accumlate = 0

        for effect in effect_list:
            try:
                pay_accumlate += int(effect['indirectpay'])
                pay_accumlate += int(effect['directpay'])
                pay_count_accumlate += int(effect['indirectpaycount'])
                pay_count_accumlate += int(effect['directpaycount'])
                fav_accumlate += int(effect['favItemCount'])
                fav_accumlate += int(effect['favShopCount'])
            except :
                pass
            

        return {'pay':pay_accumlate, 'pay_count':pay_count_accumlate, \
                'fav':fav_accumlate, \
                }


    @classmethod
    @tao_api_exception()
    def get_yesterday_rpt_campaigneffect_list(cls, nick,  campaign_id, search_type, source, access_token, subway_token):
        start_date = datetime.date.today() - datetime.timedelta(days=1)
        end_date = datetime.date.today() - datetime.timedelta(days=1)
        effect_list = cls.get_rpt_campaigneffect_list(nick, campaign_id, start_date, end_date, \
                search_type, source, access_token, subway_token)
        effect_rpt = cls.merge_effect_list(effect_list)
        return effect_rpt
        
    @classmethod
    @tao_api_exception()
    def get_last_week_rpt_campaigneffect_list(cls, nick, campaign_id, search_type, source, access_token, subway_token):
        start_date = datetime.date.today() - datetime.timedelta(days=8)
        end_date = datetime.date.today() - datetime.timedelta(days=1)
        effect_list = cls.get_rpt_campaigneffect_list(nick, campaign_id, start_date, end_date, \
                search_type, source, access_token, subway_token)
        effect_rpt = cls.merge_effect_list(effect_list)
        return effect_rpt
        
    @classmethod
    @tao_api_exception()
    def get_last_month_rpt_campaigneffect_list(cls, nick, campaign_id, search_type, source, access_token, subway_token):
        start_date = datetime.date.today() - datetime.timedelta(days=30)
        end_date = datetime.date.today() - datetime.timedelta(days=1)
        effect_list = cls.get_rpt_campaigneffect_list(nick, campaign_id, start_date, end_date, \
                search_type, source, access_token, subway_token)
        effect_rpt = cls.merge_effect_list(effect_list)
        return effect_rpt

    @classmethod
    @tao_api_exception()
    def get_rpt_campaigneffect_list_since_date(cls, nick, campaign_id, search_type, source, access_token, subway_token, start_time):
        end_date = datetime.date.today() - datetime.timedelta(days=1)
        effect_list = cls.get_rpt_campaigneffect_list(nick, campaign_id, start_time, end_date,\
                search_type, source, access_token, subway_token)
        effect_rpt = cls.merge_effect_list(effect_list)
        return effect_rpt
        

if __name__ == '__main__':
    nick = '极浦国际电工'
    campaign_id = '5805854'
    access_token = '6202227ffc9bdcbe25b823d581776a75beegid45afe1932698826726'
    subway_token = '1103827648-27455454-1352119032251-77a5aea6'

    try_list = SimbaRptCampaigneffectGet.get_yesterday_rpt_campaigneffect_list(nick, campaign_id, 'SEARCH,CAT', '1,2', access_token, subway_token)
    print try_list
        
    try_list = SimbaRptCampaigneffectGet.get_last_week_rpt_campaigneffect_list(nick, campaign_id, 'SEARCH,CAT', '1,2', access_token, subway_token)
    print try_list
        
    try_list = SimbaRptCampaigneffectGet.get_last_month_rpt_campaigneffect_list(nick, campaign_id, 'SEARCH,CAT', '1,2', access_token, subway_token)
    print try_list
       

