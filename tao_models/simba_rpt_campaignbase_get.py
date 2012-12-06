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
    logging.config.fileConfig('conf/consolelogger.conf')

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception
from tao_models.common.exceptions import  TBDataNotReadyException
from TaobaoSdk.Request.SimbaRptCampaignbaseGetRequest import SimbaRptCampaignbaseGetRequest
from TaobaoSdk.Exceptions.ErrorResponseException import ErrorResponseException

logger = logging.getLogger(__name__)

class SimbaRptCampaignbaseGet(object):
    ''
    @classmethod
    @tao_api_exception()
    def get_yesterday_rpt_campbase_list(cls, nick, campaign_id, search_type, source, access_token, subway_token):
        ''
        yesterday = datetime.date.today() - datetime.timedelta
        req = SimbaRptCampaignbaseGetRequest()
        req.nick = nick
        req.start_time = str(yesterday)
        req.end_time = str(yesterday)
        req.campaign_id = campaign_id
        req.source = source
        req.search_type = search_type   
        req.subway_token = subway_token
        
        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        l = json.loads(rsp.rpt_campaign_base_list)
        return l
    
    @classmethod
    @tao_api_exception()
    def get_camp_rpt_list_by_date(cls, nick, campaign_id, search_type, source, start_date, end_date, access_token, subway_token):
        ''
        req = SimbaRptCampaignbaseGetRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.start_time = datetime.datetime.strftime(start_date, '%Y-%m-%d')
        req.end_time = datetime.datetime.strftime(end_date, '%Y-%m-%d')
        req.source = source
        req.search_type = search_type
        req.subway_token = subway_token
        
        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        l = json.loads(rsp.rpt_campaign_base_list)
        return l
        
        
        
        
        
        
        
        
