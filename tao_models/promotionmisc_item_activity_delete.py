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
    set_api_source('normal_test')

from TaobaoSdk import PromotionmiscItemActivityDeleteRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class PromotionmiscItemActivityDelete(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(5)
    def delete_item_activity(cls, nick,activity_id):

        req = PromotionmiscItemActivityDeleteRequest()
        req.nick = nick
        req.activity_id = activity_id 
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp)




if __name__ == '__main__':
    nick = '麦苗科技001'
    activity_id = 400184451 

    result = PromotionmiscItemActivityDelete.delete_item_activity(nick,activity_id) 
    print result
