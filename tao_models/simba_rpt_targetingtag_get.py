#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2016-08-05 10:39
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

from TaobaoSdk.Request.SimbaRptTargetingtagGetRequest import SimbaRptTargetingtagGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num



class SimbaRptTargetingtagGet(object):
    
    @classmethod
    @tao_api_exception()
    def get_get_adgroup_crowd_rpt(cls,nick,campaign_id,adgroup_id,sdate,edate,source):
        req = SimbaRptTargetingtagGetRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.adgroup_id = adgroup_id
        req.start_time = sdate.strftime("%Y-%m-%d")
        req.end_time = edate.strftime("%Y-%m-%d")
        req.traffic_type = source 
        rsp = ApiService.execute(req,nick,"SYB")
        return change2num(change_obj_to_dict_deeply(rsp.results))


if __name__ == '__main__':
    import datetime
    nick = "qq199711425" 
    campaign_id = 2935632 
    adgroup_ids = [681842595]
    edate = datetime.datetime.now() - datetime.timedelta(days=1)
    sdate = edate - datetime.timedelta(days=6)
    res = SimbaRptTargetingtagGet.get_get_adgroup_crowd_rpt(nick,campaign_id,adgroup_ids[0],sdate,edate,'1,2,4,5')
    res.sort(key =lambda item:item['impression'])
    for item in res:
        print item

