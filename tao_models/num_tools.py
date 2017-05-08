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

KEYS_INT_YZB = ['campaign_id','adgroup_id','creative_id','adzone_id','target_id','ad_pv','click','uv','deep_inshop_uv','avg_access_page_num',\
                'inshop_item_col_num','dir_shop_col_num','cart_num','gmv_inshop_num','alipay_in_shop_num']
KEYS_FLOAT_YZB = ['charge','ctr','ecpc','ecpm','avg_access_time','gmv_inshop_amt','alipay_inshop_amt','cvr','roi']
MONEY_KEYS = ['charge','gmv_inshop_amt','alipay_inshop_amt','ecpc','ecpm']

from datetime import datetime

def change2num(rpt_list):
    if not rpt_list:
        return rpt_list
    for item in  rpt_list:
        for key in item.keys():
            #处理None
            if not item[key]:
                item[key] = 0
                continue
            if key in KEYS_INT:
                item[key] = int(float(item[key]))
            elif key in KEYS_FLOAT:
                item[key] = float(item[key])
        if 'log_date' in item and type(item['log_date']) != datetime:
            l = item['log_date'].strip().replace('-',' ').split(' ')
            item['log_date'] = datetime(int(l[0]), int(l[1]), int(l[2]))
    return rpt_list

def change2num2(rpt_list,change_unit = False):
    if not rpt_list:
        return rpt_list
    for item in  rpt_list:
        for key in item.keys():
            #处理None
            if not item[key]:
                item[key] = 0
                continue
            if key in KEYS_INT_YZB:
                item[key] = int(float(item[key]))
            elif key in KEYS_FLOAT_YZB:
                item[key] = float(item[key])
        if 'log_date' in item and type(item['log_date']) != datetime:
            l = item['log_date'].strip().replace('-',' ').split(' ')
            item['log_date'] = datetime(int(l[0]), int(l[1]), int(l[2]))
        if change_unit:
            for key in MONEY_KEYS:
                if key in item: 
                    item[key] *= 100
    return rpt_list
