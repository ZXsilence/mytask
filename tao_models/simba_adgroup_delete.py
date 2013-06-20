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

from TaobaoSdk import SimbaAdgroupDeleteRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaAdgroupDelete(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(4)
    def delete_adgroup(cls, access_token, nick, adgroup_id):
        """
        given a campaign_id, get the adgroup list in this campaign
        """

        req = SimbaAdgroupDeleteRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id 

        #first_call
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            logger.error("delete_adgroup error nick [%s] adgroup_id [%s] msg [%s] sub_msg [%s]" %(nick
                 , str(adgroup_id), rsp.msg, rsp.sub_msg))
            print "delete_adgroup:", rsp.msg, "\t", rsp.sub_msg
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.adgroup



if __name__ == '__main__':

    access_token = '6201d21d3bfa761000e15d6f4c1d3ZZ2331a6010d1ab4a8520500325'
    nick = 'chinchinstyle'
    adgroup_id = '230226374'

    adgroup = SimbaAdgroupDelete.delete_adgroup(access_token, nick, adgroup_id)
    
    print adgroup.toDict()
