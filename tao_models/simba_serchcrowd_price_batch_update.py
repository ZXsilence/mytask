# -*- coding: utf-8 -*-
'''
Created on 2012-11-3

@author: dk
'''
import sys
import os
import logging
import logging.config
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk.Request.SimbaSerchcrowdPriceBatchUpdateRequest import SimbaSerchcrowdPriceBatchUpdateRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SerchcrowdPriceBatchUpdate(object):

    @classmethod
    @tao_api_exception()
    def serchcrowdpricebatch_update(cls, nick, sub_nick, adgroup_id, adgroup_crowd_ids, discount, soft_code):
        req = SimbaSerchcrowdPriceBatchUpdateRequest()
        req.nick = nick
        req.sub_nick = sub_nick
        req.adgroup_id = adgroup_id
        req.adgroup_crowd_ids = ','.join([str(d) for d in adgroup_crowd_ids]) 
        req.discount = discount
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.adgrouptargetingtags)


if __name__ == '__main__':
    nick = "麦苗科技001"
    sub_nick = None
    adgroup_id = 700306707
    adgroup_crowd_ids = None
    discount = None
    soft_code = 'SYB'
    print SerchcrowdPriceBatchUpdate.serchcrowdpricebatch_update(nick, sub_nick, adgroup_id, adgroup_crowd_ids, discount, soft_code)
