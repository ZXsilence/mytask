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

from TaobaoSdk import ZuanshiBannerAdgroupModifyRequest
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class ZuanshiAdgroupModify(object):

    @classmethod
    @tao_api_exception()
    def modify_adgroup(cls, nick, id, campaign_id, soft_code='YZB', **kwargs):
        req = ZuanshiBannerAdgroupModifyRequest()
        req.id = id
        req.campaign_id = campaign_id
        for k, v in kwargs.iteritems():
            setattr(req, k, v)
        rsp = ApiService.execute(req, nick, soft_code)
        return change_obj_to_dict_deeply(rsp.result)


if __name__ == '__main__':
    nick = '优美妮旗舰店'
    campaign_id = 217069448
    adgroup_id = 217061436
    params_dict = {'name': '修改名称测试'}
    result = ZuanshiAdgroupModify.modify_adgroup(nick, adgroup_id, campaign_id, 'YZB', params_dict)
    print result
