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
from TaobaoSdk.Request.SimbaRptCampaignbaseGetRequest import SimbaRptCampaignbaseGetRequest
from TaobaoSdk.Exceptions.ErrorResponseException import ErrorResponseException

logger = logging.getLogger(__name__)

class SimbaRptCampaignbaseGet(object):
    """
    """
    @classmethod
    @tao_api_exception(6)
    def _get_rpt_campaignbase_list(cls, nick, campaign_id, start_time, end_time, search_type, source, access_token, subway_token, page_no):
        """
        Notes:
                because of taobao API access-times limit,so we recommend that (end_time - start_time) do not more than a day
        """

        req = SimbaRptCampaignbaseGetRequest()
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
            subbase_list = json.loads(rsp.rpt_campaign_base_list)
        except Exception, data:
            raise JsonDecodeException('json schema exception')
        return subbase_list

    @classmethod
    def get_rpt_campaignbase_list(cls, nick, campaign_id, start_time, end_time, search_type, source, access_token, subway_token):
        page_no = 1
        base_list = []
        while True:  
            subbase_list =  SimbaRptCampaignbaseGet._get_rpt_campaignbase_list(\
                    nick, campaign_id, start_time, end_time, search_type,\
                    source, access_token, subway_token, page_no)
            base_list.extend(subbase_list)
            if len(subbase_list) < 500:
                break
            page_no += 1
        return base_list
    
    @classmethod
    def merge_base_list(cls, base_list):
        cost_accumlate = 0
        click_accumlate = 0
        impression_accumlate = 0
        for base in base_list:
            try:
                cost_accumlate += int(base['cost'])
                click_accumlate += int(base['click'])
                impression_accumlate += int(base['impressions'])
            except Exception, data:
                pass

        return {'impression':impression_accumlate, 'click':click_accumlate, 'cost':cost_accumlate, \
                'cpc':int(cost_accumlate/(click_accumlate+0.0000001)), \
                'cpm':int(cost_accumlate/(impression_accumlate+0.0000001)*1000), \
                }


    @classmethod
    @tao_api_exception()
    def get_yesterday_rpt_campaignbase_list(cls, nick,  campaign_id, search_type, source, access_token, subway_token):
        start_date = datetime.date.today() - datetime.timedelta(days=1)
        end_date = datetime.date.today() - datetime.timedelta(days=1)
        base_list = cls.get_rpt_campaignbase_list(nick, campaign_id, start_date, end_date, \
                search_type, source, access_token, subway_token)
        base_rpt = cls.merge_base_list(base_list)
        return base_rpt
        
    @classmethod
    @tao_api_exception()
    def get_last_week_rpt_campaignbase_list(cls, nick, campaign_id, search_type, source, access_token, subway_token):
        start_date = datetime.date.today() - datetime.timedelta(days=8)
        end_date = datetime.date.today() - datetime.timedelta(days=1)
        base_list = cls.get_rpt_campaignbase_list(nick, campaign_id, start_date, end_date, \
                search_type, source, access_token, subway_token)
        base_rpt = cls.merge_base_list(base_list)
        return base_rpt
        
    @classmethod
    @tao_api_exception()
    def get_last_month_rpt_campaignbase_list(cls, nick, campaign_id, search_type, source, access_token, subway_token):
        start_date = datetime.date.today() - datetime.timedelta(days=30)
        end_date = datetime.date.today() - datetime.timedelta(days=1)
        base_list = cls.get_rpt_campaignbase_list(nick, campaign_id, start_date, end_date, \
                search_type, source, access_token, subway_token)
        base_rpt = cls.merge_base_list(base_list)
        return base_rpt

    @classmethod
    @tao_api_exception()
    def get_rpt_campaignbase_list_since_date(cls, nick, campaign_id, search_type, source, access_token, subway_token, start_time):
        end_date = datetime.date.today() - datetime.timedelta(days=1)
        base_list = cls.get_rpt_campaignbase_list(nick, campaign_id, start_time, end_date,\
                search_type, source, access_token, subway_token)
        base_rpt = cls.merge_base_list(base_list)
        return base_rpt
        

if __name__ == '__main__':
    nick = '极浦国际电工'
    campaign_id = '5805854'
    access_token = '6202227ffc9bdcbe25b823d581776a75beegid45afe1932698826726'
    subway_token = '1103827648-27455454-1352119032251-77a5aea6'

    try_list = SimbaRptCampaignbaseGet.get_yesterday_rpt_campaignbase_list(nick, campaign_id, 'SEARCH,CAT', '1,2', access_token, subway_token)
    print try_list
        
    try_list = SimbaRptCampaignbaseGet.get_last_week_rpt_campaignbase_list(nick, campaign_id, 'SEARCH,CAT', '1,2', access_token, subway_token)
    print try_list
        
    try_list = SimbaRptCampaignbaseGet.get_last_month_rpt_campaignbase_list(nick, campaign_id, 'SEARCH,CAT', '1,2', access_token, subway_token)
    print try_list
       

