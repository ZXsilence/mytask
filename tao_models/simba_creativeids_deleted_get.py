#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'


import sys
import os
import logging
import logging.config
from datetime import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaCreativeidsDeletedGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaCreativeidsDeletedGet(object):
    """
    get adgroup deleted since a time
    """
    PAGE_SIZE = 1000 


    @classmethod
    @tao_api_exception()
    def get_creativeids_deleted(cls, nick, start_time):
        creative_id_list = []
        req = SimbaCreativeidsDeletedGetRequest()
        req.nick = nick
        req.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        if not rsp.deleted_creative_ids:
            logger.debug("get_adgroupids_deleted ---nick:%s start_time:%s total_deleted_adgroups:%s"%(nick,
                                                                                                       start_time,
                                                                                                       0))
            return [] 
        creative_id_list.extend(rsp.deleted_creative_ids)
        while len(rsp.deleted_creative_ids) == cls.PAGE_SIZE:
            req.page_no += 1
            soft_code = None
            rsp = ApiService.execute(req,nick,soft_code)
            creative_id_list.extend(rsp.deleted_creative_ids)
        return change_obj_to_dict_deeply(creative_id_list)

def test():
    nick = 'chinchinstyle'
    start_time = datetime(2014,1,1) 
    SimbaCreativeidsDeletedGet.PAGE_SIZE = 1000
    creative_ids = SimbaCreativeidsDeletedGet.get_creativeids_deleted(nick,start_time)
    print 'creative_ids ',creative_ids

if __name__ == '__main__':
    test()
