#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: lichen
@contact: lichen@maimiaotech.com
@date: 2017-05-03 16:01
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
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ZuanshiBannerCampaignModifyRequest
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class ZuanshiCampaignModify(object):

    @classmethod
    @tao_api_exception()
    def modify_banner_campaign(cls, nick, modify_data, soft_code = 'YZB'):
        req = ZuanshiBannerCampaignModifyRequest()
        req.id = modify_data['id']
        if modify_data.get('name'):
            req.name = modify_data['name']
        if modify_data.get('day_budget'):
            req.day_budget = modify_data['day_budget']
        if modify_data.get('start_time') and modify_data.get('end_time'):
            req.start_time = modify_data['start_time']
            req.end_time = modify_data['end_time']
        if modify_data.get('area_id_list'):
            area_id_list = ','.join(modify_data['area_id_list'])
            req.area_id_list = area_id_list
        if modify_data.get('weekend'):
            req.weekend = ','.join(modify_data['weekend'])
        if modify_data.get('workday'):
            req.workday = ','.join(modify_data['workday'])
        if modify_data.get('type'):
            req.type = modify_data['type']
        if modify_data.get('speed_type'):
            req.speed_type = modify_data['modify_data']
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.result).get('success')

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    modify_data = {}
    modify_data['id'] = 223280585
    modify_data['workday'] = map(lambda x:True, xrange(24))
    modify_data['weekend'] = map(lambda x:True, xrange(24))
    soft_code = 'YZB'
    res = ZuanshiCampaignModify.modify_banner_campaign(nick, modify_data, soft_code)
    print res

