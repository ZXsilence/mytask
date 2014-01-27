#!/usr/bin/env python
#encoding=utf-8

import sys
import os
import logging
import logging.config
import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import VasSubscSearchRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class VasSubscSearch(object):

    PAGE_SIZE = 200
    
    @classmethod
    @tao_api_exception(3)
    def _search_vas_subsc(cls, article_code, start_deadline, end_deadline, page_no):
        req = VasSubscSearchRequest()
        req.article_code = article_code
        req.end_deadline = end_deadline
        req.start_deadline = start_deadline
        req.page_size = cls.PAGE_SIZE
        req.page_no = page_no

        
        rsp = tao_model_settings.taobao_client.execute(req, '')[0]
        
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)
        
        return rsp.article_subs
        
    @classmethod
    def search_vas_subsc(cls, article_code, start_deadline, end_deadline):
        count = 1
        article_subs = []
        
        while count < 300:
            article_sub_list = cls._search_vas_subsc( article_code, start_deadline, end_deadline, count)
            article_subs.extend(article_sub_list)
            count += 1
            
            if len(article_sub_list) < cls.PAGE_SIZE:
                break
               
               
        return article_subs
        
    @classmethod
    def search_vas_subsc_by_nick(cls, nick, article_code, start_deadline, end_deadline):
        req = VasSubscSearchRequest()
        req.article_code = article_code
        req.start_deadline = start_deadline
        req.end_deadline = end_deadline
        req.nick = nick

        rsp = tao_model_settings.taobao_client.execute(req, '')[0]

        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.article_subs
        
        
        
if __name__ == '__main__':
    article_code = 'ts-1797607'
    start_deadline = datetime.date.today() - datetime.timedelta(days=0)
    end_deadline = datetime.date.today() - datetime.timedelta(days=10)
    nick = 'chinchinstyle'
    
    #result = VasSubscSearch.search_vas_subsc_by_nick(nick, article_code,start_deadline)
    
    result = VasSubscSearch.search_vas_subsc_by_nick(nick, article_code, start_deadline, None)
    for article_sub in result:
        print article_sub.toDict()
        
    print len(result)
        
        
        
