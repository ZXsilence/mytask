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


from TaobaoSdk import ZuanshiBannerCreativeCreateRequest
from TaobaoSdk.Domain.multipart import FileItem,ZuanshiBannerCreativeCreateRequest
from tao_models.common.decorator import  tao_api_exception
from TaobaoSdk.Exceptions import  ErrorResponseException
from shop_db.services.shop_info_service import ShopInfoService
from api_server.conf.settings import APP_SETTINGS,SERVER_URL,API_NEED_SUBWAY_TOKEN,API_HOST,API_PORT
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply


logger = logging.getLogger(__name__)


class ZuanshiCreativeCreate(object):
    """
    TODO
    """

    @classmethod
    @tao_api_exception()
    def create_creative(cls,nick,image_path,name,cat_id,click_url,is_trans_to_wifi=False):
        soft_code = None
        title = 'any.jpg'
        shop_infos = ShopInfoService.get_shop_infos(nick,soft_code,False)
        for shop_info in shop_infos:
            soft_code = shop_info['soft_code']
            access_token = shop_info['access_token']
            appkey = APP_SETTINGS[soft_code]['app_key']
            secret = APP_SETTINGS[soft_code]['app_secret']
            req = ZuanshiBannerCreativeCreateRequest(API_HOST,API_PORT)
            req.set_app_info({'appkey':appkey,'secret':secret})
            req.image = FileItem(title,open(image_path))
            req.name = name
            req.is_trans_to_wifi = str(is_trans_to_wifi).lower()
            req.cat_id = cat_id
            req.click_url = click_url
            try:
                resp= req.getResponse(access_token)
            except Exception,e:
                exception = ErrorResponseException(code=e.errorcode,msg=e.message,sub_code=e.subcode,sub_msg=e.submsg)
                continue
            return resp['zuanshi_banner_creative_create_response']['result']
        if exception:
            raise exception
        else:
            raise ErrorResponseException(code=27,msg='invalid-shop_info',sub_code='invalid-shop_info',sub_msg='can not find valid shop_info')

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    name = 'test_2017_06_07'
    cat_id = 11
    click_url = 'https://detail.tmall.com/item.htm?id=35880138857'
    is_trans_to_wifi = False
    image_path = '/tmp/shoes.jpg'
    print ZuanshiCreativeCreate.create_creative(nick,image_path,name,cat_id,click_url)
