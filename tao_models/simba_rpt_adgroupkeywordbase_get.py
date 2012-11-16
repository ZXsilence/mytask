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

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    logging.config.fileConfig('conf/consolelogger.conf')

from TaobaoSdk import SimbaRptAdgroupkeywordbaseGetRequest
from TaobaoSdk.Request.SimbaRptAdgroupkeywordbaseGetRequest import SimbaRptAdgroupkeywordbaseGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception
from tao_modesl.common.exceptions import  TBDataNotReadyException

logger = logging.getLogger(__name__)

class SimbaRptAdgroupkeywordbaseGet(object):
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
    @tao_api_exception
    def get_rpt_adgroupkeywordbase_list(cls, nick, campaingn_id, adgroup_id, start_time, end_time, source, search_type, access_token, subway_token):
        
        req = SimbaRptAdgroupkeywordbaseGetRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        req.campaign_id = campaingn_id
        req.start_time = DateHandle.date_to_ustring(start_time)
        req.end_time = DateHandle.date_to_ustring(end_time)
        req.search_type = search_type
        req.source = source
        req.subway_token = subway_token
        req.page_no = 1
        req.page_size = 500
        base_list = []

        logger.debug("start get_rpt_adgroupkeywordbase_list, adgroup_id:%s"%(adgroup_id))

        while True:
#            fd = open('count','r')
#            a = int(fd.readline())
#            fd.close()
#            a += 1
#            fd = open('count','w')
#            fd.write(str(a))
#            fd.close
            
            rsp = taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
            l = json.loads(rsp.rpt_adgroupkeyword_base_list)

            if not isinstance(l, list) and  l.has_key('code') and l['code'] == 15:
                raise TBDataNotReadyException(rsp.rpt_adgroupkeyword_base_list)

            base_list.extend(l)
            if len(l) < 500:
                break
            req.page_no += 1


        logger.debug("get_rpt_adgroupkeywordbase_list, adgroup_id:%s"%(adgroup_id))
        return base_list
            
            
        
if __name__ == '__main__':
    #搜索：SEARCH,类目出价：CAT, 定向投放：NOSEARCH
    try_list = SimbaRptAdgroupkeywordbaseGet.get_rpt_adgroupkeywordbase_list(3208321, \
                                                                                        99196734, \
                                                                             datetime.date(2012,8,21), \
                                                                             datetime.date(2012,8,21), \
                                                                             'SUMMARY', \
                                                                             'SEARCH,CAT,NOSEARCH', \
                                                                             '6200602c34ZZ144de0952fb59aef3051c4e1d4af0a010e7106852162', \
                                                                             '1103016634-15007742-1346597966921-d7d35029')
    for item in try_list:
        print item
        print 'word:%s searchtype:%s impressions:%s click:%s'%(item[u'keywordstr'], item[u'searchtype'], item[u'impressions'], item[u'click'])
