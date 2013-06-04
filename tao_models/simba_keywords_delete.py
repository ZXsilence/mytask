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

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)

class SimbaKeywordsDelete(object):
    """
    TODO
    """

    @classmethod
    @tao_api_exception()
    def _delete_keywords(cls, access_token, nick, campaign_id, keyword_id_list):
        """
        args:
            keyword_id_list: [200000001,200000002]
        """

        word_list = [str(word) for word in keyword_id_list]

        req = SimbaKeywordsDeleteRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.keyword_ids = ",".join(word_list)

        try:
            rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        except Exception, data:
            raise ApiExecuteException

        if not rsp.isSuccess():
            if rsp.code == 15 and rsp.sub_msg == u'没有属于该客户下指定推广计划的有效关键词可删除':
                return []
            logger.error("delete_keywords error nick [%s] msg [%s] sub_msg [%s]" %(nick
                , rsp.msg, rsp.sub_msg))
            raise ErrorResponseException(code=rsp.code,msg=rsp.msg, sub_msg=rsp.sub_msg, sub_code=rsp.sub_code)
        return rsp.keywords

    @classmethod
    def delete_keywords(cls, access_token, nick, campaign_id, keyword_id_list):
        keywords = []
        package_num = len(keyword_id_list)/100 + 1
        if len(keyword_id_list) % 100 == 0:
            package_num -= 1
        for i in range(package_num):
            subkeywords = SimbaKeywordsDelete._delete_keywords(access_token, nick, \
                    campaign_id, keyword_id_list[i*100: (i+1)*100])
            keywords.extend(subkeywords)

        return keywords


