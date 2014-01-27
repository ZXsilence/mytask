#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import SimbaAdgroupCatmatchUpdateRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaAdgroupCatmatchUpdate(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(3)
    def update_adgroup_catmatch(cls, nick, adgroup_id, catmatch_id, max_price, use_default_price, online_status ):

        req = SimbaAdgroupCatmatchUpdateRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id 
        req.catmatch_id = catmatch_id 
        req.max_price = max_price 
        req.use_default_price = use_default_price
        req.online_status = online_status 
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.adgroupcatmatch)



if __name__ == '__main__':

    nick = 'chinchinstyle'
    adgroup_id = 346064835
    catmatch_id = 52521930069
    max_price = 17
    use_default_price = 'false' 
    online_status = 'online'

    adgroup_catmatch = SimbaAdgroupCatmatchUpdate.update_adgroup_catmatch(
             nick, adgroup_id, catmatch_id, max_price, use_default_price, online_status )
    
    print adgroup_catmatch
