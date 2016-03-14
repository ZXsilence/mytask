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

from TaobaoSdk import SimbaAdgroupOnlineitemsvonGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class SimbaAdgroupOnlineitemsvonGet(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception()
    def get_items_online(cls, nick, max_page = 50):
        """
        get items online

        format:
        "nick": "zcztest001",
                    "num_id": 12345,
                    "price": "4545",
                    "title": "女装",
                    "quantity": 100,
                    "sales_count": 100,
                    "publish_time": "2000-01-01 00:00:00"

        """
        item_online_list = []

        req = SimbaAdgroupOnlineitemsvonGetRequest()
        req.nick = nick
        req.page_size = cls.PAGE_SIZE
        req.order_field = 'bidCount'
        req.order_by = 'true'
        req.page_no = 1
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        if not rsp.page_item.total_item:
            logger.info("surprise.. , no items online  nick:%s"%nick)
            return item_online_list
        item_online_list.extend(rsp.page_item.item_list)
        # continue to call if more than one page
        total_pages = (rsp.page_item.total_item - 1)/cls.PAGE_SIZE + 1
        if total_pages > max_page:
            total_pages = max_page
        for page_no in range(2,total_pages+1):
            req.page_no = page_no
            soft_code = None
            rsp = ApiService.execute(req,nick,soft_code)
            item_online_list.extend(rsp.page_item.item_list)
            if len(item_online_list)>=10000:
                break

        logger.debug("actually get %i items online in for nick:%s"%(len(item_online_list), nick))

        return change_obj_to_dict_deeply(item_online_list)

    @classmethod
    @tao_api_exception()
    def get_items_online_with_overview(cls, nick, max_page = 3):
        item_online_list = []
        req = SimbaAdgroupOnlineitemsvonGetRequest()
        req.nick = nick
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)

        if not rsp.page_item.total_item:
            logger.info("surprise.. , no items online  nick:%s"%nick)
            return None 

        item_online_list.extend(rsp.page_item.item_list)
        total_pages = (rsp.page_item.total_item  - 1)/cls.PAGE_SIZE + 1
        if total_pages > max_page:
            total_pages = max_page
        for page_no in range(2,total_pages+1):
            req.page_no = page_no
            soft_code = None
            rsp = ApiService.execute(req,nick,soft_code)
            item_online_list.extend(rsp.page_item.item_list)
            if len(item_online_list)>=10000:
                break
        logger.debug("actually get %i items online in for nick:%s"%(len(item_online_list), nick))

        return {"item_list":change_obj_to_dict_deeply(item_online_list), "total_item":change_obj_to_dict_deeply(rsp.page_item.total_item)}

    @classmethod
    @tao_api_exception(10)
    def get_item_count(cls, nick):
        req = SimbaAdgroupOnlineitemsvonGetRequest()
        req.nick = nick
        req.page_size = cls.PAGE_SIZE
        req.order_field = 'bidCount'
        req.order_by = 'true'
        req.page_no = 1 
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.page_item.total_item)


def test():
    nick = 'chinchinstyle'
    #items = SimbaAdgroupOnlineitemsvonGet.get_items_online(nick)
    #items = SimbaAdgroupOnlineitemsvonGet.get_item_count(nick)
    items = SimbaAdgroupOnlineitemsvonGet.get_items_online_with_overview(nick)
    print items


if __name__ == '__main__':
    test()
