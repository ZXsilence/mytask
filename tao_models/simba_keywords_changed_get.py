#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'


import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import  SimbaKeywordsChangedGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaKeywordsChangedGet(object):

    PAGE_SIZE = 1000

    @classmethod
    def get_keywords_changed(cls, nick, start_time):
        """
        注意: start_time 改成datetime 传入
        return format:
        {'keyword_id': 15749079502,
        'modified_time': datetime.datetime(2012, 8, 6, 4, 26, 57),
        'nick': u'\u5bc6\u591a\u5e2e\u5df4'}
        """
        keyword_list = []
        req = SimbaKeywordsChangedGetRequest()
        req.nick = nick
        req.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1
        rsp = SimbaKeywordsChangedGet._get_sub_keywords_changed(nick,req)
        if not rsp.keywords.total_item:
            logger.debug("get_keywords_changed ---nick:%s start_time:%s total_changed_keywords:%s "%(nick,start_time,rsp.keywords.total_item))
            return keyword_list
        keyword_list.extend(rsp.keywords.keyword_list)
        total_pages = (rsp.keywords.total_item + cls.PAGE_SIZE - 1)/cls.PAGE_SIZE
        logger.debug("get_keywords_changed ---nick:%s start_time:%s total_changed_keywords:%s total_pages:%s "%(nick,start_time,rsp.keywords.total_item,total_pages))
        for curr_page_no in range(2, total_pages+1):
            req.page_no = curr_page_no
            rsp = SimbaKeywordsChangedGet._get_sub_keywords_changed(nick,req)
            keyword_list.extend(rsp.keywords.keyword_list)
        return change_obj_to_dict_deeply(keyword_list)
    
    @classmethod
    def get_total_page(cls,nick,start_time):
        req = SimbaKeywordsChangedGetRequest()
        req.nick = nick
        req.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1
        rsp = SimbaKeywordsChangedGet._get_sub_keywords_changed(nick,req)
        if not rsp.keywords.total_item:
            return 0 
        total_pages = (rsp.keywords.total_item +  cls.PAGE_SIZE  -1)/ cls.PAGE_SIZE 
        return total_pages
    
    @classmethod
    def get_keywords_id_changed(cls,nick,start_time):
        keyword_list = []
        req = SimbaKeywordsChangedGetRequest()
        req.nick = nick
        req.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1
        rsp = SimbaKeywordsChangedGet._get_sub_keywords_changed(nick,req)
        if not rsp.keywords.total_item:
            logger.debug("get_keywords_changed ---nick:%s start_time:%s total_changed_keywords:%s "%(nick,start_time,rsp.keywords.total_item))
            return keyword_list
        keyword_list.extend([ item.keyword_id for item in rsp.keywords.keyword_list])
        total_pages = (rsp.keywords.total_item + cls.PAGE_SIZE - 1)/cls.PAGE_SIZE
        logger.debug("get_keywords_changed ---nick:%s start_time:%s total_changed_keywords:%s total_pages:%s "%(nick,start_time,rsp.keywords.total_item,total_pages))
        for curr_page_no in range(2, total_pages+1):
            req.page_no = curr_page_no
            rsp = SimbaKeywordsChangedGet._get_sub_keywords_changed(nick,req)
            keyword_list.extend([ item.keyword_id for item in rsp.keywords.keyword_list])
        return keyword_list


    @classmethod
    @tao_api_exception()
    def _get_sub_keywords_changed(cls, nick, req):
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp

def test():
    nick = 'chinchinstyle'
    from datetime import datetime,timedelta
    start_time = datetime.now() - timedelta(days=10)
    SimbaKeywordsChangedGet.PAGE_SIZE = 300
    print SimbaKeywordsChangedGet.get_total_page(nick,start_time)
    print SimbaKeywordsChangedGet.get_keywords_id_changed(nick,start_time)

if __name__ == '__main__':
    test()
