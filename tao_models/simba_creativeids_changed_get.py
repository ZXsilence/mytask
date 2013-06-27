#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'


import sys
import os
import logging
import logging.config
from datetime import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    sys.path.append(os.path.join(os.path.dirname(__file__),'../../TaobaoOpenPythonSDK/'))

from TaobaoSdk import SimbaCreativeidsChangedGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import  taobao_client
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)


class SimbaCreativeidsChangedGet(object):
    """
    get adgroups changed since a start_time
    """

    PAGE_SIZE = 1000

    @classmethod
    @tao_api_exception()
    def get_creative_ids_changed(cls, access_token, nick, start_time):
        """

        return format:

        """
        #from  TaobaoSdk import  TaobaoClient
        #SERVER_URL = "http://gw.api.taobao.com/router/rest"
        #APP_KEY='12651461'
        #APP_SECRET = '80a15051c411f9ca52d664ebde46a9da'
        #taobao_client = TaobaoClient(SERVER_URL,APP_KEY , APP_SECRET)
        #creative_ids = []

        req = SimbaCreativeidsChangedGetRequest()
        req.nick = nick
        req.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1

        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        return rsp.changed_creative_ids


def test():
    access_token = "6200024c9db582ca7525fecccbce550cegb5a89cd51492a520500325"
    nick = 'chinchinstyle'
    #start_time = "2013-03-01 03:00:00"
    start_time = datetime(2013,3,8) 
    SimbaCreativeidsChangedGet.PAGE_SIZE = 1000
    creative_ids = SimbaCreativeidsChangedGet.get_creative_ids_changed(access_token,nick,start_time)

    print 'creative_ids ',creative_ids

if __name__ == '__main__':
    test()
