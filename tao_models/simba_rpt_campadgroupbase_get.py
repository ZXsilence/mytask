'''
Created on 2012-9-4

@author: dk
'''
#encoding=utf8
import sys
import os
import json
import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')

from TaobaoSdk import SimbaRptCampadgroupbaseGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception
from tao_models.common.exceptions import  TBDataNotReadyException

import logging
logger = logging.getLogger(__name__)


class SimbaRptCampadgroupBaseGet(object):
    """
    """
    @classmethod
    @tao_api_exception(10)
    def _get_rpt_adgroupbase_list(cls, nick, campaign_id, start_time, end_time, search_type, source, access_token, subway_token, page_no):
        req = SimbaRptCampadgroupbaseGetRequest()
        req.campaign_id = campaign_id
        req.nick = nick
        req.start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d')
        req.end_time = datetime.datetime.strftime(end_time, '%Y-%m-%d')
        req.search_type = search_type
        req.source = source
        req.subway_token = subway_token
        req.page_no = page_no
        req.page_size = 500
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        logger.debug('nick:[%s] campaign_id [%d], get adgroup base', nick, int(campaign_id))
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        l = json.loads(rsp.rpt_campadgroup_base_list.lower())
        if l == {}:
            l = []

        if isinstance(l, dict):
            raise ErrorResponseException(code=l['code'], msg=l['msg'], sub_code=l['sub_code'], sub_msg=l['sub_msg'])

        for rpt in l:
            rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')

        return l


    @classmethod
    def get_rpt_adgroupbase_list(cls, nick, campaign_id, start_time, end_time, search_type, source, access_token, subway_token):
        page_no = 1
        base_list = []
        while True:  
            subbase_list = SimbaRptCampadgroupBaseGet._get_rpt_adgroupbase_list(\
                    nick, campaign_id, start_time, end_time, search_type,\
                    source, access_token, subway_token, page_no)

            base_list.extend(subbase_list)
            if len(subbase_list) < 500:
                break
            page_no += 1

        return base_list


if __name__ == '__main__':
    try_list = SimbaRptCampadgroupBaseGet.get_rpt_adgroupbase_list(u'色色淑女',\
                                                                    9903616, \
                                                                    datetime.date(2013,6,26), \
                                                                    datetime.date(2013,6,26), \
                                                                   'SUMMARY', \
                                                                   '1,2', \
                                                '6201b202c4d6f7487d76a9014a8dfh1d5ba75c56ed7125a354435780',\
                                                '1102671513-15490633-1372141182065-7f41b9bb')
    print 
    for item in try_list:
        print item
