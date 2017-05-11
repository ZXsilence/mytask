# coding=utf8
"""
Created on 2017-5-5
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

from TaobaoSdk import ZuanshiBannerCreativeUnbindRequest
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class ZuanshiCreativeUnbind(object):

    @classmethod
    @tao_api_exception()
    def unbind_creative(cls, nick, campaign_id, adgroup_id, creative_id_list, soft_code='YZB'):
        req = ZuanshiBannerCreativeUnbindRequest()
        if len(creative_id_list) > 20:
            raise Exception('参数creative_id_list最大列表长度：20')
        req.campaign_id = campaign_id
        req.adgroup_id = adgroup_id
        req.creative_id_list = ','.join(map(str, creative_id_list))
        rsp = ApiService.execute(req, nick, soft_code)
        return change_obj_to_dict_deeply(rsp.result)


if __name__ == '__main__':
    nick = '优美妮旗舰店'
    campaign_id = 217069448
    adgroup_id = 217061436
    creative_id_list = [796347600001]
    result = ZuanshiCreativeUnbind.unbind_creative(nick, campaign_id, adgroup_id, creative_id_list, 'YZB')
    print result
