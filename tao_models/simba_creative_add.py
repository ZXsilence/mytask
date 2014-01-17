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

from TaobaoSdk import SimbaCreativeAddRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaCreativeAdd(object):


    @classmethod
    @tao_api_exception(5)
    def add_creative(cls, nick, adgroup_id,title,img_url):
        req = SimbaCreativeAddRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        req.title = title
        req.img_url = img_url
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.creative)

if __name__ == '__main__':
    nick = 'chinchinstyle'
    adgroup_id =164302433 
    title = '测试推广内容test'
    img_url = 'http://img.taobaocdn.com/bao/uploaded/i1/520500325/T2ZBhTXXNbXXXXXXXX_!!520500325.jpg'
    print (SimbaCreativeAdd.add_creative(nick,adgroup_id,title,img_url))

