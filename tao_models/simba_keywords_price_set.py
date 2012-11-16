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

from TaobaoSdk import SimbaKeywordsDeleteRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception




logger = logging.getLogger(__name__)

class SimbaKeywordsPriceSet(object):

    @classmethod
    @tao_api_exception
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
                keyword_price_str += str(keyword_price['kid']) + '^^' + str(keyword_price['price'])
                keyword_price_str += ','
            keyword_price_str = keyword_price_str[:-1]
            req.keywordid_prices = keyword_price_str

            rsp = taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

            keywords.extend(rsp.keywords)

        return keywords


