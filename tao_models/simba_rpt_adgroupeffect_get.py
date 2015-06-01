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

logger = logging.getLogger(__name__)

class SimbaRptAdgroupEffectGet(object):

    @classmethod
    @tao_api_exception()
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
            soft_code = None
            rsp = ApiService.execute(req,nick,soft_code)
            l = json.loads(rsp.rpt_adgroup_effect_list.lower())
            if l == {}:
                l = []
            for rpt in l:
                rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')

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
    
if __name__ == '__main__':
    nick = 'chinchinstyle'
    campaign_id = 3367748
    adgroup_id = 336844923
    search_type = 'SEARCH,CAT'
    source = '1,2'
    start_time = datetime.datetime.now() - datetime.timedelta(days=10)
    end_time = datetime.datetime.now() - datetime.timedelta(days=1)
    try_list = SimbaRptAdgroupEffectGet.get_rpt_adgroupeffect_list(nick, campaign_id, adgroup_id, start_time, end_time, search_type, source)
    print try_list
