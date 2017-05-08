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
    def create_banner_campaign(cls, soft_code = 'YZB', nick, workday, weekend, type, name, area_id_list, speed_type, day_budget, start_time, end_time):
        req = ZuanshiBannerCampaignCreateRequest()
        req.workday = ','.join([str(day) for day in workday])
        req.weekend = ','.join([str(day) for day in weekend])
        req.type = type
        req.name = name
        req.area_id_list = area_id_list
        req.speed_type = speed_type
        req.day_budget = day_budget
        req.start_time = start_time
        req.end_time = end_time
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.result).get('id')
