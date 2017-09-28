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

    PAGE_SIZE = 200

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
    def get_page_num_and_first_page(cls, nick, start_time):
        """获取分页数及第一页的关键词
        
        目前api每页最大项数为200
        分页数由返回的总项数除以200得到

        Args:
            nick: ...
            start_time: 得到此时间点之后到系统当前时间的词变化数据，不能大于一个月

        Returns:
            page_num: 分页数
            keywords: 第一页关键词id列表

        """
        req = SimbaKeywordsChangedGetRequest()
        req.nick = nick
        req.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        req.page_no = 1
        rsp = SimbaKeywordsChangedGet._get_sub_keywords_changed(nick,req)
        if not rsp.keywords.total_item:
            return 0, []
        page_num = (rsp.keywords.total_item + 200 - 1) / 200
        keywords = [item.keyword_id for item in rsp.keywords.keyword_list]
        return page_num, keywords

    @classmethod
    def get_keywords_id_changed_remain(cls, nick, start_time, page_num):
        """获取第二页以后的关键词
        
        配合get_page_num_and_first_page方法使用
        与原方法相比,减小了第一次调用

        Args:
            nick: ...
            start_time: 得到此时间点之后到系统当前时间的词变化数据，不能大于一个月
            page_num: 分页数

        Returns:
            keywords: 关键词id列表

        """
        req = SimbaKeywordsChangedGetRequest()
        req.nick = nick
        req.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        keywords = []
        for curr_page_no in range(2, page_num + 1):
            req.page_no = curr_page_no
            rsp = SimbaKeywordsChangedGet._get_sub_keywords_changed(nick,req)
            keywords.extend([item.keyword_id for item in rsp.keywords.keyword_list])
        return keywords
    
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
    #SimbaKeywordsChangedGet.PAGE_SIZE = 300
    #print SimbaKeywordsChangedGet.get_total_page(nick,start_time)
    #print SimbaKeywordsChangedGet.get_keywords_id_changed(nick,start_time)
    start_time = datetime(2017, 9, 12, 10, 14, 44)
    nick = "世家家居旗舰店"
    res = SimbaKeywordsChangedGet.get_page_num_and_first_page(nick, start_time)
    import pdb; pdb.set_trace()  # XXX BREAKPOINT

if __name__ == '__main__':
    test()
