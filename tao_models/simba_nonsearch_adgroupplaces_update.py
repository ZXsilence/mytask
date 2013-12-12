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
        return_list = []
        req = SimbaNonsearchAdgroupplacesUpdateRequest()
        req.nick = nick
        req.campaign_id = campaign_id

        while adgroup_places_json:
            sub_list = adgroup_places_json[:cls.PAGE_SIZE]
            adgroup_places_json = adgroup_places_json[cls.PAGE_SIZE:]
            try:
                req.adgroup_places_json = sub_list
                rsp = SimbaNonsearchAdgroupplacesUpdate._update_sub_adgroup_places(access_token,req)
            except Exception,e:
                print str(e)+'>>>>>>>'
                continue
            return_list.extend(rsp.adgroup_place_list)
        return return_list

    @classmethod
    @tao_api_exception(8)
    def _update_sub_adgroup_places(cls, access_token,req): 
        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        return rsp


if __name__ == '__main__':

    nick = 'chinchinstyle'
    access_token = '6200d25eac2e3658d2f2bd9b1ebbf36c0ZZ1ff5ca07c4e7520500325'
    campaign_id = 3442512
    adgroup_id = 172111840 
    adgroup_places_json = [{'adgroupId':adgroup_id,'placeId':31,'maxPrice':20,'isDefaultPrice':0}]
    SimbaNonsearchAdgroupplacesUpdate.update_nonsearch_adgroupplaces(access_token, nick,campaign_id,adgroup_places_json)
    print 'successfully'

