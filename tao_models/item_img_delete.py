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
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import ItemImgDeleteRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class ItemImgDelete(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(4)
    def delete_item_img(cls, nick, num_iid, img_id):

        req = ItemImgDeleteRequest()
        req.num_iid = num_iid
        req.id = img_id 
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.item_img)

if __name__ == '__main__':
    nick = 'chinchinstyle'
    num_iid = 7794896442
    img_id = 6686031561
    print ItemImgDelete.delete_item_img(nick,num_iid ,img_id )

    
