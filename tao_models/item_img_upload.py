#! /usr/bin/env python
#! coding: utf-8 
# author = jyd
# date = 12-8-15


import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ItemImgUploadRequest 
from TaobaoSdk.Exceptions import  ErrorResponseException
from TaobaoSdk.Domain.multipart import ItemImgUploadRequest,FileItem

from tao_models.common.decorator import  tao_api_exception
from shop_db.services.shop_info_service import ShopInfoService
from api_server.conf.settings import APP_SETTINGS,SERVER_URL,API_NEED_SUBWAY_TOKEN,API_HOST,API_PORT

logger = logging.getLogger(__name__)


class ItemImgUpload(object):
    """
    TODO
    """

    @classmethod
    @tao_api_exception()
    def upload_img(cls,nick,num_iid,image_path):
        soft_code = None
        session_expired = False
        exception = None
        shop_infos = ShopInfoService.get_shop_infos(nick,soft_code,session_expired)
        for shop_info in shop_infos:
            soft_code = shop_info['soft_code']
            access_token = shop_info['access_token']
            appkey = APP_SETTINGS[soft_code]['app_key']
            secret = APP_SETTINGS[soft_code]['app_secret']
            req = ItemImgUploadRequest(API_HOST,API_PORT)
            req.set_app_info({'appkey':appkey,'secret':secret})

            req.num_iid = num_iid
            image=FileItem('any.jpg',open(image_path))
            req.image= image

            #req.position=1
            #req.id=12345
            #req.is_major=True

            try:
                resp= req.getResponse(access_token)
            except Exception,e:
                exception = ErrorResponseException(code=e.errorcode,msg=e.message,sub_code=e.subcode,sub_msg=e.submsg)
                continue
            return resp['item_img_upload_response'] 
        if exception:
            raise exception
        else:
            raise ErrorResponseException(code=27,msg='invalid-shop_info',sub_code='invalid-shop_info',sub_msg='can not find valid shop_info')
    
if __name__ == '__main__':
    nick = '麦苗科技001'
    num_iid =18261147964 
    image_path = '/alidata1/upload/syb/a.jpg'
    print ItemImgUpload.upload_img(nick,num_iid,image_path)
