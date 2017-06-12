#encoding=utf8
'''
Created on 2017-5-4

@author: yeyuqiu
'''
import sys
import os
import logging
import logging.config
import json
import datetime
from copy import deepcopy
import simplejson as json

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ZuanshiBannerCrowdUpdateRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply, reduce_list_by_step
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date
logger = logging.getLogger(__name__)


class ZuanshiBannerCrowdUpdate(object):

    @classmethod
    def reduce_crowds_by_step(cls, crowds, step=20):
        """按20长度切分crowds，相同crowd_type的crowd必须在同一个list中"""
        type_crowds_dict = {}
        for crowd in crowds:
            crowd_type = crowd['crowd_type']
            type_crowds_dict.setdefault(crowd_type, []).append(crowd)
        values = type_crowds_dict.values()
        return reduce_list_by_step(values, step)

    @classmethod
    @tao_api_exception()
    def update_crowd(cls, nick, campaign_id, adgroup_id, crowds, soft_code='YZB'):
        """
        3.cpm计划可用定向列表 有哪些
      a. 通投|0
      b. 访客定向|16
      c. 群体定向|8192
      d. 相似宝贝定向-喜欢相似宝贝的人群|131072
      e. 兴趣点定向|64
      f. 营销场景定向|16384
      g. 相似宝贝定向-喜欢我的宝贝的人群|262144
      h. 智能定向-店铺|32768
      i. 达摩盘定向|128
        4.获取全店cpc计划可用定向列表 有哪些
      a. 通投|0
      b. 访客定向|16
      c. 系统智能推荐|65536
      d. CPC营销场景定向|32
      e. 相似宝贝定向-喜欢相似宝贝的人群|131072
      f. 相似宝贝定向-喜欢我的宝贝的人群|262144
      g. 达摩盘定向|128
        """
        req = ZuanshiBannerCrowdUpdateRequest()
        req.campaign_id = campaign_id
        req.adgroup_id = adgroup_id
        crowds_list = cls.reduce_crowds_by_step(crowds) if len(crowds) > 20 else [crowds]
        success_crowd_list = []
        failed_crowd_list = []
        for crowds in crowds_list:
            req.crowds = json.dumps(crowds)
            rsp = ApiService.execute(req, nick, soft_code)
            result = change_obj_to_dict_deeply(rsp.result)
            if result['success']:
                success_crowd_list.extend(crowds)
            else:
                failed_crowd_list.extend(crowds)
        result = {
            'success': False if failed_crowd_list else True,
            'success_list': success_crowd_list,
            'failed_list': failed_crowd_list
        }
        return result

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    campaign_id = 217069448
    adgroup_id = 222632391
    crowds = [{'crowd_type':16, 'crowd_value':'1', 'sub_crowds':[{'sub_crowd_name':u'优美妮旗舰店'}],'matrix_prices':[{'adzone_id':34492608, 'price':5}]}]
    result = ZuanshiBannerCrowdUpdate.update_crowd(nick, campaign_id, adgroup_id, crowds)
    print result
