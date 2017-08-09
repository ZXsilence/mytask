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
    API_INPUT_REPLACE_KEY = {
        "taobao.simba.keywordsbyadgroupid.get":"adgroup_id",
        "taobao.simba.keywords.pricevon.set":"keywordid_prices"
    }
    API_OUTPUT_REPLACE_KEY = {
        "taobao.simba.keywordsbyadgroupid.get":"keywords",
        "taobao.simba.keywords.pricevon.set":"keywords",
    }


