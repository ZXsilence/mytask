#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import copy

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')
 
from TaobaoSdk import SimbaInsightCatsbaseGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

class SimbaInsightCatsbaseGet(object):

    @classmethod
    @tao_api_exception(5)
    def get_catsbase(cls, access_token, category_ids,time='WEEK',filter='PV,CLICK'):
        req = SimbaInsightCatsbaseGetRequest()
        req.category_ids = category_ids
        req.time = time
        req.filter = filter
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        return rsp.in_category_bases
if __name__ == '__main__':
    access_token = '6201a2274ba002ff3a49a801d32227ZZ239c6b4da4087e8871727117'
    print SimbaInsightCatsbaseGet.get_catsbase(access_token, u'50010368')
