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
    from tao_models.conf import set_env
    set_env.getEnvReady()
    logging.config.fileConfig('conf/consolelogger.conf')

from TaobaoSdk import SimbaKeywordsDeleteRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception




logger = logging.getLogger(__name__)

class SimbaKeywordsQscoreGet(object):

    @classmethod
    @tao_api_exception
    def get_keywords_qscore(cls, access_token, nick, adgroup_id):
        req = SimbaKeywordsQscoreGetRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id

        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.keyword_qscore_list
