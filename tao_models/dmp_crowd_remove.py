#encoding=utf8
'''
Created on 2012-8-10

@author: dk
'''
import sys
import os
import logging
import logging.config
import json
import datetime
from copy import deepcopy


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import DmpCrowdRemoveRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class DmpCrowdRemove(object):

    @classmethod
    @tao_api_exception()
    def remove_dmp_crowd(cls, nick, crowd_id, soft_code = 'YZB'):
        req = DmpCrowdRemoveRequest()
        req.crowd_id= crowd_id
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.result)

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    try_list = DmpCrowdRemove.remove_dmp_crowd(nick, int(sys.argv[1]))
    import pdb; pdb.set_trace()  # XXX BREAKPOINT
    print try_list
