#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import  copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaKeywordsbyadgroupidGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from TaobaoSdk.Exceptions import ErrorResponseException 

logger = logging.getLogger(__name__)

class SimbaKeywordsbyadgroupidGet(object):
    
    @classmethod
    @tao_api_exception()
    def get_keyword_list_by_adgroup(cls, nick, adgroup_id):
        """
        get keyword list for some specific adgroup id
        """
        req = SimbaKeywordsbyadgroupidGetRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        soft_code = None
        #rsp = ApiService.execute(req,nick,soft_code)
        try:
            rsp = ApiService.execute(req,nick,soft_code)
        except ErrorResponseException,e:
            if e.sub_code == '205_E_PARAMETER_LIST_OUT_OF_BOUND' and e.sub_msg and 'idList expect' in e.sub_msg:
                return [] 
            raise e
        return change_obj_to_dict_deeply(rsp.keywords)


def test():
    nick = '小新在线1992'
    adgroup_id = 447310159
    #adgroup_id = 429010771
    keywords = SimbaKeywordsbyadgroupidGet.get_keyword_list_by_adgroup(nick, adgroup_id)
    for keyword in keywords:
        print keyword


if __name__ == '__main__':
    test()
