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

from TaobaoSdk.Request.SimbaSerchcrowdStateBatchUpdateRequest import SimbaSerchcrowdStateBatchUpdateRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SerchcrowdStateBatchUpdate(object):

    @classmethod
    @tao_api_exception()
    def serchcrowdstatebatch_update(cls, nick, adgroup_id, adgroup_crowd_ids, state, soft_code):
        req = SimbaSerchcrowdStateBatchUpdateRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        req.adgroup_crowd_ids = adgroup_crowd_ids
        req.state = state
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.adgrouptargetingtags)


if __name__ == '__main__':
    nick = "麦苗科技001"
    adgroup_id = 700306707
    adgroup_crowd_ids = 284678272590
    state = 0
    soft_code = 'SYB'
    print SerchcrowdStateBatchUpdate.serchcrowdstatebatch_update(nick, adgroup_id, adgroup_crowd_ids, state, soft_code)
