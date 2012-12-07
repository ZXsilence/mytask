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

class SimbaKeywordsDelete(object):

    @classmethod
    @tao_api_exception()
    def delete_keywords(cls, access_token, nick, campaign_id, keyword_id_list):
        if not keyword_id_list:
            return []
        keyword_id_list = [str(keyword_id) for keyword_id in keyword_id_list]
        req = SimbaKeywordsDeleteRequest()
        req.campaign_id = campaign_id
        req.nick = nick
        req.keyword_ids = ','.join(keyword_id_list)

        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            if rsp.code == 15 and rsp.sub_msg == u'没有属于该客户下指定推广计划的有效关键词可删除':
                return []
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)
        return rsp.keywords

