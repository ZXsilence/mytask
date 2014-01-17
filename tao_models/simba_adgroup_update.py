#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import SimbaAdgroupUpdateRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaAdgroupUpdate(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(3)
    def update_adgroup(cls, nick, adgroup_id, default_price, online_status ):

        req = SimbaAdgroupUpdateRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id 
        req.default_price = default_price
        #req.nonsearch_max_price = nonsearch_max_price 
        #req.use_nonsearch_default_price = use_nonsearch_default_price 
        req.online_status = online_status 
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.adgroup)


if __name__ == '__main__':
    nick = 'chinchinstyle'
    adgroup_id = 336844923
    default_price = 11
    online_status = 'online'
    adgroup = SimbaAdgroupUpdate.update_adgroup(nick, adgroup_id, default_price, online_status )
    print adgroup
