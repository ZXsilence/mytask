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

from TaobaoSdk import ItemJointImgRequest 
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class ItemJointImg(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(4)
    def joint_img(cls, nick, num_iid, pic_path):

        req = ItemJointImgRequest()
        req.num_iid = num_iid
        req.pic_path = pic_path
        #req.is_major = 'true' 
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.item_img)

if __name__ == '__main__':

    nick = 'chinchinstyle'
    num_iid = 7794896442
    pic_path = 'i1/520500325/T2ZBhTXXNbXXXXXXXX_!!520500325.jpg'
    result = ItemJointImg.joint_img(nick,num_iid ,pic_path)
    print result
    
