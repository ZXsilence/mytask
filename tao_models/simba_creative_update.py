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
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import SimbaCreativeUpdateRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaCreativeUpdate(object):

    @classmethod
    @tao_api_exception(5)
    def update_creative(cls, nick, adgroup_id, creative_id, img_url, title):
        """
        update a creative in adgroup
        """
        req = SimbaCreativeUpdateRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        req.creative_id = creative_id
        req.img_url = img_url
        req.title = title
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.creativerecord)


if __name__ == '__main__':
    nick = 'chinchinstyle'
    campaign_id = 3367748
    adgroup_id = 345679857
    creative_id = 373504976 
    title = '你好新世界'
    img_url = 'http://img01.taobaocdn.com/bao/uploaded/i1/T1VM64Xk0jXXcYck3T_012555.jpg'
    creativerecord = SimbaCreativeUpdate.update_creative(nick, adgroup_id, creative_id, img_url, title)
    print creativerecord

