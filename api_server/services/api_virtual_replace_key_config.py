#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-08-07 15:06
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
class ApiVirtualReplaceKeyConfig(object):
    #
    # 注释 写api只保留读api配置，可以让用户数据先同步
    #
    API_INPUT_REPLACE_KEY = {
        #读api
        #"taobao.simba.keywordsbyadgroupid.get":"adgroup_id",
        #"taobao.simba.keywordsbykeywordids.get":"keyword_ids",
        #"taobao.simba.keywords.changed.get":"start_time",
        #"taobao.simba.keywordids.deleted.get":"start_time",

        #实时报表配置
        "taobao.simba.rtrpt.cust.get":"the_date",
        "taobao.simba.rtrpt.campaign.get":"the_date",
        "taobao.simba.rtrpt.adgroup.get":"the_date",
        "taobao.simba.rtrpt.bidword.get":"the_date",
        #写api
        #"taobao.simba.keywords.pricevon.set":"keywordid_prices",
        #"taobao.simba.keywordsvon.add":"keyword_prices",
        #"taobao.simba.keywords.delete":"keyword_ids",
    }
    API_OUTPUT_REPLACE_KEY = {
        #读api
        #"taobao.simba.keywordsbyadgroupid.get":"keywords",
        #"taobao.simba.keywordsbykeywordids.get":"keywords",
        #"taobao.simba.keywords.changed.get":"keywords",
        #"taobao.simba.keywordids.deleted.get":"deleted_keyword_ids",

        #实时报表配置
        "taobao.simba.rtrpt.cust.get":"results",
        "taobao.simba.rtrpt.campaign.get":"resultss",
        "taobao.simba.rtrpt.adgroup.get":"results",
        "taobao.simba.rtrpt.bidword.get":"results",
        #写api
        #"taobao.simba.keywords.pricevon.set":"keywords",
        #"taobao.simba.keywordsvon.add":"keywords",
        #"taobao.simba.keywords.delete":"keywords",
    }


