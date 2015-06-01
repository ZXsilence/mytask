#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

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
    set_api_source('normal_test')

from TaobaoSdk import VasOrderSearchRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from api_server.conf.settings import APP_SETTINGS,SERVER_URL,API_NEED_SUBWAY_TOKEN

logger = logging.getLogger(__name__)

class VasOrderSearch(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(10)
    def _search_vas_order(cls, start_created, end_created, page_no,soft_code, nick=None):

        req = VasOrderSearchRequest()
        req.article_code = APP_SETTINGS[soft_code]['article_code']
        #req.item_code = item_code 
        req.start_created = start_created 
        req.end_created = end_created 
        req.page_size = VasOrderSearch.PAGE_SIZE 
        req.page_no = page_no 
        if nick != None:
            req.nick = nick
        nick = None
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.article_biz_orders


    @classmethod
    def search_vas_order(cls, start_created, end_created,soft_code, nick=None):
        """ 从最后一页开始获取订购记录,防止翻页时丢单"""
        order_count=cls.get_var_orders_count(start_created, end_created,soft_code,nick)
        page_count=(order_count-1)/VasOrderSearch.PAGE_SIZE+1
        article_biz_orders_all = []
        while page_count>0:
            article_biz_orders = VasOrderSearch._search_vas_order(start_created, end_created, page_count,soft_code, nick)
            if not article_biz_orders:
                break 
            article_biz_orders_all.extend(article_biz_orders)
            page_count -= 1
        return change_obj_to_dict_deeply(article_biz_orders_all)

    @classmethod
    def search_vas_order_yesterday(cls, soft_code):
        yes = datetime.datetime.now() - datetime.timedelta(days=1)
        today = datetime.datetime.now()
        start_created = yes.strftime("%Y-%m-%d 00:00:00") 
        end_created = today.strftime("%Y-%m-%d 00:00:00") 
        return VasOrderSearch.search_vas_order( start_created, end_created,soft_code)

    @classmethod
    def search_vas_order_all(cls, soft_code,days=30):
        start = datetime.datetime.now() - datetime.timedelta(days)
        today = datetime.datetime.now()
        start_created = start.strftime("%Y-%m-%d 00:00:00") 
        end_created = today.strftime("%Y-%m-%d 00:00:00") 
        return VasOrderSearch.search_vas_order(start_created, end_created,soft_code)

    @classmethod
    def search_vas_order_by_nick(cls, sdate, edate, soft_code,nick):
        start_created = sdate.strftime("%Y-%m-%d 00:00:00") 
        end_created = edate.strftime("%Y-%m-%d 00:00:00") 
        return VasOrderSearch.search_vas_order(start_created, end_created,soft_code, nick)

    @classmethod
    def search_vas_order_by_nick_new(cls, sdate, edate, soft_code,nick):
        start_created = sdate.strftime("%Y-%m-%d %H:%M:%S") 
        end_created = edate.strftime("%Y-%m-%d %H:%M:%S") 
        return VasOrderSearch.search_vas_order(start_created, end_created,soft_code, nick)

    @classmethod
    @tao_api_exception(10)
    def get_var_orders_count(cls,start_created, end_created,soft_code,nick=None):
        """
        article_code 应用id 
        start_created ,end_created 为字符格式时间 eg: start_created="2013-07-14 00:00:00"
        """
        req = VasOrderSearchRequest()
        req.article_code = APP_SETTINGS[soft_code]['article_code']
        req.start_created = start_created
        req.end_created = end_created
        req.page_size =1
        if nick is not None:
            req.nick=nick
        soft_code = None
        nick = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.total_item)


if __name__ == '__main__':
    nick = '易瑞达家居专营店'
    soft_code = 'SYB'
    start = datetime.datetime.now() - datetime.timedelta(89)
    today = datetime.datetime.now()
    result = VasOrderSearch.search_vas_order_by_nick(start, today, soft_code,nick)
    for element in result:
        print element
