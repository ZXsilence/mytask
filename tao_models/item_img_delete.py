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

from TaobaoSdk import ItemImgDeleteRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class ItemImgDelete(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(4)
    def delete_item_img(cls, access_token, num_iid, img_id):
        """
        given a campaign_id, get the adgroup list in this campaign
        """

        req = ItemImgDeleteRequest()
        req.num_iid = num_iid
        req.id = img_id 

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.item_img



if __name__ == '__main__':

    access_token = '6201d21d3bfa761000e15d6f4c1d3ZZ2331a6010d1ab4a8520500325'
    nick = 'chinchinstyle'
    num_iid = 7794896442
    img_id = 6686031561
    result = ItemImgDelete.delete_item_img(access_token ,num_iid ,img_id )
    print result.toDict()

    
