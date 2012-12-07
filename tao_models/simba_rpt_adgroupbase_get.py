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
    from xuanciw.settings import  trigger_envReady
    logging.config.fileConfig('../xuanciw/consolelogger.conf')

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    logging.config.fileConfig('conf/consolelogger.conf')

from TaobaoSdk import SimbaRptAdgroupbaseGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception
from tao_models.common.exceptions import  TBDataNotReadyException

logger = logging.getLogger(__name__)

class SimbaRptAdgroupBaseGet(object):
    """
    """
    @classmethod
    @tao_api_exception()
    def get_rpt_adgroupbase_list(cls, nick, campaign_id, adgroup_id, start_time, end_time, search_type, source, access_token, subway_token):
        """
        Notes:
                because of taobao API access-times limit,so we recommend that (end_time - start_time) do not more than a day
        """
        req = SimbaRptAdgroupbaseGetRequest()
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
            l = json.loads(rsp.rpt_adgroup_base_list)

            if not isinstance(l, list) and  l.has_key('code') and l['code'] == 15:
                raise TBDataNotReadyException(rsp.rpt_adgroup_base_list)

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
        return base_list
    
    @classmethod
    @tao_api_exception()
    def get_yesterday_rpt_adgroupbase_list(cls, campaign_id, adgroup_id, search_type, source, access_token, subway_token):
        'get yesterday adgroup base rpt list'
        yes = datetime.date.today() - datetime.timedelta(days=1)
        base_list = cls.get_rpt_adgroupbase_list(campaign_id, adgroup_id, str(yes), str(yes), search_type, source, access_token, subway_token)
        return base_list
        
if __name__ == '__main__':
    try_list = SimbaRptAdgroupBaseGet.get_yesterday_rpt_adgroupbase_list(7266464, 122016166, 'SEARCH,CAT', '1,2', '6200b26ad6dde0735bc63c45618ca4f8bdfhfc1dfd08854100160612', '1104314334-31146703-1343962127197-c876e57d')
    print try_list
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        