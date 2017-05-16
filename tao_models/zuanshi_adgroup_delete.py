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

from TaobaoSdk import ZuanshiBannerAdgroupDeleteRequest
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply, slice_list

logger = logging.getLogger(__name__)


class ZuanshiAdgroupDelete(object):

    @classmethod
    @tao_api_exception()
    def delete_adgroup(cls, nick, campaign_id, adgroup_id_list, soft_code='YZB'):
        req = ZuanshiBannerAdgroupDeleteRequest()
        req.campaign_id = campaign_id
        success_id_list = []
        failed_id_list = []
        for chunk in slice_list(adgroup_id_list, 20):
            # 参数adgroup_id_list最大列表长度：20
            req.adgroup_id_list = ','.join(map(str, chunk))
            rsp = ApiService.execute(req, nick, soft_code)
            result = change_obj_to_dict_deeply(rsp.result)
            if result['success']:
                success_id_list.extend(chunk)
            else:
                failed_id_list.extend(chunk)
        result = {
            'success': False if failed_id_list else True,
            'success_list': success_id_list,
            'failed_list': failed_id_list
        }
        return result


if __name__ == '__main__':
    nick = '优美妮旗舰店'
    campaign_id = 217069448
    adgroup_id_list = [217061436]
    result = ZuanshiAdgroupDelete.delete_adgroup(nick, campaign_id, adgroup_id_list, 'YZB')
    print result
