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
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12651461', '80a15051c411f9ca52d664ebde46a9da')

from TaobaoSdk import SimbaRptAdgroupcreativebaseGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception
from tao_models.common.exceptions import  TBDataNotReadyException

logger = logging.getLogger(__name__)

class SimbaRptAdgroupcreativeBaseGet(object):
    """
    """
    @classmethod
    @tao_api_exception(40)
    def get_rpt_adgroupcreativebase_list(cls, nick, campaign_id, adgroup_id, start_time, end_time, search_type, source, access_token, subway_token):
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
        req.subway_token = subway_token
        req.page_no = 1
        req.page_size = 500
        base_list = []
        
        while True:  
            rsp = taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
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
        return base_list
    
        
if __name__ == '__main__':

    nick = 'chinchinstyle'
    campaign_id = 3442512 
    adgroup_id = 163715837
    start_time = datetime.datetime(2013,2,20)
    end_time = datetime.datetime(2013,2,21)
    search_type = 'SUMMARY'
    source = 'SUMMARY'
    access_token = '6200e168f708b8167250268dfhe2555e99ed247caa1cdeb520500325'
    subway_token =  '1103075437-19809948-1357723903348-1238f9d4'
    try_list = SimbaRptAdgroupcreativeBaseGet.get_rpt_adgroupcreativebase_list(nick, campaign_id, adgroup_id, start_time, end_time, search_type, source, access_token, subway_token)
    print try_list
        
        
        
        
        
