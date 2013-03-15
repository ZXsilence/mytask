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

from TaobaoSdk import SimbaNonsearchAdgroupplacesUpdateRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception
from tao_models.common.util import get_test_token_dict

logger = logging.getLogger(__name__)

class SimbaNonsearchAdgroupplacesUpdate(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    #@tao_api_exception(3)
    def update_nonsearch_adgroupplaces(cls, access_token, nick,campaign_id,adgroup_places_json):
        """
        update an adgroup
        """

        req = SimbaNonsearchAdgroupplacesUpdateRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.adgroup_places_json = adgroup_places_json

        rsp = taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.adgroup_place_list



if __name__ == '__main__':

    nick = 'chinchinstyle'
    shop_info = get_test_token_dict('rmt',nick)
    access_token = shop_info['access_token'] 
    campaign_id = 3442512
    adgroup_id = 172111840 
    adgroup_places_json = [{'adgroupId':adgroup_id,'placeId':31,'maxPrice':20,'isDefaultPrice':0}]
    SimbaNonsearchAdgroupplacesUpdate.update_nonsearch_adgroupplaces(access_token, nick,campaign_id,adgroup_places_json)
    print 'successfully'

