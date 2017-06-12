#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: lichen
@contact: lichen@maimiaotech.com
@date: 2017-05-03 16:54
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

from TaobaoSdk import ZuanshiBannerCampaignDeleteRequest
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class ZuanshiCampaignDelete(object):

    @classmethod
    @tao_api_exception()
    def delete_banner_campaign(cls, nick, delete_id_list, soft_code='YZB'):
        req = ZuanshiBannerCampaignDeleteRequest()
        delete_id_list = ','.join([str(delete_id) for delete_id in delete_id_list])
        req.campaign_id_list = delete_id_list
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.result)

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    soft_code = 'YZB'
    delete_id_list = [225344013]
    res = ZuanshiCampaignDelete.delete_banner_campaign(nick,delete_id_list,soft_code)
    print res
