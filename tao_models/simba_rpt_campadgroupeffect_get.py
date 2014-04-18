'''
Created on 2012-9-4

@author: dk

'''
#encoding=utf8
import sys
import os
import json
import datetime
import logging

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaRptCampadgroupeffectGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaRptCampadgroupEffectGet(object):

    @classmethod
    @tao_api_exception(10)
    def _get_rpt_adgroupeffect_list(cls, nick, campaign_id, start_time, end_time, search_type, source, page_no):
        req = SimbaRptCampadgroupeffectGetRequest()
        req.nick = nick 
        req.campaign_id = campaign_id
        req.start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d')
        req.end_time = datetime.datetime.strftime(end_time, '%Y-%m-%d')
        req.search_type = search_type
        req.source = source
        req.page_no = page_no
        req.page_size = 500
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        l =  json.loads(rsp.rpt_campadgroup_effect_list.lower())
        if l == {}:
            l = []
        if isinstance(l, dict):
            raise ErrorResponseException(code=l['code'], msg=l['msg'], sub_code=l['sub_code'], sub_msg=l['sub_msg'])
        for rpt in l:
            rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')
        return l

    @classmethod
    def get_rpt_adgroupeffect_list(cls, nick, campaign_id, start_time, end_time, search_type, source):
        page_no = 1
        effect_list = []
        while True:  
            subeffect_list = SimbaRptCampadgroupEffectGet._get_rpt_adgroupeffect_list(\
                    nick, campaign_id, start_time, end_time, search_type,\
                    source, page_no)

            effect_list.extend(subeffect_list)
            if len(subeffect_list) < 500:
                break
            page_no += 1
        return change_obj_to_dict_deeply(effect_list)


if __name__ == '__main__':
    nick = 'chinchinstyle'
    campaign_id = 3367748
    adgroup_id = 336844923
    search_type = 'SEARCH,CAT'
    source = '1,2'
    start_time = datetime.datetime.now() - datetime.timedelta(days=10)
    end_time = datetime.datetime.now() - datetime.timedelta(days=1)
    try_list = SimbaRptCampadgroupEffectGet.get_rpt_adgroupeffect_list(nick, campaign_id, start_time, end_time, search_type, source)
    for item in try_list:
        print item
        
