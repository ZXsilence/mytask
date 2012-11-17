#! /usr/bin/env python
#! coding: utf-8 
# author = jyd
# date = 12-8-16

import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from xuanciw.settings import  trigger_envReady
    logging.config.fileConfig('../xuanciw/consolelogger.conf')

from TaobaoSdk import SimbaAdgroupsItemExistRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import  taobao_client
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)

class SimbaAdgroupsItemExist(object):
    """
    TODO
    """

    @classmethod
    @tao_api_exception
    def is_adgroup_item_exist(cls,nick , access_token, campaign_id, num_iid):
        req = SimbaAdgroupsItemExistRequest()
        req.campaign_id = campaign_id
        req.item_id = num_iid
        req.nick = nick

        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        return rsp.exist