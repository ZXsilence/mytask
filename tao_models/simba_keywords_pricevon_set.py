#! /usr/bin/env python
#! coding: utf-8
# author = 'jyd'


import sys
import os
import  copy
import json
import logging
import logging.config

if __name__ == '__main__':
    #logging.config.fileConfig('conf/consolelogger.conf')
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    #set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')
    set_taobao_client('21065688', '74aecdce10af604343e942a324641891')

from TaobaoSdk import SimbaKeywordsPricevonSetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception
from tao_models.common.page_size import  PageSize

logger = logging.getLogger(__name__)

class SimbaKeywordsPricevonSet(object):

    @classmethod
    @tao_api_exception()
    def set_keywords_price(cls, access_token, nick, keyword_price_list):
        if not keyword_price_list:
            return []
        size = PageSize.KEYWORDS_SET
        word_price_dict_list = []
        for element in keyword_price_list:
            word_price_dict = {
                    "keywordId":element['kid']
                    , "maxPrice":element['price']
                    , "isDefaultPrice":0
                    , "matchScope":element.get('match_scope',4)
                    }
            word_price_dict_list.append(word_price_dict)

        req = SimbaKeywordsPricevonSetRequest()
        req.nick = nick

        package_num = len(keyword_price_list)/size+ 1
        if len(keyword_price_list) % size== 0:
            package_num -= 1

        keywords = []
        for i in range(package_num):
            keyword_price_str = json.dumps(word_price_dict_list[i*size: (i+1)*size])
            req.keywordid_prices = keyword_price_str

            rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

            keywords.extend(rsp.keywords)

        return keywords


    @classmethod
    @tao_api_exception(50)
    def _set_price(cls, access_token, nick, keywordid_prices):
        """
        args:
            wordid_price_list: [('keywordid', price),(102232, 33)]
        """
        word_price_dict_list = []
        for kid, price in keywordid_prices:
            word_price_dict = {
                    "keywordId":kid
                    , "maxPrice":price
                    , "isDefaultPrice":0
                    , "matchScope":4
                    }
            word_price_dict_list.append(word_price_dict)

        req = SimbaKeywordsPricevonSetRequest()
        req.nick = nick
        req.keywordid_prices = json.dumps(word_price_dict_list) 
        try:
            rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        except Exception, data:
            raise ApiExecuteException

        if not rsp.isSuccess():
            logger.error("set_price error nick [%s] msg [%s] sub_msg [%s]" %(nick
                ,rsp.msg, rsp.sub_msg))
            if rsp.sub_msg and '关键词不能为空' in rsp.sub_msg:
                return []
            raise ErrorResponseException(code=rsp.code,msg=rsp.msg, sub_msg=rsp.sub_msg, sub_code=rsp.sub_code)
        return rsp.keywords

    @classmethod
    def set_price(cls, access_token, nick, wordid_price_list):
        size = PageSize.KEYWORDS_SET
        package_num = len(wordid_price_list)/size+ 1
        if len(wordid_price_list) % size== 0:
            package_num -= 1

        keywords = []
        for i in range(package_num):
            keywordid_prices = wordid_price_list[i*size:(i+1)*size]
            subkeywords = SimbaKeywordsPricevonSet._set_price(access_token, nick, keywordid_prices)
            keywords.append(subkeywords)
        return keywords

def test():
    #access_token = '6201c01b4ZZdb18b1773873390fe3ff66d1a285add9c10c520500325'
    access_token = '620181005f776f4b1bdfd5952ec7cfa172e008384c567a2520500325'
    nick = 'chinchinstyle'
    word_price_list = [(24497482990, 250), (24497482994, 168)]
    SimbaKeywordsPricevonSet.set_price(access_token, nick, word_price_list)

def test2():
    access_token = '620181005f776f4b1bdfd5952ec7cfa172e008384c567a2520500325'
    nick = 'chinchinstyle'
    word_price_list = [{'kid':24497482990, 'price':254, 'match_scope':1}
            ,{'kid':24497482994, 'price':450, 'match_scope':4}]
    SimbaKeywordsPricevonSet.set_keywords_price(access_token, nick, word_price_list)

if __name__ == '__main__':
    #test()
    test2()
