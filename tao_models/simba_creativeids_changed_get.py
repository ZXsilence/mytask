#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'


import sys
import os
import logging
import logging.config
from datetime import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import SimbaCreativeidsChangedGetRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaCreativeidsChangedGet(object):
    """
    get adgroups changed since a start_time
    """

    PAGE_SIZE = 1000

    @classmethod
    @tao_api_exception()
    def get_creative_ids_changed(cls, nick, start_time):

        req = SimbaCreativeidsChangedGetRequest()
        req.nick = nick
        req.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.changed_creative_ids)


def test():
    nick = 'chinchinstyle'
    start_time = datetime(2014,1,1) 
    SimbaCreativeidsChangedGet.PAGE_SIZE = 1000
    creative_ids = SimbaCreativeidsChangedGet.get_creative_ids_changed(nick,start_time)
    print 'creative_ids ',creative_ids

if __name__ == '__main__':
    test()
