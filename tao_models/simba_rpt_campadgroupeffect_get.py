'''
Created on 2012-9-4

@author: dk

'''
#encoding=utf8
import sys
import os
import json
import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')

from TaobaoSdk import SimbaRptCampadgroupEffectGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception
from date_handle import DateHandle

class SimbaRptCampadgroupEffectGet(object):
    """
    """
    @classmethod
    @tao_api_exception(10)
    def _get_rpt_adgroupeffect_list(cls, nick, campaign_id, start_time, end_time, search_type, source, access_token, subway_token, page_no):
        req = SimbaRptCampadgroupeffectGetRequest()
        req.nick = nick 
        req.campaign_id = campaign_id
        req.start_time = DateHandle.date_to_ustring(start_time)
        req.end_time = DateHandle.date_to_ustring(end_time)
        req.search_type = search_type
        req.source = source
        req.subway_token = subway_token
        req.page_no = page_no
        req.page_size = 500
        
        rsp = taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        return json.loads(rsp.rpt_campadgroup_effect_list)

    @classmethod
    def get_rpt_adgroupeffect_list(cls, nick, campaign_id, start_time, end_time, search_type, source, access_token, subway_token):
        page_no = 1
        effect_list = []
        while True:  
            subeffect_list = SimbaRptCampadgroupEffectGet._get_rpt_adgroupeffect_list(\
                    nick, campaign_id, start_time, end_time, search_type,\
                    source, access_token, subway_token, page_no)

            effect_list.extend(subeffect_list)
            if len(subeffect_list) < 500:
                break
            page_no += 1

        return effect_list


if __name__ == '__main__':
    try_list = SimbaRptCampadgroupEffectGet.get_rpt_adgroupeffect_list('chinchinstyle', \
                                                                    3367690, \
                                                                    datetime.date(2012,8,30), \
                                                                    datetime.date(2012,10,31), \
                                                                   'SUMMARY', \
                                                                   'SUMMARY', \
                                                '6201d07d3bfa761ZZ984821000e15d6f4c1d3010d1ab4a8520500325',\
                                                '1103075437-19809948-1351694757632-efb462ed')
    for item in try_list:
        print item
        
