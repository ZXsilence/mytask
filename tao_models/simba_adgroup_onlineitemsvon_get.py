#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'



import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    #set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')
    set_taobao_client('21065688', '74aecdce10af604343e942a324641891')

from TaobaoSdk import SimbaAdgroupOnlineitemsvonGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)


class SimbaAdgroupOnlineitemsvonGet(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception()
    def get_items_online(cls, access_token, nick, max_page = 50):
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

        #first call
        req.page_no = 1
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        if not rsp.page_item.total_item:
            logger.info("surprise.. , no items online  nick:%s"%nick)
            return item_online_list

        item_online_list.extend(rsp.page_item.item_list)

        # continue to call if more than one page
        total_pages = (rsp.page_item.total_item + cls.PAGE_SIZE - 1)/cls.PAGE_SIZE
        if total_pages > max_page:
            total_pages = max_page
        for page_no in range(2,total_pages+1):
            req.page_no = page_no
            rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
            item_online_list.extend(rsp.page_item.item_list)

        logger.debug("actually get %i items online in for nick:%s"%(len(item_online_list), nick))

        return item_online_list

    @classmethod
    @tao_api_exception()
    def get_items_online_with_overview(cls, access_token, nick, max_page = 3):
        """
        """
        item_online_list = []

        req = SimbaAdgroupOnlineitemsvonGetRequest()
        req.nick = nick
        req.page_size = cls.PAGE_SIZE

        #first call
        req.page_no = 1
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        if not rsp.page_item.total_item:
            logger.info("surprise.. , no items online  nick:%s"%nick)
            return None 

        item_online_list.extend(rsp.page_item.item_list)

        # continue to call if more than one page
        total_pages = (rsp.page_item.total_item + cls.PAGE_SIZE - 1)/cls.PAGE_SIZE
        if total_pages > max_page:
            total_pages = max_page
        for page_no in range(2,total_pages+1):
            req.page_no = page_no
            rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
            item_online_list.extend(rsp.page_item.item_list)

        logger.debug("actually get %i items online in for nick:%s"%(len(item_online_list), nick))

        return {"item_list":item_online_list, "total_item":rsp.page_item.total_item}

    @classmethod
    @tao_api_exception(3)
    def get_item_count(cls, access_token, nick):
        """
        """
        req = SimbaAdgroupOnlineitemsvonGetRequest()
        req.nick = nick
        req.page_size = cls.PAGE_SIZE
        req.order_field = 'bidCount'
        req.order_by = 'true'
        req.page_no = 1 

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        
        return rsp.page_item.total_item 


def test():
    #access_token = '6201c01b4ZZdb18b1773873390fe3ff66d1a285add9c10c520500325'
    access_token = '620181005f776f4b1bdfd5952ec7cfa172e008384c567a2520500325'
    nick = 'chinchinstyle'
    campaign_id = 3367690 
    items = SimbaAdgroupOnlineitemsvonGet.get_items_online(access_token, nick)
    for item in items:
        print item.toDict()


if __name__ == '__main__':
    test()
