#! /usr/bin/env python
#! coding: utf-8
# author = 'jyd'


import sys
import os
import  copy
import json
import logging
import logging.config
import copy

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import SimbaKeywordsPricevonSetRequest
from tao_models.common.page_size import  PageSize
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply
from TaobaoSdk.Exceptions import ErrorResponseException

logger = logging.getLogger(__name__)

class SimbaKeywordsPricevonSet(object):

    @classmethod
    @tao_api_exception()
    def set_keywords_price(cls, nick, keyword_price_list):
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
            soft_code = None
            try:
                rsp = ApiService.execute(req,nick,soft_code)
            except ErrorResponseException,e:
                rsp = e.rsp
                if not rsp.isSuccess():
                    if rsp.sub_msg and ('关键词不能为空' in rsp.sub_msg or '包含了不属于该客户的关键词Id' in rsp.sub_msg):
                        logger.warning('[%s] keywords_add failed,keywordid_prices:%s  :%s,%s'%(nick,keyword_price_str,rsp.msg,rsp.sub_msg))
                        continue
                    raise e

            keywords.extend(rsp.keywords)
        return change_obj_to_dict_deeply(keywords)


    @classmethod
    @tao_api_exception(50)
    def _set_price(cls, nick, keywordid_prices):
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
        soft_code = None
        try:
            rsp = ApiService.execute(req,nick,soft_code)
        except ErrorResponseException,e:
            rsp = e.rsp
            if not rsp.isSuccess():
                logger.debug("set_price error nick [%s] msg [%s] sub_msg [%s]" %(nick
                    ,rsp.msg, rsp.sub_msg))
                if rsp.sub_msg and ('关键词不能为空' in rsp.sub_msg or '包含了不属于该客户的关键词Id' in rsp.sub_msg):
                    logger.warning('[%s] keywords_add failed,keywordid_prices:%s  :%s,%s'%(nick,word_price_dict_list,rsp.msg,rsp.sub_msg))
                    return []
                raise e

        return rsp.keywords
   
    @classmethod
    def _del_duplicates(cls,wordid_price_list):
        #去重
        kids_list = []
        return_list = []
        for item in wordid_price_list:
            keyword_id = item[0]
            if keyword_id in kids_list:
                continue
            else:
                kids_list.append(keyword_id)
                return_list.append(item)
        return return_list 


    @classmethod
    def set_price(cls, nick, wordid_price_list):
        wordid_price_list = SimbaKeywordsPricevonSet._del_duplicates(wordid_price_list)

        size = PageSize.KEYWORDS_SET
        package_num = len(wordid_price_list)/size+ 1
        if len(wordid_price_list) % size== 0:
            package_num -= 1

        keywords = []
        for i in range(package_num):
            keywordid_prices = wordid_price_list[i*size:(i+1)*size]
            subkeywords = SimbaKeywordsPricevonSet._set_price(nick, keywordid_prices)
            keywords.extend(subkeywords)
        return change_obj_to_dict_deeply(keywords)

def test():
    nick = 'chinchinstyle'
    word_price_list = [(50729824904, 250), (50729824900, 168)]
    print SimbaKeywordsPricevonSet.set_price(nick, word_price_list)

def test2():
    nick = 'chinchinstyle'
    word_price_list = [{'kid':50729824900, 'price':333, 'match_scope':4}]
    print SimbaKeywordsPricevonSet.set_keywords_price(nick, word_price_list)

if __name__ == '__main__':
    #test()
    test2()
