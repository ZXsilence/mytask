# coding=utf8
"""
Created on 2017-5-2
@author: yeyuqiu
"""

import sys
import os
import logging.config


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ZuanshiBannerAdgroupStatusRequest
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class ZuanshiAdgroupStatus(object):

    @classmethod
    @tao_api_exception()
    def modify_adgroup_status(cls, nick, campaign_id, adgroup_id_list, status, soft_code='YZB'):
        req = ZuanshiBannerAdgroupStatusRequest()
        # if len(adgroup_id_list) > 20:
        #     raise Exception('参数adgroup_id_list最大列表长度：20')
        req.campaign_id = campaign_id
        req.adgroup_id_list = ','.join(map(str, adgroup_id_list))
        req.status = status
        rsp = ApiService.execute(req, nick, soft_code)
        return change_obj_to_dict_deeply(rsp.result)


if __name__ == '__main__':
    nick = '优美妮旗舰店'
    campaign_id = 217069448
    adgroup_id_list = [217061436]
    status = 1
    result = ZuanshiAdgroupStatus.modify_adgroup_status(nick, campaign_id, adgroup_id_list, status, 'YZB')
    print result
