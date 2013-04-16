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

from TaobaoSdk import SimbaCreativeidsDeletedGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import  taobao_client
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaCreativeidsDeletedGet(object):
    """
    get adgroup deleted since a time
    """
    PAGE_SIZE = 1000 


    @classmethod
    @tao_api_exception()
    def get_creativeids_deleted(cls, access_token, nick, start_time):

        #from  TaobaoSdk import  TaobaoClient
        #SERVER_URL = "http://gw.api.taobao.com/router/rest"
        #APP_KEY='12651461'
        #APP_SECRET = '80a15051c411f9ca52d664ebde46a9da'
        #taobao_client = TaobaoClient(SERVER_URL,APP_KEY , APP_SECRET)
        #creative_ids = []


        creative_id_list = []

        req = SimbaCreativeidsDeletedGetRequest()
        req.nick = nick
        req.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1

        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        if not rsp.deleted_creative_ids:
            logger.debug("get_adgroupids_deleted ---nick:%s start_time:%s total_deleted_adgroups:%s"%(nick,
                                                                                                       start_time,
                                                                                                       0))
            return [] 

        creative_id_list.extend(rsp.deleted_creative_ids)

        while len(rsp.deleted_creative_ids) == cls.PAGE_SIZE:
            req.page_no += 1
            rsp = taobao_client.execute(req, access_token)[0]

            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)
            creative_id_list.extend(rsp.deleted_creative_ids)

        return creative_id_list


def test():
    access_token = "6200024c9db582ca7525fecccbce550cegb5a89cd51492a520500325"
    nick = 'chinchinstyle'
    #start_time = "2013-03-01 03:00:00"
    start_time = datetime(2013,3,8) 
    SimbaCreativeidsDeletedGet.PAGE_SIZE = 1
    creative_ids = SimbaCreativeidsDeletedGet.get_creativeids_deleted(access_token,nick,start_time)

    print 'creative_ids ',creative_ids

if __name__ == '__main__':
    test()
