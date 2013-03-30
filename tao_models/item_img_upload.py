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
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12651461', '80a15051c411f9ca52d664ebde46a9da')

from TaobaoSdk import ItemImgUploadRequest 
from TaobaoSdk.Exceptions import  ErrorResponseException
from TaobaoSdk.Domain.multipart import ItemImgUploadRequest,FileItem

from tao_models.conf import  settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)


class ItemImgUpload(object):
    """
    TODO
    """

    @classmethod
    @tao_api_exception()
    def upload_img(cls,access_token, num_iid,image_path):
        appkey = tao_model_settings.taobao_client.appKey
        secret = tao_model_settings.taobao_client.appSecret
        req = ItemImgUploadRequest()
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
            raise ErrorResponseException(code=e.errorcode,msg=e.message,sub_code=e.subcode,sub_msg=e.submsg)

        return resp['item_img_upload_response'] 
    
if __name__ == '__main__':
    access_token = '6202302294ZZbc448bcdca4be425fcdbfdbf692a463a82b520500325'
    num_iid =7794896442 
    image_path = '/home/wulingping/test.png'
    #ItemImgUpload.upload_img_tao_api(access_token,num_iid,image)
    print ItemImgUpload.upload_img(access_token,num_iid,image_path)
    


