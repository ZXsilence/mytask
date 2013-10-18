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
from tao_models.common.page_size import  PageSize 


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

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            if rsp.code == 15 and rsp.sub_msg == u'没有属于该客户下指定推广计划的有效关键词可删除':
                return []
            if rsp.sub_msg and  '包含了不属于该客户的关键词Id' in rsp.sub_msg:
                logger.warning('[%s] keywords_delete failed,word_list:%s  :%s,%s'%(nick,word_list,rsp.msg,rsp.sub_msg))
                return []
            logger.debug("delete_keywords error nick [%s] msg [%s] sub_msg [%s]" %(nick
                , rsp.msg, rsp.sub_msg))
            raise ErrorResponseException(code=rsp.code,msg=rsp.msg, sub_msg=rsp.sub_msg, sub_code=rsp.sub_code)
        return rsp.keywords

    @classmethod
    def delete_keywords(cls, access_token, nick, campaign_id, keyword_id_list):
        keywords = []
        size = PageSize.KEYWORDS_DEL
        package_num = len(keyword_id_list)/size + 1
        if len(keyword_id_list) % size == 0:
            package_num -= 1
        for i in range(package_num):
            subkeywords = SimbaKeywordsDelete._delete_keywords(access_token, nick, \
                    campaign_id, keyword_id_list[i*size: (i+1)*size])
            keywords.extend(subkeywords)

        return keywords


