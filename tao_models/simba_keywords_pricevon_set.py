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
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaKeywordsPricevonSetRequest
from tao_models.common.page_size import  PageSize
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from TaobaoSdk.Exceptions import ErrorResponseException

logger = logging.getLogger(__name__)

class SimbaKeywordsPricevonSet(object):

    @classmethod
    def set_keywords_price(cls, nick, keyword_price_list,safe=True):
        if not keyword_price_list:
            return []
        keyword_price_list = SimbaKeywordsPricevonSet._del_duplicates2(keyword_price_list)
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
        soft_code = None
        for i in range(package_num):
            sub_keywords = cls._set_price2(nick, word_price_dict_list[i*size: (i+1)*size], soft_code, safe)
            keywords.extend(sub_keywords)

        return change_obj_to_dict_deeply(keywords)

    @classmethod
    @tao_api_exception(20)
    def _set_price2(cls, nick, word_price_list, soft_code, safe=True):
        keywords = []
        try:
            req = SimbaKeywordsPricevonSetRequest()
            req.nick = nick
            keyword_price_str = json.dumps(word_price_list)
            req.keywordid_prices = keyword_price_str
            rsp = ApiService.execute(req,nick,soft_code)
            if not rsp.isSuccess():
                if rsp.sub_msg and ('关键词不能为空' in rsp.sub_msg or '包含了不属于该客户的关键词Id' in rsp.sub_msg):
                    return keywords
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        except Exception,e:
            if safe is True:
                raise
        else:
            keywords = rsp.keywords

        return keywords
        

    @classmethod
    @tao_api_exception(20)
    def _set_price(cls, nick, keywordid_prices):
        """
        args:
            wordid_price_list: [('keywordid', price),(102232, 33)]
        """
        word_price_dict_list = []
        for k in keywordid_prices:
            kid = k[0]
            price = k[1]
            match_scope = k[2] if len(k) >=3 else 4
            word_price_dict = {
                    "keywordId":kid
                    , "maxPrice":price
                    , "isDefaultPrice":0
                    , "matchScope": match_scope
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
    def _del_duplicates2(cls,wordid_price_list):
        #去重
        kids_list = []
        return_list = []
        for item in wordid_price_list:
            keyword_id = item['kid']
            if keyword_id in kids_list:
                continue
            else:
                kids_list.append(keyword_id)
                return_list.append(item)
        return return_list 

   
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
    def set_price(cls, nick, wordid_price_list,safe=True):
        wordid_price_list = SimbaKeywordsPricevonSet._del_duplicates(wordid_price_list)

        size = PageSize.KEYWORDS_SET
        package_num = len(wordid_price_list)/size+ 1
        if len(wordid_price_list) % size== 0:
            package_num -= 1

        keywords = []
        for i in range(package_num):
            
            keywordid_prices = wordid_price_list[i*size:(i+1)*size]
            try:
                subkeywords = SimbaKeywordsPricevonSet._set_price(nick, keywordid_prices)
            except Exception:
                if safe:
                    raise
                else:
                    continue
            keywords.extend(subkeywords)
        return change_obj_to_dict_deeply(keywords)

def test():
    nick = 'chinchinstyle'
    word_price_list = [(50729824904, 250), (50729824900, 168,1)]
    print SimbaKeywordsPricevonSet.set_price(nick, word_price_list)

def test2():
    nick = 'chinchinstyle'
    word_price_list = [{'kid':70160490652, 'price':101, 'match_scope':1}, \
            {'kid':70160490655, 'price':101, 'match_scope':1}, \
            {'kid':70160490656, 'price':101, 'match_scope':1}, \
            {'kid':70160490657, 'price':101, 'match_scope':1}, \
            {'kid':60160490658, 'price':101, 'match_scope':1}
            ]
    print SimbaKeywordsPricevonSet.set_keywords_price(nick, word_price_list)

if __name__ == '__main__':
    #test()
    test2()
