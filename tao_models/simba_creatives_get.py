#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12651461', '80a15051c411f9ca52d664ebde46a9da')

from TaobaoSdk import SimbaCreativesGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaCreativesGet(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(25)
    def get_creative_list_by_adgroup(cls, access_token, nick, adgroup_id):
        """
        given a adgroup_id, get the creative list in this adgroup
        """

        creative_list = []

        req = SimbaCreativesGetRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        #req.creative_ids = ",".join([str(k) for k in creative_ids])

        rsp = taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            logger.error("get_creative_list_by_adgroup error nick [%s] msg [%s] sub_msg [%s]" %(nick
                , rsp.msg, rsp.sub_msg))
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.creatives


if __name__ == '__main__':
    nick = 'chinchinstyle'
    access_token = '6200e168f708b8167250268dfhe2555e99ed247caa1cdeb520500325'
    adgroup_id =164302433 
    nick = 'chinchinstyle'
    
    creatives = SimbaCreativesGet.get_creative_list_by_adgroup(access_token, nick, adgroup_id)

    for creative in creatives:
        print creative.toDict()
