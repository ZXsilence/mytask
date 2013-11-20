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

from TaobaoSdk import SimbaAdgroupNonsearchpricesUpdateRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaAdgroupNonsearchpricesUpdate(object):

    PAGESIZE = 200

    @classmethod
    @tao_api_exception(1)
    def set_adgroups_nonsearchprices(cls,access_token,nick,campaign_id,adgroupid_price_json):
        if not adgroupid_price_json:
            return []
        return_list = []
        size = cls.PAGESIZE
        page_num = len(adgroupid_price_json)/size+ 1
        if len(adgroupid_price_json) % size== 0:
            page_num -= 1
        for i in range(page_num):
            sub_json_list= adgroupid_price_json[i*size: (i+1)*size]
            adgroup_list = SimbaAdgroupNonsearchpricesUpdate.sub_set_adgroups_nonsearchprices(access_token,nick,campaign_id,sub_json_list)
            return_list.extend(adgroup_list)
        return return_list


    @classmethod
    @tao_api_exception(10)
    def sub_set_adgroups_nonsearchprices(cls,access_token,nick,campaign_id,adgroupid_price_json):
        req = SimbaAdgroupNonsearchpricesUpdateRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.adgroupid_price_json = adgroupid_price_json
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            logger.debug("set_adgroups_nonsearchstates error nick [%s] adgroupid_price_json [%s] msg [%s] sub_msg [%s]" %(nick, adgroupid_price_json, rsp.msg, rsp.sub_msg))
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        
        return rsp.adgroup_list


