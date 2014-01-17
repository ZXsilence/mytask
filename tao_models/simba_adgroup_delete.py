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

from TaobaoSdk import SimbaAdgroupDeleteRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaAdgroupDelete(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(4)
    def delete_adgroup(cls, nick, adgroup_id):
        """
        given a campaign_id, get the adgroup list in this campaign
        """

        req = SimbaAdgroupDeleteRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id 
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.adgroup)



if __name__ == '__main__':

    nick = 'chinchinstyle'
    adgroup_id = 346064835
    adgroup = SimbaAdgroupDelete.delete_adgroup(nick, adgroup_id)
    print adgroup
