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
    set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')

from TaobaoSdk import SimbaCreativeUpdateRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaCreativeUpdate(object):

    @classmethod
    @tao_api_exception(5)
    def update_creative(cls, access_token, nick, adgroup_id, creative_id, img_url, title):
        """
        update a creative in adgroup
        """
        req = SimbaCreativeUpdateRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        req.creative_id = creative_id
        req.img_url = img_url
        req.title = title

        rsp = taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            logger.error("update_creative error nick [%s] adgroup_id [%s] msg [%s] sub_msg [%s]" %(nick
                , str(adgroup_id), rsp.msg, rsp.sub_msg))
            if '图片不是推广组的图片' in rsp.sub_msg:
                raise ImgNotBelongToAdgroupException
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.creativerecord


if __name__ == '__main__':
    access_token = '6201011016ade5298c4ZZ0c4bff2e7b98fcad8ebcf11d58520500325'
    nick = 'chinchinstyle'
    adgroup_id = '131326905'
    creative_id = '139123226' 
    img_url = 'http://img07.taobaocdn.com/bao/uploaded/i7/T1yvupXmNAXXbmMCkY_030501.jpg'
    title = '你好新世界'
    creativerecord = SimbaCreativeUpdate.update_creative(access_token, nick, adgroup_id, creative_id, img_url, title)

    print creativerecord.toDict()

