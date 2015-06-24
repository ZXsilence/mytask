#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: xieguanfu
@contact: xieguanfu@maimiaotech.com
@date: 2015-03-26 18:57
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
KEYS_INT  =["click","impression","impressions","directpaycount",\
            "indirectpaycount","favitemcount","favshopcount",\
            "transactiontotal","directtransactionshipping",\
            "indirecttransactionshipping","indirectcarttotal", \
            "transactionshippingtotal","favshoptotal","carttotal",\
            "favitemtotal","directcarttotal","favtotal"]
KEYS_FLOAT = ["cpm","avgpos","ctr","cost","directpay","indirectpay",\
                "cpc","roi","indirecttransaction","directtransaction", \
              "coverage"]
KEYS_RT = ['impression', 'roi', 'directtransactionshipping', 'cost', \
           'directtransaction', 'favshoptotal', 'impressions', 'click',\
           'transactiontotal', 'indirecttransactionshipping', 'indirecttransaction', \
           'transactionshippingtotal', 'coverage', 'directcarttotal', 'favtotal', \
           'cpm', 'ctr', 'cpc', 'indirectcarttotal', 'carttotal', 'favitemtotal']

def change2num(rpt_list):
    if not rpt_list:
        return rpt_list
    for item in  rpt_list:
        for key in item.keys():
            #处理None
            if not item[key]:
                item[key] = 0
            if key in KEYS_INT:
                item[key] = int(float(item[key]))
            elif key in KEYS_FLOAT:
                item[key] = float(item[key])
    return rpt_list
