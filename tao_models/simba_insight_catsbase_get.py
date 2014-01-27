#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import copy

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('api_test')
 
from TaobaoSdk import SimbaInsightCatsbaseGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

class SimbaInsightCatsbaseGet(object):

    @classmethod
    @tao_api_exception(5)
    def get_catsbase(cls, category_ids,time='WEEK',filter='PV,CLICK',nick=None):
        req = SimbaInsightCatsbaseGetRequest()
        req.category_ids = category_ids
        req.time = time
        req.filter = filter
        if nick:
            req.nick = nick
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.in_category_bases)

if __name__ == '__main__':
    print SimbaInsightCatsbaseGet.get_catsbase(u'50010368','WEEK','PV,CLICK','chinchinstyle')

