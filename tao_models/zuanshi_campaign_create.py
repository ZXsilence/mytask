#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: lichen
@contact: lichen@maimiaotech.com
@date: 2017-05-02 17:17
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""


import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ZuanshiBannerCampaignCreateRequest
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class ZuanshiCampaignCreate(object):
    
    @classmethod
    @tao_api_exception()
    def create_banner_campaign(cls, nick, workday, weekend, type, name, area_id_list, speed_type, day_budget, start_time, end_time, soft_code='YZB'):
        req = ZuanshiBannerCampaignCreateRequest()
        req.workday = ','.join([str(day) for day in workday])
        req.weekend = ','.join([str(day) for day in weekend])
        req.type = type
        req.name = name
        req.area_id_list = ','.join([str(area_id) for area_id in area_id_list])
        req.speed_type = speed_type
        req.day_budget = day_budget
        req.start_time = start_time
        req.end_time = end_time
        rsp = ApiService.execute(req,nick,soft_code)
        if not change_obj_to_dict_deeply(rsp.result).get('id'):
            logging.info('%s:%s'%(nick, change_obj_to_dict_deeply(rsp.result).get('message')))
        return change_obj_to_dict_deeply(rsp.result).get('id')

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    soft_code = 'YZB'
    workday = map(lambda x:'true', xrange(24))
    weekend = map(lambda x:'true', xrange(24))
    type = 2
    name = 'carlos_test'
    area_id_list = [1,19,532,39]
    speed_type = 1
    day_budget=110000
    start_time="2017-05-10 00:00:00"
    end_time="2017-05-11 00:00:00"
    res = ZuanshiCampaignCreate.create_banner_campaign(nick, workday, weekend, type, name, area_id_list, speed_type, day_budget, start_time, end_time, soft_code)
    print res
