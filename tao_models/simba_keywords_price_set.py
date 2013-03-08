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
    from xuanciw.settings import  trigger_envReady
    logging.config.fileConfig('../xuanciw/consolelogger.conf')

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    logging.config.fileConfig('conf/consolelogger.conf')

from TaobaoSdk import SimbaKeywordsPriceSetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception




logger = logging.getLogger(__name__)

class SimbaKeywordsPriceSet(object):

    @classmethod
    @tao_api_exception()
    def set_keywords_price(cls, access_token, nick, keyword_price_list):
        if not keyword_price_list:
            return []

        req = SimbaKeywordsPriceSetRequest()
        req.nick = nick

        package_num = len(keyword_price_list)/100 + 1
        if package_num % 100 == 0:
            package_num -= 1

        keywords = []
        for i in range(package_num):
            keyword_price_str = ""
            for keyword_price in keyword_price_list[i*100: (i+1)*100]:
                keyword_price_str += str(keyword_price['kid']) + '^^' + str(keyword_price['price']) + '^^' +str(keyword_price['match_scope'])
                keyword_price_str += ','
            keyword_price_str = keyword_price_str[:-1]
            req.keywordid_prices = keyword_price_str

            rsp = taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

            keywords.extend(rsp.keywords)

        return keywords


    @classmethod
    @tao_api_exception(20)
    def _set_price(cls, access_token, nick, keywordid_prices):
        """
        args:
            wordid_price_list: [('keywordid', price),(102232, 33)]
        """
        req = SimbaKeywordsPriceSetRequest()
        req.nick = nick
        req.keywordid_prices = keywordid_prices
        try:
            rsp = taobao_client.execute(req, access_token)[0]
        except Exception, data:
            raise ApiExecuteException

        if not rsp.isSuccess():
            logger.error("set_price error nick [%s] msg [%s] sub_msg [%s]" %(nick
                ,rsp.msg, rsp.sub_msg))
            raise ErrorResponseException(code=rsp.code,msg=rsp.msg, sub_msg=rsp.sub_msg, sub_code=rsp.sub_code)
        return rsp.keywords

    @classmethod
    def set_price(cls, access_token, nick, wordid_price_list):
        
        keywords = []
        wordid_price_list = [str(wordid)+"^^"+str(price) for wordid, price in wordid_price_list]
        package_num = len(wordid_price_list)/100 + 1
        if len(wordid_price_list) % 100 == 0:
            package_num -= 1

        for i in range(package_num):
            keywordid_prices = ",".join(wordid_price_list[i*100:(i+1)*100])
            subkeywords = SimbaKeywordsPriceSet._set_price(access_token, nick, keywordid_prices)
            keywords.append(subkeywords)
        return keywords

