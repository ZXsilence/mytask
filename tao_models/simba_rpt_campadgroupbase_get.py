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

from TaobaoSdk import SimbaRptCampadgroupbaseGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaRptCampadgroupBaseGet(object):

    @classmethod
    @tao_api_exception(10)
    def _get_rpt_adgroupbase_list(cls, nick, campaign_id, start_time, end_time, search_type, source, page_no):
        req = SimbaRptCampadgroupbaseGetRequest()
        req.campaign_id = campaign_id
        req.nick = nick
        req.start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d')
        req.end_time = datetime.datetime.strftime(end_time, '%Y-%m-%d')
        req.search_type = search_type
        req.source = source
        req.page_no = page_no
        req.page_size = 500
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        logger.debug('nick:[%s] campaign_id [%d], get adgroup base', nick, int(campaign_id))
        l = json.loads(rsp.rpt_campadgroup_base_list.lower())
        if l == {}:
            l = []
        for rpt in l:
            rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')
        return l

    @classmethod
    def get_rpt_adgroupbase_list(cls, nick, campaign_id, start_time, end_time, search_type, source):
        page_no = 1
        base_list = []
        keys_int  =["click","impressions"]
        keys_float = ["cpm","avgpos","ctr","cost"]
        while True:  
            subbase_list = SimbaRptCampadgroupBaseGet._get_rpt_adgroupbase_list(\
                    nick, campaign_id, start_time, end_time, search_type,\
                    source,page_no)
            base_list.extend(subbase_list)
            if len(subbase_list) < 500:
                break
            page_no += 1
        rpt_list  = change_obj_to_dict_deeply(base_list)
        for item in  rpt_list:
            for key in item.keys():
                if key in keys_int:
                    item[key] = int(item[key])
                elif key in keys_float:
                    item[key] = float(item[key])
        return rpt_list

if __name__ == '__main__':
    nick = 'zhangyu_xql'
    campaign_id = 6765909
    adgroup_id =368440092 
    search_type = 'SEARCH,CAT'
    source = '1,2'
    start_time = datetime.datetime.now() - datetime.timedelta(days=10)
    end_time = datetime.datetime.now() - datetime.timedelta(days=1)
    print SimbaRptCampadgroupBaseGet.get_rpt_adgroupbase_list(nick, campaign_id, start_time, end_time, search_type, source)

