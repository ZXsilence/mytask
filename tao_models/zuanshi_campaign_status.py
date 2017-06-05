#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: lichen
@contact: lichen@maimiaotech.com
@date: 2017-05-03 19:41
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

from TaobaoSdk import ZuanshiBannerCampaignStatusRequest
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class ZuanshiCampaignStatus(object):

    @classmethod
    @tao_api_exception()
    def modify_banner_campaign_status(cls, nick, modify_campaign_status_data, soft_code='YZB'):
        req = ZuanshiBannerCampaignStatusRequest()
        campaign_id_list = ','.join([str(campaign_id) for campaign_id in modify_campaign_status_data['campaign_id_list']])
        req.campaign_id_list = campaign_id_list
        req.status = modify_campaign_status_data['status']
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.result)


if __name__ == '__main__':
    nick = '优美妮旗舰店'
    soft_code = 'YZB'
    modify_campaign_status_data = {}
    modify_campaign_status_data['campaign_id_list'] = [226674640]
    modify_campaign_status_data['status'] = 9
    res = ZuanshiCampaignStatus.modify_banner_campaign_status(nick, modify_campaign_status_data, soft_code)
    import simplejson as json
    print res



