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

from TaobaoSdk import SimbaNonsearchAdgroupplacesGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaNonsearchAdgroupplacesGet(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(3)
    def get_nonsearch_adgroupplaces(cls, access_token, nick, campaign_id,adgroup_id_list):
        """
        update an adgroup
        """

        req = SimbaNonsearchAdgroupplacesGetRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        adgroup_ids = ','.join([str(adgroup_id) for adgroup_id in adgroup_id_list])
        req.adgroup_ids = adgroup_ids
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            logger.error("get_Adgroupplaces error nick [%s] adgroup_id [%s] msg [%s] sub_msg [%s]" %(nick, 
                str(adgroup_ids), rsp.msg, rsp.sub_msg))
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.adgroup_place_list



if __name__ == '__main__':

    access_token = '62017096de6f96daegibf9b4d214c3a07220daeb9d23226520500325'
    nick = 'chinchinstyle'
    campaign_id = 3367690
    adgroup_ids = [169471501]

    places_list = SimbaNonsearchAdgroupplacesGet.get_Adgroupplaces(access_token, nick, campaign_id,adgroup_ids)
    
    for place in places_list:
        print place.toDict()

