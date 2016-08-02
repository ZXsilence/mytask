# -*- coding: utf-8 -*-
'''
Created on 2012-11-3

@author: dk
'''
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

from TaobaoSdk.Request.SimbaSerchcrowdGetRequest import SimbaSerchcrowdGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SerchcrowdGet(object):

    @classmethod
    @tao_api_exception()
    def serchcrowdget_result(cls, nick, adgroup_id, soft_code):
        req = SimbaSerchcrowdGetRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.adgrouptargetingtags)


if __name__ == '__main__':
    nick = "麦苗科技001"
    adgroup_id = 699940229
    soft_code = 'SYB'
    print SerchcrowdGet.serchcrowdget_result(nick, adgroup_id, soft_code)
