#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config
import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')

from TaobaoSdk import VasOrderSearchRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class VasOrderSearch(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(3)
    def _search_vas_order(cls, article_code, start_created, end_created, page_no, nick=None):
        """
        """

        req = VasOrderSearchRequest()
        req.article_code = article_code 
        #req.item_code = item_code 
        req.start_created = start_created 
        req.end_created = end_created 
        req.page_size = VasOrderSearch.PAGE_SIZE 
        req.page_no = page_no 
        if nick != None:
            req.nick = nick

        rsp = tao_model_settings.taobao_client.execute(req, '')[0]
        if not rsp.isSuccess():
            print rsp.msg
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.article_biz_orders


    @classmethod
    def search_vas_order(cls, article_code, start_created, end_created, nick=None):
        """ 从最后一页开始获取订购记录,防止翻页时丢单"""
        order_count=cls.get_var_orders_count(article_code, start_created, end_created)
        page_count=(order_count-1)/VasOrderSearch.PAGE_SIZE+1
        article_biz_orders_all = []
        while page_count>0:
            article_biz_orders = VasOrderSearch._search_vas_order(article_code, start_created, end_created, page_count, nick)
            if not article_biz_orders:
                break 
            article_biz_orders_all.extend(article_biz_orders)
            page_count -= 1

        return article_biz_orders_all

    @classmethod
    def search_vas_order_yesterday(cls, article_code):
        yes = datetime.datetime.now() - datetime.timedelta(days=1)
        today = datetime.datetime.now()
        start_created = yes.strftime("%Y-%m-%d 00:00:00") 
        end_created = today.strftime("%Y-%m-%d 00:00:00") 
        return VasOrderSearch.search_vas_order(article_code, start_created, end_created)

    @classmethod
    def search_vas_order_all(cls, article_code,days=30):
        start = datetime.datetime.now() - datetime.timedelta(days)
        today = datetime.datetime.now()
        start_created = start.strftime("%Y-%m-%d 00:00:00") 
        end_created = today.strftime("%Y-%m-%d 00:00:00") 
        return VasOrderSearch.search_vas_order(article_code, start_created, end_created)

    @classmethod
    def search_vas_order_by_nick(cls, article_code, sdate, edate, nick):
        start_created = sdate.strftime("%Y-%m-%d 00:00:00") 
        end_created = edate.strftime("%Y-%m-%d 00:00:00") 
        return VasOrderSearch.search_vas_order(article_code, start_created, end_created, nick)

    @classmethod
    def search_vas_order_by_nick_new(cls, article_code, sdate, edate, nick):
        start_created = sdate.strftime("%Y-%m-%d %H:%M:%S") 
        end_created = edate.strftime("%Y-%m-%d %H:%M:%S") 
        return VasOrderSearch.search_vas_order(article_code, start_created, end_created, nick)

    @classmethod
    @tao_api_exception(3)
    def get_var_orders_count(cls,article_code, start_created, end_created,nick=None):
        """
        article_code 应用id 
        start_created ,end_created 为字符格式时间 eg: start_created="2013-07-14 00:00:00"
        """
        req = VasOrderSearchRequest()
        req.article_code = article_code
        req.start_created = start_created
        req.end_created = end_created
        req.page_size =1
        if nick is not None:
            req.nick=nick
        rsp = tao_model_settings.taobao_client.execute(req, '')[0]
        if not rsp.isSuccess():
            print rsp.msg
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        return rsp.total_item



if __name__ == '__main__':

    article_code = 'ts-1796606'
    #result = VasOrderSearch.search_vas_order_yesterday(article_code)
    start = datetime.datetime.now() - datetime.timedelta(300)
    today = datetime.datetime.now()
    result = VasOrderSearch.search_vas_order_by_nick(article_code, start, today, 'chinchinstyle')
    for element in result:
        print element.toDict()
