# -*- coding: utf-8 -*-
'''
Created on 2012-8-31

@author: dk
'''
import sys
import os
import json
import datetime
import logging
from copy import deepcopy

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaRptAdgroupkeywordeffectGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class SimbaRptAdgroupkeywordeffectGet(object):
    """
    campaign_id    Number    必须    110694874         推广计划ID
    adgroup_id    Number    必须    1106475122         推广组ID
    start_time    String    必须    2000-01-01 00:00:00         开始时间
    end_time    String    必须    2000-01-01 00:00:00         结束时间
    source    String    必须    1,2    1,2     数据来源（站内：1，站外：2 ，汇总：SUMMARY）SUMMARY必须单选，其他值可多选例如1,2
    subway_token    String    必须    1102001000-101102001000-1318045030614-ed7cf93b         权限校验参数
    page_no    Number    可选    1    1     页码
    page_size    Number    可选    500    500     每页大小
    search_type    String    必须    SEARCH         报表类型（搜索：SEARCH,类目出价：CAT, 定向投放：NOSEARCH）可多选例如：SEARCH,CAT
    """
    @classmethod
    def get_rpt_adgroupkeywordeffect_list(cls, nick, campaign_id, adgroup_id, start_time, end_time, source, search_type):
        rpt_list = []
        date_list = split_date(start_time,end_time)
        for item in date_list:
            rpt_list.extend(cls._get_rpt_adgroupkeywordeffect_list(nick, campaign_id, adgroup_id,item[0],item[1],source,search_type))
        return rpt_list

    @classmethod
    def _get_rpt_adgroupkeywordeffect_list(cls, nick, campaign_id, adgroup_id, start_time, end_time, source, search_type):
        req = SimbaRptAdgroupkeywordeffectGetRequest()
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
        logger.info("start get_rpt_adgroupkeywordeffect_list, adgroup_id:%s, sdate:%s, edate:%s"%(adgroup_id, start_time, end_time))
        while True:
            l = cls._sub_get_rpt_adgroupkeywordeffect_list(req,nick)
            effect_list.extend(l)
            if len(l) < 500:
                break
            req.page_no += 1
        logger.info("get_rpt_adgroupkeywordeffect_list, adgroup_id:%s, sdate:%s, edate:%s"%(adgroup_id, start_time, end_time))
        return change2num(change_obj_to_dict_deeply(effect_list))

    @classmethod 
    @tao_api_exception()
    def _sub_get_rpt_adgroupkeywordeffect_list(cls,req,nick,soft_code=None):
        rsp = ApiService.execute(req,nick,soft_code)
        l = json.loads(rsp.rpt_adgroupkeyword_effect_list.lower())
        test_sdate = datetime.datetime.strptime(req.start_time,'%Y-%m-%d')
        test_edate = datetime.datetime.strptime(req.end_time,'%Y-%m-%d')   
        if type(l) == type({}) and 'sub_code' in l:
            if '开始日期不能大于结束日期' == l['sub_msg'] and datetime.datetime.strptime(req.start_time,'%Y-%m-%d') <= datetime.datetime.strptime(req.end_time,'%Y-%m-%d'):
                l['sub_code'] = '1515'
            raise ErrorResponseException(sub_code = l['sub_code'],sub_msg = l['sub_msg'],code = l['code'],msg = l['msg'], sdate = test_sdate, edate = test_edate)
        if l == {}:
            l = []
        for rpt in l:
            rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')
        return l

if __name__ == '__main__':
    nick = '美妃服饰旗舰店'
    campaign_id = 6175323
    adgroup_id = 707780421 
    search_type = 'SEARCH,CAT'
    source = '1,2,4,5'
    #start_time = datetime.datetime.now() - datetime.timedelta(days=10)
    #end_time = datetime.datetime.now() - datetime.timedelta(days=1)
    start_data = datetime.datetime.combine(datetime.date.today(), datetime.time()) - datetime.timedelta(days=8)  
    end_data = datetime.datetime.combine(datetime.date.today(), datetime.time()) - datetime.timedelta(days=1)
    start_time = datetime.datetime.combine(start_data, datetime.time())
    end_time = datetime.datetime.combine(end_data, datetime.time())
    res = SimbaRptAdgroupkeywordeffectGet.get_rpt_adgroupkeywordeffect_list(nick, campaign_id, adgroup_id, start_time, end_time, source, search_type)
    print len(res)

