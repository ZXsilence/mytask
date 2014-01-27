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
    from api_server.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')

from TaobaoSdk import TaobaoJindouCloudMessageSendRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)


class MessageSend(object):

    @classmethod
    @tao_api_exception()
    def send_message(cls, access_token):
        req = TaobaoJindouCloudMessageSendRequest()
        req.messages = [{"nick": "chinchinstyle","title": "测试titleasdf","view_data": ["展示数据10","展示数据20"],"send_no": '126855425205003251',"msg_category":"item","msg_type":"ItemAdd"}]
        import pdb;pdb.set_trace()
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg,sub_code=rsp.sub_code,sub_msg =rsp.sub_msg)

        return rsp.item.cid
    
if __name__ == '__main__':
    access_token = '6200d25eac2e3658d2f2bd9b1ebbf36c0ZZ1ff5ca07c4e7520500325'
    MessageSend.send_message(access_token)
