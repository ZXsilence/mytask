#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: lichen
@contact: lichen@maimiaotech.com
@date: 2017-05-24 17:52
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""


import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ZuanshiBannerCreativeModifyRequest
from TaobaoSdk.Domain.multipart import FileItem, ZuanshiBannerCreativeModifyRequest
from TaobaoSdk.Exceptions import  ErrorResponseException
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from shop_db.services.shop_info_service import ShopInfoService
from api_server.conf.settings import APP_SETTINGS,SERVER_URL,API_NEED_SUBWAY_TOKEN,API_HOST,API_PORT
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class ZuanshiCreativeModify(object):


    @classmethod
    @tao_api_exception()
    def modify_creative(cls,nick,params):
        soft_code = None
        shop_infos = ShopInfoService.get_shop_infos(nick,soft_code,False)
        title = 'any.jpg'
        for shop_info in shop_infos:
            soft_code = shop_info['soft_code']
            access_token = shop_info['access_token']
            appkey = APP_SETTINGS[soft_code]['app_key']
            secret = APP_SETTINGS[soft_code]['app_secret']
            req = ZuanshiBannerCreativeModifyRequest(API_HOST,API_PORT)
            req.set_app_info({'appkey':appkey,'secret':secret})

            req.id = params['id']
            if params.get("name"):
                req.name = params['name']
            req.is_trans_to_wifi = str(params['is_trans_to_wifi']).lower()
            if params.get('image'):
                req.image = FileItem(title,open(params['image_path']))
            if params.get('cat_id'):
                req.cat_id = params['cat_id']
            if params.get('click_url'):
                req.click_url = params['click_url']

            try:
                resp= req.getResponse(access_token)
            except Exception,e:
                exception = ErrorResponseException(code=e.errorcode,msg=e.message,sub_code=e.subcode,sub_msg=e.submsg)
                continue
            return resp['zuanshi_banner_creative_modify_response']['result']
        if exception:
            raise exception
        else:
            raise ErrorResponseException(code=27,msg='invalid-shop_info',sub_code='invalid-shop_info',sub_msg='can not find valid shop_info')

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    soft_code = 'YZB'
    params = {'id': 805164400001, 'name': 'carlos_lee_test', 'is_trans_to_wifi': False}
    res = ZuanshiCreativeModify.modify_creative(nick,params)
    print res
