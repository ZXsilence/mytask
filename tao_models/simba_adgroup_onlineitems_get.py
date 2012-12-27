#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'



import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from xuanciw.settings import  trigger_envReady
    logging.config.fileConfig('../xuanciw/consolelogger.conf')

from TaobaoSdk import SimbaAdgroupOnlineitemsGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import  taobao_client
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)


class SimbaAdgroupOnlineitemsGet(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception()
    def get_items_online(cls, access_token, nick, max_page = 30):
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

        req = SimbaAdgroupOnlineitemsGetRequest()
        req.nick = nick
        req.page_size = cls.PAGE_SIZE

        #first call
        req.page_no = 1
        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

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
            rsp = taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)
            item_online_list.extend(rsp.page_item.item_list)

        logger.debug("actually get %i items online in for nick:%s"%(len(item_online_list), nick))

        return item_online_list

    @classmethod
    @tao_api_exception(3)
    def get_item_count(cls, access_token, nick):
        """
        """
        req = SimbaAdgroupOnlineitemsGetRequest()
        req.nick = nick
        req.page_size = cls.PAGE_SIZE
        req.order_field = 'bidCount'
        req.order_by = 'true'
        req.page_no = 1 

        try:
            rsp = taobao_client.execute(req, access_token)[0]
        except Exception, data:
            raise ApiExecuteException

        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.page_item.total_item 



def test():
    access_token = "6200b26ad6dde0735bc63c45618ca4f8bdfhfc1dfd08854100160612"
    nick = '密多帮巴'
    SimbaAdgroupOnlineitemsGet.PAGE_SIZE = 200
    item_online_list = SimbaAdgroupOnlineitemsGet.get_items_online(access_token, nick)
    print len(item_online_list)



if __name__ == '__main__':
    test()


