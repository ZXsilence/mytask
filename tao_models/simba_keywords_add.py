#! /usr/bin/env python
#! coding: utf-8 
# author = jyd
# date = 12-8-14

import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from xuanciw.settings import  trigger_envReady
    logging.config.fileConfig('../xuanciw/consolelogger.conf')

from TaobaoSdk import SimbaKeywordsAddRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import  taobao_client
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)

class SimbaKeywordsAdd(object):
    """
    TODO
    """

    @classmethod
    @tao_api_exception()
    def add_keywords(cls, access_token, nick, adgroup_id, word_price_list):
        """
        args:
            word_price_list: [('key', price),('aa', 33)]
        """

        word_price_list = [word+"^^"+str(price) for word, price in word_price_list]

        req = SimbaKeywordsAddRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        
        keywords = []
        package_num = len(word_price_list)/100 + 1
        if len(word_price_list) % 100 == 0:
            package_num -= 1

        for i in range(package_num):
            req.keyword_prices = ",".join(word_price_list[i*100:(i+1)*100])
            rsp = taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                if rsp.code == 15 and rsp.sub_msg == u'没有有效关键词可增加， 输入的关键词和已有出现重复':
                    return []
                logger.error("add keywords failed, msg [%s] sub_msg [%s]", rsp.msg, rsp.sub_msg) 
                raise ErrorResponseException(code=rsp.code,msg=rsp.msg, sub_msg=rsp.sub_msg, sub_code=rsp.sub_code)
            keywords.extend(rsp.keywords) 
        return keywords


