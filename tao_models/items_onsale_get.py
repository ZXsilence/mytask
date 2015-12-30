#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ItemsOnsaleGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from TaobaoSdk import TaobaoClient
from TaobaoSdk.Exceptions import ErrorResponseException
from api_server.conf.settings import APP_SETTINGS,SERVER_URL,API_NEED_SUBWAY_TOKEN,API_SOURCE

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
    def get_item_list(cls, nick, max_pages=50, fields=DEFAULT_FIELDS):

        total_item_list = []

        req = ItemsOnsaleGetRequest()
        req.fields = fields
        req.order_by = "sold_quantity:desc"
        req.page_size = 200
        req.page_no = 1

        while True:
            rsp = cls._get_page_items(req,nick)
            if rsp.items is None:
                logger.info("get item info, but none return")
                break
            logger.info("get item info, actually return: %s"%(len(rsp.items)))
            total_item_list.extend(rsp.items)
            print req.page_no

            if len(rsp.items) != req.page_size:
                break
            if req.page_no == max_pages:
                break
            req.page_no += 1

        return change_obj_to_dict_deeply(total_item_list)

    @classmethod
    def get_item_list_with_page_no(cls,nick,page_no,fields=DEFAULT_FIELDS):
        req = ItemsOnsaleGetRequest()
        req.fields = fields
        req.order_by = "sold_quantity:desc"
        req.page_size = 200
        req.page_no = page_no
        rsp = cls._get_page_items(req,nick)
        if rsp.items:
            return change_obj_to_dict_deeply(rsp.items)
        return []

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


    @classmethod
    @tao_api_exception()
    def get_item_list_overview_with_access_token(cls,soft_code,access_token,fields=DEFAULT_FIELDS):
        req = ItemsOnsaleGetRequest()
        req.fields = fields
        req.order_by = "modified:desc"
        req.page_size = 2
        req.page_no = 1

        app_key = APP_SETTINGS[soft_code]['app_key']
        app_secret = APP_SETTINGS[soft_code]['app_secret']
        params = ApiService.getReqParameters(req)
        taobao_client = TaobaoClient(SERVER_URL,app_key,app_secret)
        params['method'] = 'taobao.items.onsale.get'
        rsp = ApiService.getResponseObj(taobao_client.execute(params, access_token))
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg,params=params,rsp=rsp)
        return {'total_results':change_obj_to_dict_deeply(rsp.total_results), 'item_list':change_obj_to_dict_deeply(rsp.items)}



def test():
    nick = '纸老虎图书专营店'
    total_item_list = ItemsOnsaleGet.get_item_list(nick)

def test_overview():
    nick = '麦苗科技001'
    items_overview = ItemsOnsaleGet.get_item_list_with_overview(nick)
    print items_overview['total_results']

if __name__ == '__main__':
    import pdb; pdb.set_trace()  # XXX BREAKPOINT
    nick = "麦苗科技001"
    print ItemsOnsaleGet.get_item_list_with_page_no(nick,2)
    test_overview()
