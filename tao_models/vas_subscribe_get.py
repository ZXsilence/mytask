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

from TaobaoSdk import VasSubscribeGetRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply
from tao_models.conf.settings import APP_SETTINGS,SERVER_URL,API_NEED_SUBWAY_TOKEN

logger = logging.getLogger(__name__)

class VasSubscribeGet(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(30)
    def get_vas_subscribe(cls, nick, soft_code):
        """
        given a campaign_id, get the adgroup list in this campaign
        """
        req = VasSubscribeGetRequest()
        req.nick = nick
        req.article_code = APP_SETTINGS[soft_code]['article_code']
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.article_user_subscribes)

if __name__ == '__main__':
    nick = 'chinchinstyle'
    soft_code = 'BD'
    article_user_subscribes = VasSubscribeGet.get_vas_subscribe(nick, soft_code)
    for article_user_subscribe in article_user_subscribes:
        print article_user_subscribe
