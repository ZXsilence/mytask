#encoding=utf8
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
    sys.path.append(os.path.join(os.path.dirname(__file__),'../../backends/'))
    from adgroup_db.db_models.adgroups import Adgroups

from TaobaoSdk import SimbaRptTargetingtagbaseGetRequest 
from TaobaoSdk.Exceptions import  ErrorResponseException
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num

logger = logging.getLogger(__name__)

class SimbaRptTargetingtagbaseGet(object):

    @classmethod
    @tao_api_exception()
    def get_rpt_adgroupnonsearchbase_list(cls, nick, campaign_id, adgroup_id, start_time, end_time):
        """
        """

        req = SimbaRptTargetingtagbaseGetRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        req.campaign_id = campaign_id
        req.start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d')
        req.end_time = datetime.datetime.strftime(end_time, '%Y-%m-%d')
        req.page_no = 1
        req.page_size = 500
        base_list = []
        while True:  
            soft_code = None
            rsp = ApiService.execute(req,nick,soft_code)
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
            response = json.loads(rsp.responseBody.lower())
            l = response['simba_rpt_targetingtagbase_get_response']['results']['rpt_base_entity_d_t_o']
            if l == {}:
                l = []
            for rpt in l:
                rpt['thedate'] = datetime.datetime.strptime(rpt['thedate'], '%Y-%m-%d')
            base_list.extend(l)
            if len(l) < 500:
                break
            req.page_no += 1
        """rpt_adgroup_base_list main columns
        cost: the adgroup's cost amount
        impressions: the adgroup's impression amount
        click: the adgroup's click amount
        searchtype: the report's type in {SEARCH, CAT, NOSEARCH}
        source: the data source in {1,2}
        date: the report date
        """
        return change2num(change_obj_to_dict_deeply(base_list))
    
if __name__ == '__main__':
    nick = 'nowxh'
    campaign_id = 46231373 
    adgroup_id = 744571445 
    start_time = datetime.datetime.now() - datetime.timedelta(days=2)
    end_time = datetime.datetime.now() - datetime.timedelta(days=2)
    rpt_list = SimbaRptTargetingtagbaseGet.get_rpt_adgroupnonsearchbase_list(nick, campaign_id, adgroup_id, start_time, end_time)
    for rpt in rpt_list:
        print '%(crowdid)s,%(source)s,%(crowdname)s,%(impression)s,%(click)s,%(cost)s'% rpt
        
