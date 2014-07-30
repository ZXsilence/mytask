#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zhoujb
@contact: zhoujiebing@maimiaotech.com
@date: 2014-06-24 16:47
@version: 0.0.0
@license: Copyright maimiaotech.com
@copyright: Copyright maimiaotech.com

"""
class CampaignType(object):

    CAMPAIGN_GIVEUP = 11
    CAMPAIGN_LOW_CLICK = 12
    CAMPAIGN_LOW_ROI = 13
    CAMPAIGN_OK = 14

    SHOP_IN_DEBT = 101     
    SHOP_BE_PUNISH = 102
    
    CAMPAIGN_OFF_LINE = 111
    CAMPAIGN_LESS_ADGROUPS = 112 
    CAMPAIGN_LOW_BIDMAX = 113
    
    CAMPAIGN_PLATFORM_CLOSE = 121
    CAMPAIGN_PLATFORM_LOW_DISCOUNT = 122
    CAMPAIGN_PLATFORM_LOW_ROI = 123
    
    CAMPAIGN_SCHEDULE_LOW_DISCOUNT = 131
    CAMPAIGN_SCHEDULE_ROI_DIFF = 132
    
    CAMPAIGN_AREA_LESS_CITY = 141
    CAMPAIGN_AREA_LOW_ROI = 142
    
    CAMPAIGN_NO_ADGROUP = 151
    CAMPAIGN_NO_ADGROUP_HANDLE = 152
    CAMPAIGN_STOP = 153
    CAMPAIGN_NO_HANDLE = 154
    
    ALL_CAMPAIGN_TYPES = [
        CAMPAIGN_GIVEUP,
        CAMPAIGN_LOW_CLICK,
        CAMPAIGN_LOW_ROI,
        CAMPAIGN_OK,
        SHOP_IN_DEBT,     
        SHOP_BE_PUNISH,
        CAMPAIGN_OFF_LINE,
        CAMPAIGN_LESS_ADGROUPS, 
        CAMPAIGN_LOW_BIDMAX,
        CAMPAIGN_PLATFORM_CLOSE,
        CAMPAIGN_PLATFORM_LOW_DISCOUNT,
        CAMPAIGN_PLATFORM_LOW_ROI,
        CAMPAIGN_SCHEDULE_LOW_DISCOUNT,
        CAMPAIGN_SCHEDULE_ROI_DIFF,
        
        CAMPAIGN_AREA_LESS_CITY,
        CAMPAIGN_AREA_LOW_ROI,
        
        CAMPAIGN_NO_ADGROUP,
        CAMPAIGN_NO_ADGROUP_HANDLE,
        CAMPAIGN_STOP,
        CAMPAIGN_NO_HANDLE
        ]
    
            


class AdgroupType(object):
    
    ADGROUP_SMALL_CAT = 21
    ADGROUP_LESS_KEYWORD = 22
    ADGROUP_LOW_BIDMAX = 23
    ADGROUP_LOW_BID = 24
    ADGROUP_LOW_TRAFFIC = 25
    ADGROUP_LOW_CVR = 26                           

    ADGROUP_HIGH_CPC_OF_BID = 201
    ADGROUP_HIGH_CPC_OF_QSCORE = 202

    ADGROUP_LOW_RELATIVE_SCORE = 210
    ADGROUP_LOW_CREATIVE_SCORE = 211
    ADGROUP_LOW_BASE_SCORE = 212
    ADGROUP_LOW_CTR = 213
    
    ADGROUP_USER_INCREASE_COST = 220
    ADGROUP_USER_DECREASE_COST = 221

    ADGROUP_NONSEARCH_CLOSE = 230
    ADGROUP_NONSEARCH_LOW_ROI = 231
    
    ADGROUP_UNKNOW = 400

    ALL_ADGROUP_TYPES = [
        ADGROUP_SMALL_CAT,
        ADGROUP_LESS_KEYWORD,
        ADGROUP_LOW_BIDMAX,
        ADGROUP_LOW_BID,
        ADGROUP_LOW_TRAFFIC,
        ADGROUP_LOW_CVR,                           
        ADGROUP_HIGH_CPC_OF_BID,
        ADGROUP_HIGH_CPC_OF_QSCORE,
        ADGROUP_LOW_RELATIVE_SCORE,
        ADGROUP_LOW_CREATIVE_SCORE,
        ADGROUP_LOW_BASE_SCORE,
        ADGROUP_LOW_CTR,
        ADGROUP_USER_INCREASE_COST,
        ADGROUP_USER_DECREASE_COST,
        ADGROUP_NONSEARCH_CLOSE,
        ADGROUP_NONSEARCH_LOW_ROI,
        ADGROUP_UNKNOW
        ]


CAMPAIGN_GIVEUP_REASON = {
        CampaignType.CAMPAIGN_NO_ADGROUP:"计划内无推广组"
        ,CampaignType.CAMPAIGN_NO_ADGROUP_HANDLE:"计划内无推广组托管"
        ,CampaignType.CAMPAIGN_STOP:"计划暂停"
        ,CampaignType.CAMPAIGN_NO_HANDLE:"计划未托管"
        ,CampaignType.SHOP_IN_DEBT:"店铺欠费"
        ,CampaignType.SHOP_BE_PUNISH:"店铺直通车违禁"

        }

CAMPAIGN_LOW_CLICK_REASON = {
        CampaignType.CAMPAIGN_PLATFORM_CLOSE:"计划站外或无线未开起"
        ,CampaignType.CAMPAIGN_PLATFORM_LOW_DISCOUNT:"计划站外折扣设置过低"
        ,CampaignType.CAMPAIGN_SCHEDULE_LOW_DISCOUNT:"计划分时折扣过低"
        ,CampaignType.CAMPAIGN_AREA_LESS_CITY:"计划地域勾选过少"
        ,CampaignType.CAMPAIGN_OFF_LINE:"计划提前下线"
        ,CampaignType.CAMPAIGN_LESS_ADGROUPS:"推广组不足"
        ,CampaignType.CAMPAIGN_LOW_BIDMAX:"计划最高出价设置过低"

        ,AdgroupType.ADGROUP_NONSEARCH_CLOSE:"推广组定向未开起"
        ,AdgroupType.ADGROUP_LOW_CREATIVE_SCORE:"推广组创意不佳"
        ,AdgroupType.ADGROUP_LOW_BASE_SCORE:"推广组基础分低"
        ,AdgroupType.ADGROUP_LOW_RELATIVE_SCORE:"推广组相关性低"
        ,AdgroupType.ADGROUP_SMALL_CAT:"宝贝属于小类目"
        ,AdgroupType.ADGROUP_LESS_KEYWORD:"推广组内关键词过少"
        ,AdgroupType.ADGROUP_LOW_BIDMAX:"推广组最高出价设置过低"
        ,AdgroupType.ADGROUP_LOW_BID:"推广组关键词出价过低"
        ,AdgroupType.ADGROUP_LOW_TRAFFIC:"推广组关键词偏冷"

        }


CAMPAIGN_LOW_ROI_REASON = {
        CampaignType.CAMPAIGN_OFF_LINE:"计划提前下线"
        ,CampaignType.CAMPAIGN_PLATFORM_LOW_ROI:"计划站外或无线ROI过低"
        ,CampaignType.CAMPAIGN_SCHEDULE_ROI_DIFF:"计划分时折扣设置不合理"
        ,CampaignType.CAMPAIGN_AREA_LOW_ROI:"计划地域设置不合理"
        
        ,AdgroupType.ADGROUP_NONSEARCH_LOW_ROI:"推广组定向设置不合理"
        ,AdgroupType.ADGROUP_LOW_CVR:"宝贝转化率低"
        ,AdgroupType.ADGROUP_HIGH_CPC_OF_BID:"推广组CPC过高"
        ,AdgroupType.ADGROUP_HIGH_CPC_OF_QSCORE:"推广组质量分低导致CPC过高"
        
        }                

