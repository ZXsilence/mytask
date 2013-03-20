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
    def _search_vas_order(cls, article_code, start_created, end_created, page_no):
        """
        """

        req = VasOrderSearchRequest()
        req.article_code = article_code 
        #req.item_code = item_code 
        req.start_created = start_created 
        req.end_created = end_created 
        req.page_size = VasOrderSearch.PAGE_SIZE 
        req.page_no = page_no 
        rsp = tao_model_settings.taobao_client.execute(req, '')[0]
        if not rsp.isSuccess():
            print rsp.msg
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.article_biz_orders


    @classmethod
    def search_vas_order(cls, article_code, start_created, end_created):
        count = 1
        article_biz_orders_all = []
        while count < 30:
            article_biz_orders = VasOrderSearch._search_vas_order(article_code, start_created, end_created, count)
            article_biz_orders_all.extend(article_biz_orders)
            count += 1
            if len(article_biz_orders) < VasOrderSearch.PAGE_SIZE :
                break

        return article_biz_orders_all

    @classmethod
    def search_vas_order_yesterday(cls, article_code):
        yes = datetime.datetime.now() - datetime.timedelta(days=15)
        today = datetime.datetime.now() - datetime.timedelta(days=14)
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

if __name__ == '__main__':

    article_code = 'ts-1796606'
    result = VasOrderSearch.search_vas_order_yesterday(article_code)
    #result = VasOrderSearch.search_vas_order_all(article_code)
    for element in result:
        print element.toDict()
