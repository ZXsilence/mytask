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
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12651461', '80a15051c411f9ca52d664ebde46a9da')

from TaobaoSdk import ItemsOnsaleGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)


class ItemsOnsaleGet(object):

    DEFAULT_FIELDS = 'title,price,pic_url,num_iid'

    @classmethod
    @tao_api_exception()
    def get_item_list(cls, access_token, max_pages=30, fields=DEFAULT_FIELDS):

        total_item_list = []

        req = ItemsOnsaleGetRequest()
        req.fields = fields
        req.order_by = "modified:desc" 
        req.page_size = 200
        req.page_no = 1 
        access_token = ''

        while True:

            rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

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

        return total_item_list

    @classmethod
    @tao_api_exception()
    def get_item_list_with_overview(cls, access_token, max_pages=1, fields=DEFAULT_FIELDS):

        total_item_list = []

        req = ItemsOnsaleGetRequest()
        req.fields = fields
        req.order_by = "modified:desc" 
        req.page_size = 2
        req.page_no = 1 

        while True:

            rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

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

        return {'total_results':rsp.total_results, 'item_list':total_item_list} 

def test():
    access_token = "620260146ZZc0465e1b4185f7b4ca8ba1c7736c28d1c675871727117"
    #fields = 'title,price,pic_url,num_iid,detail_url,props_name,cid,list_time,delist_time,modified'
    total_item_list = ItemsOnsaleGet.get_item_list(access_token)

    print len(total_item_list)
    for item in total_item_list:
        print item.toDict()

def test_overview():
    access_token = "620260146ZZc0465e1b4185f7b4ca8ba1c7736c28d1c675871727117"
    #fields = 'title,price,pic_url,num_iid,detail_url,props_name,cid,list_time,delist_time,modified'
    items_overview = ItemsOnsaleGet.get_item_list_with_overview(access_token)
    
    print items_overview['total_results']
    for item in items_overview['item_list']:
        print item.toDict()

if __name__ == '__main__':
    #test()
    test_overview()
