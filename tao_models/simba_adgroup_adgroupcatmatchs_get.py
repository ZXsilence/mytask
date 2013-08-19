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

from TaobaoSdk import SimbaAdgroupAdgroupcatmatchsGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaAdgroupAdgroupcatmatchsGet(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(3)
    def get_adgroup_catmatchs(cls, access_token, nick, adgroup_ids):
        """
        get adgroup catmatchs
        """
        adgroup_ids_str = [str(adgroup_id) for adgroup_id in adgroup_ids]
        req = SimbaAdgroupAdgroupcatmatchsGetRequest()
        req.nick = nick
        req.adgroup_ids = ','.join(adgroup_ids_str)

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            logger.debug("get_adgroup_catmatchs error nick [%s] adgroup_id [%s] msg [%s] sub_msg [%s]" %(nick, 
                str(adgroup_id), rsp.msg, rsp.sub_msg))
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.adgroup_catmatch_list 



if __name__ == '__main__':

    access_token = '6200b16f59ac4c0501c11e7fhj59b5b50bfc9591c98afe2520500325'
    nick = 'chinchinstyle'
    adgroup_id = '162709345'

    adgroup_catmatch_list = SimbaAdgroupAdgroupcatmatchsGet.get_adgroup_catmatchs(
            access_token, nick, [adgroup_id])
    
    for adgroup_catmatch in adgroup_catmatch_list:
        print adgroup_catmatch.toDict()
