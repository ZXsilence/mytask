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

from TaobaoSdk import SimbaAdgroupAdgroupcatmatchsGetRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaAdgroupAdgroupcatmatchsGet(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(3)
    def get_adgroup_catmatchs(cls, nick, adgroup_ids):

        adgroup_ids_str = [str(adgroup_id) for adgroup_id in adgroup_ids]
        req = SimbaAdgroupAdgroupcatmatchsGetRequest()
        req.nick = nick
        req.adgroup_ids = ','.join(adgroup_ids_str)
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.adgroup_catmatch_list)



if __name__ == '__main__':

    nick = 'chinchinstyle'
    adgroup_ids = [346064835, 346519023] 
    adgroup_catmatch_list = SimbaAdgroupAdgroupcatmatchsGet.get_adgroup_catmatchs(
            nick, adgroup_ids)
    for adgroup_catmatch in adgroup_catmatch_list:
        print adgroup_catmatch
