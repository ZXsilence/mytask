# coding=utf8
'''
Created on 2017-5-5

@author: yeyuqiu
'''

import sys
import os
import logging
import logging.config
import json
import datetime
from copy import deepcopy


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ZuanshiBannerAdgroupAdzoneUnbindRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)


class ZuanshiAdgroupAdzoneUnbind(object):

    @classmethod
    @tao_api_exception()
    def unbind_adzone(cls, nick, campaign_id, adgroup_id, adzone_id_list, soft_code='YZB'):
        req = ZuanshiBannerAdgroupAdzoneUnbindRequest()
        req.campaign_id = campaign_id
        req.adgroup_id = adgroup_id
        req.adzone_id_list = adzone_id_list
        rsp = ApiService.execute(req, nick, soft_code)
        return change_obj_to_dict_deeply(rsp.result)


if __name__ == '__main__':
    nick = '优美妮旗舰店'
    campaign_id = 217069448
    adgroup_id = 217061436
    adzone_id_list = 64400199
    result = ZuanshiAdgroupAdzoneUnbind.unbind_adzone(nick, campaign_id, adgroup_id, adzone_id_list)
    print result
