#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2016-08-05 10:58
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import sys
import os
import logging
import logging.config
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk.Request.SimbaRtrptTargetingtagGetRequest import SimbaRtrptTargetingtagGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply


class SimbaRtrptTargetingtagGet(object):
    
    @classmethod
    def get_get_adgroup_crowd_rpt(cls,nick,campaign_id,adgroup_id,tdate,source):
        req = SimbaRtrptTargetingtagGetRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.adgroup_id = adgroup_id
        req.the_date = tdate.strftime("%Y-%m-%d")
        req.traffic_type = source 
        rsp = ApiService.execute(req,nick,"SYB")
        return change_obj_to_dict_deeply(rsp.results)



if __name__ == '__main__':
    import datetime
    #nick = "麦苗科技001"
    #adgroup_id = 700403273 
    nick = "qq199711425" 
    campaign_id = 2935632 
    adgroup_ids = [681842595]
    now  = datetime.datetime.now()
    edate = now  - datetime.timedelta(days=1)
    sdate = now  - datetime.timedelta(days=7)
    res = SimbaRtrptTargetingtagGet.get_get_adgroup_crowd_rpt(nick,campaign_id,adgroup_ids[0],now,'1,2,4,5')
    for item in res:
        print item

