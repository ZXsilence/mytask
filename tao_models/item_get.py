#! /usr/bin/env python
#! coding: utf-8 
# author = jyd
# date = 12-8-15


import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    sys.path.append(os.path.join(os.path.dirname(__file__),'../../TaobaoOpenPythonSDK/'))

from TaobaoSdk import ItemGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)


class ItemGet(object):
    """
    TODO
    """

    @classmethod
    @tao_api_exception()
    def get_cid(cls, access_token, num_iid):
        req = ItemGetRequest()
        req.num_iid = num_iid
        req.fields = 'cid'

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg,sub_code=rsp.sub_code,sub_msg =rsp.sub_msg)

        return rsp.item.cid
    
    @classmethod
    @tao_api_exception()
    def get_item_info(cls, access_token, num_iid):
        req = ItemGetRequest()
        req.num_iid = num_iid
        req.fields = 'created,num_iid,title,list_time,price,item_img,pic_url,seller_cids,cid,freight_payer'
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg,sub_code=rsp.sub_code,sub_msg =rsp.sub_msg)

        return rsp.item

if __name__ == '__main__':
    access_token = '6201f21ebfb1b2f040fb3becac3dace9a5a315fb1e7907b871727117'
    tao_model_settings.set_taobao_client('12685542','6599a8ba3455d0b2a043ecab96dfa6f9')
    num_iid = 15500797448 
    item = ItemGet.get_item_info(access_token,num_iid)
    print item.toDict()
