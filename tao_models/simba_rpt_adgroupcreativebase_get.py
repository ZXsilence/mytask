'''
Created on 2012-8-10

@author: dk
'''
#encoding=utf8
import sys
import os
import logging
import logging.config
import json
import datetime
from copy import deepcopy


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import SimbaRptAdgroupcreativebaseGetRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaRptAdgroupcreativeBaseGet(object):

    @classmethod
    @tao_api_exception(40)
    def get_rpt_adgroupcreativebase_list(cls, nick, campaign_id, adgroup_id, start_time, end_time, search_type, source):
        """
        Notes:
                because of taobao API access-times limit,so we recommend that (end_time - start_time) do not more than a day
        """
        req = SimbaRptAdgroupcreativebaseGetRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        req.campaign_id = campaign_id
        req.start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d')
        req.end_time = datetime.datetime.strftime(end_time, '%Y-%m-%d')
        req.search_type = search_type
        req.source = source
        req.page_no = 1
        req.page_size = 500
        base_list = []
        
        while True:  
            soft_code = None
            rsp = ApiService.execute(req,nick,soft_code)
            l = json.loads(rsp.rpt_adgroupcreative_base_list.lower())
            if l == {}:
                l = []
            if isinstance(l, dict):
                raise ErrorResponseException(code=l['code'], msg=l['msg'], sub_code=l['sub_code'], sub_msg=l['sub_msg'])
            for rpt in l:
                rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')
            base_list.extend(l)
            if len(l) < 500:
                break
            req.page_no += 1
        return change_obj_to_dict_deeply(base_list)
    
        
if __name__ == '__main__':

    nick = 'chinchinstyle'
    campaign_id = 3367748
    adgroup_id = 336844923
    search_type = 'SUMMARY'
    source = 'SUMMARY'
    start_time = datetime.datetime.now() - datetime.timedelta(days=10)
    end_time = datetime.datetime.now() - datetime.timedelta(days=1)
    try_list = SimbaRptAdgroupcreativeBaseGet.get_rpt_adgroupcreativebase_list(nick, campaign_id, adgroup_id, start_time, end_time, search_type, source)
    print try_list
        
