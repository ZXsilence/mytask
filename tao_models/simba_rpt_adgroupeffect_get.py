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

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaRptAdgroupeffectGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException

logger = logging.getLogger(__name__)

class SimbaRptAdgroupEffectGet(object):

    @classmethod
    def get_rpt_adgroupeffect_list(cls, nick, campaign_id, adgroup_id, start_time, end_time, search_type, source):
        """
        Notes:
                because of taobao API access-times limit,so we recommend that (end_time - start_time) do not more than a day
        """
        req = SimbaRptAdgroupeffectGetRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        req.campaign_id = campaign_id
        req.start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d')
        req.end_time = datetime.datetime.strftime(end_time, '%Y-%m-%d')
        req.search_type = search_type
        req.source = source
        req.page_no = 1
        req.page_size = 500
        effect_list = []
        while True:
            print req.page_no
            l = cls._sub_get_rpt_adgroupeffect_list(req,nick)
            effect_list.extend(l)
            if len(l) < 500:
                break
            req.page_no += 1
        """rpt_adgroup_effect_list main columns
        directpay: the adgroup's direct payment in 3 days
        indirectpay: this adgroup's indirect payment in 3 days
        searchtype: the report's type in {SEARCH, CAT, NOSEARCH}
        source: the data source in {1,2}
        date: the report date
        """
        return change2num(change_obj_to_dict_deeply(effect_list))
    
    @classmethod
    @tao_api_exception()
    def _sub_get_rpt_adgroupeffect_list(cls,req,nick,soft_code=None):
        rsp = ApiService.execute(req,nick,soft_code)
        l = json.loads(rsp.rpt_adgroup_effect_list.lower())
        if type(l) == type({}) and 'sub_code' in l:
            if '开始日期不能大于结束日期' == l['sub_msg'] and datetime.datetime.strptime(req.start_time,'%Y-%m-%d') <= datetime.datetime.strptime(req.end_time,'%Y-%m-%d'):
                l['sub_code'] = '1515'
            raise ErrorResponseException(sub_code = l['sub_code'],sub_msg = l['sub_msg'],code = l['code'],msg = l['msg'])
        if l == {}:
            l = []
        for rpt in l:
            rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')
        return l



    
if __name__ == '__main__':
    nick = '大雪1'
    campaign_id = 2617648
    adgroup_id = 645184372 
    search_type = 'SEARCH,CAT'
    source = '1,2,4,5'
    start_time = datetime.datetime.now() - datetime.timedelta(days=40)
    end_time = datetime.datetime.now() - datetime.timedelta(days=1)
    try_list = SimbaRptAdgroupEffectGet.get_rpt_adgroupeffect_list(nick, campaign_id, adgroup_id, start_time, end_time, search_type, source)
    print len(try_list)
