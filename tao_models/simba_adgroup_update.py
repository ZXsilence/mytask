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

from TaobaoSdk import SimbaAdgroupUpdateRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception
from tao_models.common.exceptions import AdgroupAudictFailedException 

logger = logging.getLogger(__name__)

class SimbaAdgroupUpdate(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(3)
    def update_adgroup(cls, access_token, nick, adgroup_id, default_price, online_status ):
        """
        update an adgroup
        """

        req = SimbaAdgroupUpdateRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id 
        req.default_price = default_price
        #req.nonsearch_max_price = nonsearch_max_price 
        #req.use_nonsearch_default_price = use_nonsearch_default_price 
        req.online_status = online_status 

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            if rsp.sub_msg and u'审核下线的推广组不能手工上下线' in rsp.sub_msg:
                raise AdgroupAudictFailedException
            logger.error("update_adgroup error nick [%s] adgroup_id [%s] msg [%s] sub_msg [%s]" %(nick, 
                str(adgroup_id), rsp.msg, rsp.sub_msg))
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.adgroup



if __name__ == '__main__':

    access_token = '6201011016ade5298c4ZZ0c4bff2e7b98fcad8ebcf11d58520500325'
    nick = 'chinchinstyle'
    adgroup_id = '131326905'
    default_price = '10'
    nonsearch_max_price = '10'
    use_nonsearch_default_price = 'true'
    online_status = 'offline'

    adgroup = SimbaAdgroupUpdate.update_adgroup(access_token, nick, adgroup_id, default_price, nonsearch_max_price , use_nonsearch_default_price, online_status )
    
    print adgroup.toDict()
