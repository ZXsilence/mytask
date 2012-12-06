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
    from xuanciw.settings import  trigger_envReady
    logging.config.fileConfig('../xuanciw/consolelogger.conf')

from TaobaoSdk import ItemGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import  taobao_client
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

        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg,sub_code=rsp.sub_code,sub_msg =rsp.sub_msg)

        return rsp.item.cid
