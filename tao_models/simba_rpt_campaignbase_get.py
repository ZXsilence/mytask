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
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaRptCampaignbaseGetRequest
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class SimbaRptCampaignbaseGet(object):
    
    @classmethod
    @tao_api_exception()
    def get_yesterday_rpt_campbase_list(cls, nick, campaign_id, search_type, source):
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        req = SimbaRptCampaignbaseGetRequest()
        req.nick = nick
        req.start_time = str(yesterday)
        req.end_time = str(yesterday)
        req.campaign_id = campaign_id
        req.source = source
        req.search_type = search_type   
        soft_code = None
        keys_int  =["click","impressions"]
        keys_float = ["cpm","avgpos","ctr","cost"]
        rsp = ApiService.execute(req,nick,soft_code)
        l = json.loads(rsp.rpt_campaign_base_list.lower())
        if l == {}:
            l = []
        if isinstance(l, dict):
            raise ErrorResponseException(code=l['code'], msg=l['msg'], sub_code=l['sub_code'], sub_msg=l['sub_msg'])
        for rpt in l:
            rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')
        return change2num(change_obj_to_dict_deeply(l))

    @classmethod
    @tao_api_exception()
    def get_camp_rpt_list_by_date(cls, nick, campaign_id, search_type, source, start_date, end_date):
        rpt_list = []
        date_list = split_date(start_date,end_date)
        for  item in date_list:
            rpt_list.extend(cls._get_camp_rpt_list_by_date(nick, campaign_id, search_type, source, item[0],item[1]))
        return rpt_list

    @classmethod
    @tao_api_exception()
    def _get_camp_rpt_list_by_date(cls, nick, campaign_id, search_type, source, start_date, end_date):
        req = SimbaRptCampaignbaseGetRequest()
        keys_int  =["click","impressions"]
        keys_float = ["cpm","avgpos","ctr","cost"]
        req.nick = nick
        req.campaign_id = campaign_id
        req.start_time = datetime.datetime.strftime(start_date, '%Y-%m-%d')
        req.end_time = datetime.datetime.strftime(end_date, '%Y-%m-%d')
        req.source = source
        req.search_type = search_type
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        l = json.loads(rsp.rpt_campaign_base_list.lower())
        if l == {}:
            l = []
        if isinstance(l, dict):
            raise ErrorResponseException(code=l['code'], msg=l['msg'], sub_code=l['sub_code'], sub_msg=l['sub_msg'])
        for rpt in l:
            rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')
        return change2num(change_obj_to_dict_deeply(l))


        
    @classmethod
    def get_campaign_base_accumulate(cls, nick, campaign_id, search_type, source, sdate, edate):
        rpt_base_list = SimbaRptCampaignbaseGet.get_camp_rpt_list_by_date(
                nick, int(campaign_id), search_type, source, sdate, edate)
        cost_accumlate = 0
        click_accumlate = 0
        impression_accumlate = 0
        for base in rpt_base_list:
            if not(type(base) == type ({}) and base.has_key('cost') 
                    and base.has_key('click') and base.has_key('impressions')):
                continue
            cost_accumlate += int(base['cost'])
            click_accumlate += int(base['click'])
            impression_accumlate += int(base['impressions'])

        return {'cost':cost_accumlate, 'click':click_accumlate, 'impression':impression_accumlate}

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


if __name__ == '__main__':
    nick = '沃尔盾家居专营店'
    campaign_id = 11219137 
    adgroup_id = 604426910 
    search_type = 'SEARCH,CAT'
    source = '1,2'
    start_time = datetime.datetime.now() - datetime.timedelta(days=10)
    end_time = datetime.datetime.now() - datetime.timedelta(days=1)
    try_list = SimbaRptCampaignbaseGet.get_camp_rpt_list_by_date(nick, campaign_id, search_type, source, start_time, end_time)
    print try_list


