#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import ItemsOnsaleGetRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class ItemsOnsaleGet(object):

    DEFAULT_FIELDS = 'title,price,pic_url,num_iid'

    @classmethod
    @tao_api_exception()
    def _get_page_items(cls,req,nick):
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp


    @classmethod
    @tao_api_exception()
    def get_item_list(cls, nick, max_pages=50, fields=DEFAULT_FIELDS):

        total_item_list = []

        req = ItemsOnsaleGetRequest()
        req.fields = fields
        req.order_by = "modified:desc" 
        req.page_size = 200
        req.page_no = 1 

        while True:
            rsp = cls._get_page_items(req,nick)
            if rsp.items is None:
                logger.info("get item info, but none return")
                break 
            logger.info("get item info, actually return: %s"%(len(rsp.items)))
            total_item_list.extend(rsp.items)

            if len(rsp.items) != req.page_size:
                break
            if req.page_no == max_pages:
                break
            req.page_no += 1

        return change_obj_to_dict_deeply(total_item_list)

    @classmethod
    @tao_api_exception()
    def get_item_list_with_overview(cls, nick, max_pages=1, fields=DEFAULT_FIELDS):

        total_item_list = []

        req = ItemsOnsaleGetRequest()
        req.fields = fields
        req.order_by = "modified:desc" 
        req.page_size = 2
        req.page_no = 1 

        while True:
            soft_code = None
            rsp = ApiService.execute(req,nick,soft_code)
            if rsp.items is None:
                logger.info("get item info, but none return")
                return {'total_results':0, 'item_list':total_item_list} 

            logger.info("get item info, actually return: %s"%(len(rsp.items)))
            total_item_list.extend(rsp.items)

            if len(rsp.items) != req.page_size:
                break
            if req.page_no == max_pages:
                break

            req.page_no += 1

        return {'total_results':change_obj_to_dict_deeply(rsp.total_results), 'item_list':change_obj_to_dict_deeply(total_item_list)} 

def test():
    nick = 'chinchinstyle'
    total_item_list = ItemsOnsaleGet.get_item_list(nick)

    print len(total_item_list)
    for item in total_item_list:
        print item

def test_overview():
    nick = 'chinchinstyle'
    items_overview = ItemsOnsaleGet.get_item_list_with_overview(nick)
    print items_overview['total_results']
    for item in items_overview['item_list']:
        print item

if __name__ == '__main__':
    test()
    #test_overview()
