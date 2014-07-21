#! /usr/bin/env python
#! coding: utf-8
# author = 'jyd'

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

from TaobaoSdk import SimbaKeywordsQscoreGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaKeywordsQscoreGet(object):

    @classmethod
    @tao_api_exception()
    def get_keywords_qscore(cls, nick, adgroup_id):
        req = SimbaKeywordsQscoreGetRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.keyword_qscore_list)

if __name__ == '__main__':
    #nick = 'chinchinstyle'
    #adgroup_id = 336844923
    nick = '麦苗科技001'
    adgroup_id = 409604759 
    print SimbaKeywordsQscoreGet.get_keywords_qscore(nick,adgroup_id)

