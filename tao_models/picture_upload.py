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

from TaobaoSdk import PictureUploadRequest 
from TaobaoSdk.Exceptions import  ErrorResponseException
from TaobaoSdk.Domain.multipart import PictureUploadRequest,FileItem

from tao_models.common.decorator import  tao_api_exception
from shop_db.services.shop_info_service import ShopInfoService
from api_server.conf.settings import APP_SETTINGS,SERVER_URL,API_NEED_SUBWAY_TOKEN,API_HOST,API_PORT
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class PictureUpload(object):
    """
    TODO
    """

    @classmethod
    @tao_api_exception()
    def upload_img(cls,nick,image_path,category_id = 0,title = 'any.jpg'):
        soft_code = None
        shop_infos = ShopInfoService.get_shop_infos(nick,soft_code,False)
        for shop_info in shop_infos:
            soft_code = shop_info['soft_code']
            access_token = shop_info['access_token']
            appkey = APP_SETTINGS[soft_code]['app_key']
            secret = APP_SETTINGS[soft_code]['app_secret']
            req = PictureUploadRequest(API_HOST,API_PORT)
            #req = PictureUploadRequest('121.199.170.144',30002)
            req.set_app_info({'appkey':appkey,'secret':secret})

            image=FileItem(title,open(image_path))
            req.img = image
            req.image = image
            req.picture_category_id = category_id
            req.image_input_title = title

            try:
                resp= req.getResponse(access_token)
            except Exception,e:
                exception = ErrorResponseException(code=e.errorcode,msg=e.message,sub_code=e.subcode,sub_msg=e.submsg)
                continue
            return resp['picture_upload_response'] 
        if exception:
            raise exception
        else:
            raise ErrorResponseException(code=27,msg='invalid-shop_info',sub_code='invalid-shop_info',sub_msg='can not find valid shop_info')
    
if __name__ == '__main__':
    nick = '麦苗科技001'
    image_path = '/alidata1/upload/syb/a.jpg'
    print PictureUpload.upload_img(nick,image_path)
    


