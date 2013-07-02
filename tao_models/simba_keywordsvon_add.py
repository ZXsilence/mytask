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
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    #set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')
    set_taobao_client('21065688', '74aecdce10af604343e942a324641891')


from TaobaoSdk import SimbaKeywordsvonAddRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception
from tao_models.common.exceptions import KeywordsFullException


logger = logging.getLogger(__name__)

class SimbaKeywordsvonAdd(object):
    """
    TODO
    [ { "word": "西瓜汁", "maxPrice": 123 ,"isDefaultPrice": 0,"matchScope": 1}, { "word": "苹果汁","maxPrice": 0, "isDefaultPrice": 1 ,"matchScope": 2} ]
    """

    @classmethod
    @tao_api_exception()
    def add_keywords(cls, access_token, nick, adgroup_id, word_price_list,batch_match_scope=4,  custom_match_scope=False):
        """
        args:
            word_price_list: [('key', price),('aa', 33)] or word_price_list: [('key', price,match_scope),('aa', 33,2)]
            if custom_match_scope is True look up batch_match_scope from  word_price_list first
        """
        logger.error("add keywords size [%d]", len(word_price_list)) 

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
        package_num = len(word_price_dict_list)/100 + 1
        if len(word_price_dict_list) % 100 == 0:
            package_num -= 1

        for i in range(package_num):
            keyword_prices_str = json.dumps(word_price_dict_list[i*100:(i+1)*100])
            req.keyword_prices = keyword_prices_str 
            rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                if rsp.code == 15 and rsp.sub_msg != None and u'已有关键词已经达到200' in rsp.sub_msg:
                    return []
                if rsp.code == 15 and rsp.sub_msg == u'没有有效关键词可增加， 输入的关键词和已有出现重复':
                    return []
                if rsp.code == 15 and rsp.sub_msg == u'指定的推广组不存在':
                    return []
                logger.error("add keywords failed, msg [%s] sub_msg [%s]", rsp.msg, rsp.sub_msg) 
                raise ErrorResponseException(code=rsp.code,msg=rsp.msg, sub_msg=rsp.sub_msg, sub_code=rsp.sub_code)
            keywords.extend(rsp.keywords) 
        return keywords


def test():
    #access_token = '6201c01b4ZZdb18b1773873390fe3ff66d1a285add9c10c520500325'
    access_token = '620181005f776f4b1bdfd5952ec7cfa172e008384c567a2520500325'
    nick = 'chinchinstyle'
    adgroup_id = '169703057'
    word_price_list = [('chinzzz', 250), ('styleeee', 168)]
    SimbaKeywordsvonAdd.add_keywords(access_token, nick, adgroup_id, word_price_list)

if __name__ == '__main__':
    test()
