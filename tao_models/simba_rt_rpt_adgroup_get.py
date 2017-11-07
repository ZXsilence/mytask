#! /usr/bin/env python
# -*- coding: utf-8 -*-
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

from TaobaoSdk import SimbaRtrptAdgroupGetRequest 
from tao_models.common.decorator import  tao_api_exception, rt_check_retry
from api_server.services.api_service import ApiService
from api_server.conf.settings import API_VIRTUAL_TEST
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num, KEYS_INT, KEYS_FLOAT, KEYS_RT

logger = logging.getLogger(__name__)

class SimbaRtRptAdgroupGet(object):
    
    #保留分平台数据
    @classmethod 
    def get_adgroup_platform_rt_rpt_list(cls, nick, campaign_id, the_date):

        adgroups_rpt_list = cls.get_adgroup_rt_detail_rpt_list(nick, campaign_id, the_date, "SUMMARY")
        
        adgroups_rpt_dict_pc = {} 
        adgroups_rpt_dict_wx = {}
        adgroups_rpt_dict = {}
        
        for adgroup_rpt in adgroups_rpt_list:
            adgroup_id = adgroup_rpt['adgroup_id']
            source_id = int(adgroup_rpt['source'])
            if not adgroups_rpt_dict.has_key(adgroup_id):
                adgroups_rpt_dict[adgroup_id] = {}
                for key in adgroup_rpt.keys():
                    adgroups_rpt_dict[adgroup_id][key] = adgroup_rpt[key]
            else:
                sum_adgroup_rpt = adgroups_rpt_dict[adgroup_id]
                for key in adgroup_rpt:
                    if key not in KEYS_INT and key not in KEYS_FLOAT:
                        continue
                    if not sum_adgroup_rpt.has_key(key):
                        sum_adgroup_rpt[key] = adgroup_rpt[key]
                    else:
                        sum_adgroup_rpt[key] += adgroup_rpt[key]
            if source_id == 1 or source_id == 2:
                if not adgroups_rpt_dict_pc.has_key(adgroup_id):
                    adgroups_rpt_dict_pc[adgroup_id] = adgroup_rpt
                else:
                    sum_adgroup_rpt = adgroups_rpt_dict_pc[adgroup_id]
                    for key in adgroup_rpt:
                        if key not in KEYS_INT and key not in KEYS_FLOAT:
                            continue
                        if not sum_adgroup_rpt.has_key(key):
                            sum_adgroup_rpt[key] = adgroup_rpt[key]
                        else:
                            sum_adgroup_rpt[key] += adgroup_rpt[key]
            else:
                if not adgroups_rpt_dict_wx.has_key(adgroup_id):
                    adgroups_rpt_dict_wx[adgroup_id] = adgroup_rpt
                else:
                    sum_adgroup_rpt = adgroups_rpt_dict_wx[adgroup_id]
                    for key in adgroup_rpt:
                        if key not in KEYS_INT and key not in KEYS_FLOAT: 
                             continue
                        if not sum_adgroup_rpt.has_key(key):
                            sum_adgroup_rpt[key] = adgroup_rpt[key]
                        else:
                            sum_adgroup_rpt[key] += adgroup_rpt[key]

        for adgroup_rpt in adgroups_rpt_dict.values():
            adgroup_rpt['cpc'] = 0 if adgroup_rpt['click'] <= 0 else\
                adgroup_rpt['cost'] / adgroup_rpt['click']
            adgroup_rpt['ctr'] = 0 if adgroup_rpt['impressions'] <= 0 else\
                100.0*adgroup_rpt['click'] / adgroup_rpt['impressions']
            adgroup_rpt['coverage'] = 0 if adgroup_rpt['click'] <= 0 else \
                100.0*(adgroup_rpt['directtransactionshipping'] + \
                       adgroup_rpt['indirecttransactionshipping']) / adgroup_rpt['click']
            adgroup_rpt['cpm'] = 0 if adgroup_rpt['impressions'] <= 0 else\
                1000.0*adgroup_rpt['cost'] / adgroup_rpt['impressions']
            adgroup_rpt['roi'] = 0 if adgroup_rpt['cost'] <= 0 else\
                (adgroup_rpt['directtransaction'] + adgroup_rpt['indirecttransaction']) \
                / float(adgroup_rpt['cost'])
        
        for adgroup_rpt in adgroups_rpt_dict_pc.values():
            adgroup_rpt['cpc'] = 0 if adgroup_rpt['click'] <= 0 else\
                adgroup_rpt['cost'] / adgroup_rpt['click']
            adgroup_rpt['ctr'] = 0 if adgroup_rpt['impressions'] <= 0 else\
                100.0*adgroup_rpt['click'] / adgroup_rpt['impressions']
            adgroup_rpt['coverage'] = 0 if adgroup_rpt['click'] <= 0 else \
                100.0*(adgroup_rpt['directtransactionshipping'] + \
                     adgroup_rpt['indirecttransactionshipping']) / adgroup_rpt['click']
            adgroup_rpt['cpm'] = 0 if adgroup_rpt['impressions'] <= 0 else\
                1000.0*adgroup_rpt['cost'] / adgroup_rpt['impressions']
            adgroup_rpt['roi'] = 0 if adgroup_rpt['cost'] <= 0 else\
                (adgroup_rpt['directtransaction'] + adgroup_rpt['indirecttransaction']) \
                / float(adgroup_rpt['cost'])
            adgroup_rpt['source'] = 'pc'

        for adgroup_rpt in adgroups_rpt_dict_wx.values():
            adgroup_rpt['cpc'] = 0 if adgroup_rpt['click'] <= 0 else\
                adgroup_rpt['cost'] / adgroup_rpt['click']
            adgroup_rpt['ctr'] = 0 if adgroup_rpt['impressions'] <= 0 else\
                100.0*adgroup_rpt['click'] / adgroup_rpt['impressions']
            adgroup_rpt['coverage'] = 0 if adgroup_rpt['click'] <= 0 else \
                100.0*(adgroup_rpt['directtransactionshipping'] + \
                     adgroup_rpt['indirecttransactionshipping']) / adgroup_rpt['click']
            adgroup_rpt['cpm'] = 0 if adgroup_rpt['impressions'] <= 0 else\
                1000.0*adgroup_rpt['cost'] / adgroup_rpt['impressions']
            adgroup_rpt['roi'] = 0 if adgroup_rpt['cost'] <= 0 else\
                (adgroup_rpt['directtransaction'] + adgroup_rpt['indirecttransaction']) \
                / float(adgroup_rpt['cost'])
            adgroup_rpt['source'] = 'wx'
        return adgroups_rpt_dict.values(), adgroups_rpt_dict_pc.values(), adgroups_rpt_dict_wx.values()

    @classmethod
    def get_adgroup_rt_rpt_list(cls, nick, campaign_id, the_date,source="SUMMARY"):
        """
        获取推广组实时报表
        """
        adgroups_rpt_list = cls.get_adgroup_rt_detail_rpt_list(nick, campaign_id, the_date,source)
        adgroups_rpt_dict = {}
        for adgroup_rpt in adgroups_rpt_list:
            adgroup_id = adgroup_rpt['adgroup_id']
            if not adgroups_rpt_dict.has_key(adgroup_id):
                adgroups_rpt_dict[adgroup_id] = adgroup_rpt
            else:
                sum_adgroup_rpt = adgroups_rpt_dict[adgroup_id]
                for key in adgroup_rpt:
                    if key not in KEYS_INT and key not in KEYS_FLOAT:
                        continue
                    if not sum_adgroup_rpt.has_key(key):
                        sum_adgroup_rpt[key] = adgroup_rpt[key]
                    else:
                        sum_adgroup_rpt[key] += adgroup_rpt[key]
        
        for adgroup_rpt in adgroups_rpt_dict.values():
            adgroup_rpt['cpc'] = 0 if adgroup_rpt['click'] <= 0 else\
                adgroup_rpt['cost'] / adgroup_rpt['click']
            adgroup_rpt['ctr'] = 0 if adgroup_rpt['impressions'] <= 0 else\
                100.0*adgroup_rpt['click'] / adgroup_rpt['impressions']
            adgroup_rpt['coverage'] = 0 if adgroup_rpt['click'] <= 0 else \
                100.0*(adgroup_rpt['directtransactionshipping'] + \
                     adgroup_rpt['indirecttransactionshipping']) / adgroup_rpt['click']
            adgroup_rpt['cpm'] = 0 if adgroup_rpt['impressions'] <= 0 else\
                1000.0*adgroup_rpt['cost'] / adgroup_rpt['impressions']
            adgroup_rpt['roi'] = 0 if adgroup_rpt['cost'] <= 0 else\
                (adgroup_rpt['directtransaction'] + adgroup_rpt['indirecttransaction']) \
                / float(adgroup_rpt['cost'])

        adgroups_rpt_list = adgroups_rpt_dict.values()
        return adgroups_rpt_list
    
    @classmethod
    @rt_check_retry()
    @tao_api_exception()
    def get_adgroup_rt_detail_rpt_list(cls, nick, campaign_id, the_date,source="SUMMARY"):
        """
        获取推广组实时报表,分来源和类型
        """
        req = SimbaRtrptAdgroupGetRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.the_date = datetime.datetime.strftime(the_date, '%Y-%m-%d')
        req.page_size = 500
        req.page_number = 1
        rpt_list = []

        while True:  
            soft_code = None
            rsp = ApiService.execute(req,nick,soft_code)
            l = rsp.results
            if not l:
                l = []
            rpt_list.extend(l)
            if len(l) < 500:
                break
            if API_VIRTUAL_TEST and nick in ("chinchinstyle","麦苗科技001"):
                break
            req.page_number += 1

        adgroups_rpt_list = change2num(change_obj_to_dict_deeply(rpt_list))
        for adgroup_rpt in adgroups_rpt_list:
            for key in KEYS_RT:
                if not adgroup_rpt.has_key(key):
                    adgroup_rpt[key] = 0
            adgroup_rpt['campaign_id'] = int(adgroup_rpt['campaignid'])
            adgroup_rpt['adgroup_id'] = int(adgroup_rpt['adgroupid'])
            adgroup_rpt['impressions'] = adgroup_rpt.get('impression',0)
            adgroup_rpt['cvr'] = adgroup_rpt.get('coverage',0)
        adgroups_rpt_dict = {}
        for adgroup_rpt  in adgroups_rpt_list:
            if not adgroups_rpt_dict.has_key(adgroup_rpt['source']):
                adgroups_rpt_dict[adgroup_rpt['source']] = [adgroup_rpt]
            else:
                adgroups_rpt_dict[adgroup_rpt['source']].append(adgroup_rpt) 
        if source=="SUMMARY":
            return adgroups_rpt_list
        else:
            return adgroups_rpt_dict.get(source,[])
        return adgroups_rpt_list


if __name__ == '__main__':
    nick = sys.argv[1]
    campaign_id = int(sys.argv[2])
    adgroup_id = int(sys.argv[3])
    the_date = datetime.datetime.now()
    rpt_list = SimbaRtRptAdgroupGet.get_adgroup_platform_rt_rpt_list(nick, campaign_id, the_date)
    print "results"
    for rpt in rpt_list:
        print rpt
        #if rpt['adgroup_id'] == adgroup_id:
        #    print rpt

