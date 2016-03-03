#! /usr/bin/env python
# -*- coding: utf-8 -*-
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

from TaobaoSdk import SimbaRptAdgroupcreativebaseGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.num_tools import change2num

logger = logging.getLogger(__name__)

class SimbaRptAdgroupcreativeBaseGet(object):

    @classmethod
    @tao_api_exception(10)
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
            if type(l) == type({}) and 'sub_code' in l:
                if '开始日期不能大于结束日期' == l['sub_msg'] and start_time.date() <= end_time.date():
                    l['sub_code'] = '1515'
                raise ErrorResponseException(sub_code = l['sub_code'],sub_msg = l['sub_msg'],code = l['code'],msg = l['msg'])
            if l == {}:
                l = []
            for rpt in l:
                rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')
            base_list.extend(l)
            if len(l) < 500:
                break
            req.page_no += 1
        return change2num(change_obj_to_dict_deeply(base_list))
    
        
if __name__ == '__main__':

    nick = '御森旗舰店'
    campaign_id = 18819261 
    adgroup_id = 448284862
    #nick = '牙齿天天晒'
    #campaign_id = 6965418 
    #adgroup_id = 441729311 
    nick = 'chinchinstyle'
    campaign_id = 3328400
    adgroup_id = 458765944
    search_type = 'SEARCH,NOSEARCH,CAT'
    source = 'SUMMARY'
    start_time = datetime.datetime.now() - datetime.timedelta(days=1)
    end_time = datetime.datetime.now() - datetime.timedelta(days=1)
    try_list = SimbaRptAdgroupcreativeBaseGet.get_rpt_adgroupcreativebase_list(nick, campaign_id, adgroup_id, start_time, end_time, search_type, source)
    for obj in try_list:
        print obj
        
