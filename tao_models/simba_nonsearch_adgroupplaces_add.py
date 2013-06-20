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

from TaobaoSdk import SimbaNonsearchAdgroupplacesAddRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaNonsearchAdgroupplacesAdd(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(3)
    def add_nonsearch_adgroupplaces(cls, access_token, nick,campaign_id,adgroup_place_list):
        """
        update an adgroup
        """

        req = SimbaNonsearchAdgroupplacesAddRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.adgroup_places_json = adgroup_place_list

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.adgroup_place_list



if __name__ == '__main__':

    access_token = '62017096de6f96daegibf9b4d214c3a07220daeb9d23226520500325'
    nick = 'chinchinstyle'
    campaign_id = 3367690
    adgroup_ids = [{'adgroupId':169471501,'placeId':11},{'adgroupId':169471501,'placeId':31}]

    SimbaNonsearchAdgroupplacesAdd.add_nonsearch_adgroupplaces(access_token, nick, campaign_id,adgroup_ids)
    

