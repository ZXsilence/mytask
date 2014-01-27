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
    set_api_source('api_test')

from TaobaoSdk import SimbaKeywordsDeleteRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.common.page_size import PageSize
from TaobaoSdk.Exceptions import ErrorResponseException

logger = logging.getLogger(__name__)

class SimbaKeywordsDelete(object):

    @classmethod
    @tao_api_exception()
    def _delete_keywords(cls, nick, campaign_id, keyword_id_list):
        """
        args:
            keyword_id_list: [200000001,200000002]
        """
        word_list = [str(word) for word in keyword_id_list]
        req = SimbaKeywordsDeleteRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.keyword_ids = ",".join(word_list)
        soft_code = None
        try:
            rsp = ApiService.execute(req,nick,soft_code)
        except ErrorResponseException,e:
            rsp = e.rsp
            if not rsp.isSuccess():
                if rsp.code == 15 and rsp.sub_msg == u'没有属于该客户下指定推广计划的有效关键词可删除':
                    logger.info('[%s] keywords_delete failed,没有属于该客户下指定推广计划的有效关键词可删除,word_list:%s  :%s,%s'%(nick,word_list,rsp.msg,rsp.sub_msg))
                    return []
                if rsp.sub_msg and  '包含了不属于该客户的关键词Id' in rsp.sub_msg:
                    logger.info('[%s] keywords_delete failed,word_list:%s  :%s,%s'%(nick,word_list,rsp.msg,rsp.sub_msg))
                    return []
                logger.debug("delete_keywords error nick [%s] msg [%s] sub_msg [%s]" %(nick
                    , rsp.msg, rsp.sub_msg))
                raise e
        return rsp.keywords

    @classmethod
    def delete_keywords(cls, nick, campaign_id, keyword_id_list):
        keywords = []
        size = PageSize.KEYWORDS_DEL
        package_num = len(keyword_id_list)/size + 1
        if len(keyword_id_list) % size == 0:
            package_num -= 1
        for i in range(package_num):
            subkeywords = SimbaKeywordsDelete._delete_keywords(nick, \
                    campaign_id, keyword_id_list[i*size: (i+1)*size])
            keywords.extend(subkeywords)
        return change_obj_to_dict_deeply(keywords)

if __name__ == '__main__':
    nick = 'chinchinstyle'
    campaign_id = 3367748
    keyword_id_list = [50729824879]
    print SimbaKeywordsDelete.delete_keywords(nick, campaign_id, keyword_id_list)

