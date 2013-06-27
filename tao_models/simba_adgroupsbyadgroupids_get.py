#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config
import copy

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    #set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')
    set_taobao_client('21065688', '74aecdce10af604343e942a324641891')

from TaobaoSdk import SimbaAdgroupsbyadgroupidsGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaAdgroupsbyadgroupidsGet(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception()
    def get_adgroup_list_by_adgroup_ids(cls, access_token, nick, adgroup_id_list):
        origin_id_list = copy.deepcopy(adgroup_id_list)
        req = SimbaAdgroupsbyadgroupidsGetRequest()
        req.nick = nick
        #useless page_size, page_no, but required when post the request
        req.page_size = cls.PAGE_SIZE 
        req.page_no = 1
        response_dict = {}
        while adgroup_id_list:
            sub_adgroup_id_list = adgroup_id_list[:cls.PAGE_SIZE]
            adgroup_id_list = adgroup_id_list[cls.PAGE_SIZE:]

            req.adgroup_ids = ",".join([str(k) for k in sub_adgroup_id_list])
            logger.debug("get adgroup info adgroup_length:%s nick:%s"%(len(sub_adgroup_id_list), nick))
            rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
            result_adgroup_list = rsp.adgroups.adgroup_list
            for adgroup_object in result_adgroup_list:
                adgroup_id = adgroup_object.toDict()['adgroup_id']
                response_dict[adgroup_id] = adgroup_object

        adgroup_object_list = [None]*(len(origin_id_list))
        for adgroup_id in origin_id_list:
            index = origin_id_list.index(adgroup_id) 
            if response_dict.has_key(adgroup_id):
               adgroup_object_list[index] = response_dict[adgroup_id] 
        return adgroup_object_list 


def test():
    #access_token = '6201c01b4ZZdb18b1773873390fe3ff66d1a285add9c10c520500325'
    access_token = '620181005f776f4b1bdfd5952ec7cfa172e008384c567a2520500325'
    nick = 'chinchinstyle'
    adgroup_ids = [11,166881055,11] 
    #adgroup_ids = [11, 13] 
    adgroups = SimbaAdgroupsbyadgroupidsGet.get_adgroup_list_by_adgroup_ids(access_token, nick, adgroup_ids)
    for adgroup in adgroups:
        print adgroup


if __name__ == '__main__':
    test()
