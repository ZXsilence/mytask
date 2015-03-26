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

def change2num(rpt_list):
    keys_int  =["click","impressions","directpaycount","indirectpaycount","favitemcount","favshopcount"]
    keys_float = ["cpm","avgpos","ctr","cost","directpay","indirectpay"]
    if not rpt_list:
        return rpt_list
    for item in  rpt_list:
        for key in item.keys():
            #处理None
            if not item[key]:
                item[key] = 0
            if key in keys_int:
                item[key] = int(float(item[key]))
            elif key in keys_float:
                item[key] = float(item[key])
    return rpt_list
