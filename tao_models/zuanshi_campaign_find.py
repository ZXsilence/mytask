#encoding=utf8
'''
Created on 2012-8-10

@author: dk
'''
import sys
import os
import logging
import logging.config
import json
import datetime
from copy import deepcopy


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ZuanshiBannerCampaignFindRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class ZuanshiCampaignFind(object):

    page_size  = 200

    @classmethod
    def get_campaign_list(cls, nick,name = None,campaign_id_list  = [],status_list = [] ,type = None,soft_code = 'YZB'):
        campaign_list = []
        page_num = 1
        while True:
            tmp_list = cls.__get_sub_campaign_list(nick,name = name,campaign_id_list = campaign_id_list,status_list = status_list,type = type,page_num = page_num,soft_code = soft_code)
            if tmp_list:
                campaign_list.extend(tmp_list)
            if not tmp_list or len(tmp_list) < cls.page_size:
                break;
            page_num +=1
        return campaign_list

    @classmethod
    @tao_api_exception()
    def __get_sub_campaign_list(cls, nick,name = None,campaign_id_list  = [],status_list = [] ,type = None,page_num = 1,soft_code = 'YZB'):
        #获取计划列表
        req = ZuanshiBannerCampaignFindRequest()
        if name:
            req.name = name
        if campaign_id_list:
            req.campaign_id_list = ','.join(str(campaign_id) for campaign_id in campaign_id_list)
        if status_list:
            req.status_list = ','.join(str(status) for status in status_list)
        if type:
            req.type = type
        req.page_num = page_num
        req.page_size = cls.page_size
        rsp = ApiService.execute(req,nick,soft_code)
        if change_obj_to_dict_deeply(rsp.result).get('campaigns'):
            return change_obj_to_dict_deeply(rsp.result).get('campaigns')['campaign']
        else:
            return None

if __name__ == '__main__':
    nick = '麦苗科技001'
    try_list = ZuanshiCampaignFind.get_campaign_list(nick)
    for obj in try_list:
        print obj
