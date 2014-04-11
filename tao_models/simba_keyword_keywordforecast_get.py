# -*- coding: utf-8 -*-
'''
Created on 2012-11-21

@author: dk
'''
import sys
import os
import datetime
import logging
import logging.config
import json
from time import sleep
from tao_models.common.exceptions import  TaoApiMaxRetryException 
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    #logging.config.fileConfig('conf/consolelogger.conf')
    
from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception
from TaobaoSdk.Request.SimbaKeywordKeywordforecastGetRequest import SimbaKeywordKeywordforecastGetRequest
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaKeywordKeywordforecastGet(object):
    ''
    @classmethod
    @tao_api_exception()
    def get_keywordforecast(cls,keyword_id,bidword_price,nick=None):
        """词预估"""
        req = SimbaKeywordKeywordforecastGetRequest()
        req.keyword_id = keyword_id
        req.bidword_price = bidword_price
        if nick:
            req.nick= nick
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.keyword_forecast)

    @classmethod
    def get_keywordforecast_by_price_range(cls,keyword_id,min_price,max_price,nick=None):
        """价格段内的排名分布"""
        num = 0
        max_num = 20
        rank_dict ={}
        bid_price = min_price
        while True:
            num += 1
            temp_rank_dict = cls._get_keywordforecast(keyword_id,bid_price,nick)
            if not temp_rank_dict.keys():
                raise TaoApiMaxRetryException("api error")
            rank_dict.update(temp_rank_dict)
            if max(temp_rank_dict.keys()) >= max_price:
                logger.debug("经过num:%s次排名预估找到价格区间预估min_price:%s,max_price:%s,nick:%s,keyword_id:%s" %(num,min_price,max_price,nick,keyword_id))
                break
            if not temp_rank_dict:
                logger.debug("未获取到排名预估nick:%s,min_price:%s,max_price:%s,keyword_id:%s" %(nick,min_price,max_price,keyword_id)) 
                break
            if num >max_num:
                logger.debug("获取到排名预估nick:%s,min_price:%s,max_price:%s,keyword_id:%s,已经达到max_num:%s 退出" %(nick,min_price,max_price,keyword_id,max_num))
                break
            #当前出价比最大出价还低
            if max(temp_rank_dict.keys()) < max_price:
                bid_price = max(temp_rank_dict.keys()) 
        return rank_dict


    @classmethod
    def _get_keywordforecast(cls,keyword_id,price,nick=None):
        """获取价格排名分布"""
        i = 0
        while(True):
            if i == 20:
                raise TaoApiMaxRetryException("retry 20 times ,but still failed")
            data_dict = SimbaKeywordKeywordforecastGet.get_keywordforecast(keyword_id,price,nick)
            if not data_dict or not data_dict.has_key('price_rank') or not data_dict['price_rank']:
                i += 1
                sleep(1)
                print 'retry get keywordforecast',i
                continue
            else:
                break
        cost_dict = {}
        click_dict = {}
        if data_dict and data_dict.get("price_click"):
            l = data_dict["price_click"].split(",")
            for obj in l:
                a_list = obj.split(":")
                click_dict[int(a_list[0])] = int(a_list[1])
        if data_dict and data_dict.get("price_cust"):
            l = data_dict["price_cust"].split(",")
            for obj in l:
                a_list = obj.split(":")
                cost_dict[int(a_list[0])] = int(a_list[1])
        ret_dict ={}
        if data_dict and data_dict.get("price_rank"):
            l = data_dict["price_rank"].split(",")
            for obj in l:
                a_list = obj.split(":")
                key = int(a_list[0])
                if not ret_dict.has_key(int(a_list[0])):
                    ret_dict[key] = {}
                ret_dict[key]['rank'] = int(a_list[1])
                ret_dict[key]['click'] = click_dict[key/10*10]
                ret_dict[key]['cost'] = cost_dict[key/10*10]
        return ret_dict

if __name__ =="__main__":
    tao_model_settings.set_taobao_client('21065688','74aecdce10af604343e942a324641891')
    keyword_id = 54849998072
    price = 230 
    access_token = "62018175fd80b11fb03e28afdfh7feb0d829efc228b5a93871727117"
    keyword_id = 55108934651
    #keyword_id = 53203700147
    price = 270
    #access_token = "620200488562ZZ4711a5a8f32852f2b81bfcc1954015c7e816221524"
    #nick ="康诺宜家家居旗舰店"
    nick = "栾氏茶业"
    rsp = SimbaKeywordKeywordforecastGet.get_keywordforecast(keyword_id,price,nick)
    for key ,v in rsp.iteritems():
        print key,v
    #print SimbaKeywordKeywordforecastGet.get_keywordforecast_by_price_range(keyword_id,10,300,access_token,nick)
