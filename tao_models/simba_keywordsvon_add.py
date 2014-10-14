#! /usr/bin/env python
#! coding: utf-8 
# author = jyd
# date = 12-8-14

import sys
import os
import json
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaKeywordsvonAddRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.common.page_size import PageSize
from TaobaoSdk.Exceptions import ErrorResponseException

logger = logging.getLogger(__name__)

class SimbaKeywordsvonAdd(object):
    """
    [ { "word": "西瓜汁", "maxPrice": 123 ,"isDefaultPrice": 0,"matchScope": 1}, { "word": "苹果汁","maxPrice": 0, "isDefaultPrice": 1 ,"matchScope": 2} ]
    """

    @classmethod
    @tao_api_exception()
    def add_keywords(cls, nick, adgroup_id, word_price_list,batch_match_scope=4,  custom_match_scope=False):
        """
        args:
            word_price_list: [('key', price),('aa', 33)] or word_price_list: [('key', price,match_scope),('aa', 33,2)]
            if custom_match_scope is True look up batch_match_scope from  word_price_list first
        """
        logger.info("add keywords size [%d]", len(word_price_list)) 

        word_price_dict_list = []
        for add_tuple in word_price_list:
            if custom_match_scope and len(add_tuple)>=3:
                word_price_dict = {"word":add_tuple[0], "maxPrice":add_tuple[1], "isDefaultPrice":0, "matchScope":add_tuple[2]}
            else:
                word_price_dict = {"word":add_tuple[0], "maxPrice":add_tuple[1], "isDefaultPrice":0, "matchScope":batch_match_scope}
            word_price_dict_list.append(word_price_dict)

        req = SimbaKeywordsvonAddRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        
        keywords = []
        size = PageSize.KEYWORDS_ADD
        package_num = len(word_price_dict_list)/size + 1
        if len(word_price_dict_list) % size== 0:
            package_num -= 1
        for i in range(package_num):
            keyword_prices_str = json.dumps(word_price_dict_list[i*size:(i+1)*size])
            req.keyword_prices = keyword_prices_str 
            soft_code = None
            try:
                rsp = ApiService.execute(req,nick,soft_code)
            except ErrorResponseException,e:
                rsp = e.rsp
                if not rsp.isSuccess():
                    logger.info("add keywords failed, total size [%d] package num [%d] msg [%s] sub_msg [%s] code [%s] sub_code [%s]", len(word_price_dict_list), i, str(rsp.msg), str(rsp.sub_msg), str(rsp.code), str(rsp.sub_code)) 
                    if rsp.code == 15 and rsp.sub_msg != None and u'已有关键词已经达到200' in rsp.sub_msg:
                        return change_obj_to_dict_deeply(keywords)
                    if rsp.code == 15 and rsp.sub_msg == u'没有有效关键词可增加， 输入的关键词和已有出现重复':
                        return []
                    if rsp.code == 15 and rsp.sub_msg == u'指定的推广组不存在':
                        return []
                    if rsp.code == 15 and  rsp.sub_msg == u"bidwordList size must in [1,200] , actual is 0":
                        return  change_obj_to_dict_deeply(keywords) 
                    raise e
            keywords.extend(rsp.keywords) 
        return change_obj_to_dict_deeply(keywords)


def test():
    nick = '萌娃潮妞'
    adgroup_id =  446826939 
    word_price_list = [('test', 250), ('test1', 168)]
    print SimbaKeywordsvonAdd.add_keywords(nick, adgroup_id, word_price_list)

if __name__ == '__main__':
    test()
