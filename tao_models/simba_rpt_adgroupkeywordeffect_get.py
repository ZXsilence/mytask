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
    @tao_api_exception(40)
    def get_rpt_adgroupkeywordeffect_list(cls, nick, campaign_id, adgroup_id, start_time, end_time, source, search_type):
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
        logger.debug("start get_rpt_adgroupkeywordeffect_list, adgroup_id:%s"%(adgroup_id))
        while True:
            soft_code = None
            rsp = ApiService.execute(req,nick,soft_code)
            l = json.loads(rsp.rpt_adgroupkeyword_effect_list.lower())
            if l == {}:
                l = []
            for rpt in l:
                rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')
            effect_list.extend(l)
            if len(l) < 500:
                break
            req.page_no += 1
        logger.debug("get_rpt_adgroupkeywordeffect_list, adgroup_id:%s"%(adgroup_id))
        return change_obj_to_dict_deeply(effect_list)
    
if __name__ == '__main__':
    nick = 'chinchinstyle'
    campaign_id = 3367748
    adgroup_id = 336844923
    search_type = 'SEARCH,CAT'
    source = '1,2'
    start_time = datetime.datetime.now() - datetime.timedelta(days=10)
    end_time = datetime.datetime.now() - datetime.timedelta(days=1)
    print SimbaRptAdgroupkeywordeffectGet.get_rpt_adgroupkeywordeffect_list(nick, campaign_id, adgroup_id, start_time, end_time, source, search_type)

