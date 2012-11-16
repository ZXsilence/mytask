#! /usr/bin/env python
#! coding: utf-8 
# author = jyd
# date = 12-8-31


import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from xuanciw.settings import  trigger_envReady
    logging.config.fileConfig('../xuanciw/consolelogger.conf')

from TaobaoSdk import VasOrderSearchRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from xuanciw.settings import  taobao_client
from common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)

class VasOrderSearch(object):

    PAGE_SIZE = 20

    @classmethod
    @tao_api_exception
    def get_order_list(cls, article_code, item_code=None, start_created=None, end_created=None):
        order_list = []
        req = VasOrderSearchRequest()
        req.article_code = article_code
        req.item_code = item_code
        req.start_created = start_created
        req.end_created = end_created
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1

        rsp = taobao_client.execute(req)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        if not rsp.total_item:
            logger.info("5555...no order this time")
            return []

        order_list.extend(rsp.article_biz_orders)

        total_pages = (rsp.total_item + cls.PAGE_SIZE - 1)/cls.PAGE_SIZE
        for page_no in range(2,total_pages+1):
            req.page_no = page_no
            rsp = taobao_client.execute(req)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)
            order_list.extend(rsp.article_biz_orders)

        logger.debug("actually get %i order from %s to %s"%(len(order_list), start_created, end_created))

        return order_list


def test_get_order_list():
    article_code = 'ts-1797607'
    item_code = 'ts-1797607-1'
    import datetime
    start_created_str = "2012-08-30 00:00:00"
    order_list = VasOrderSearch.get_order_list(article_code, item_code, start_created=start_created_str)
    for order in order_list:
        print order.toDict()

if __name__ == '__main__':
    test_get_order_list()
