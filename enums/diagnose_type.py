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

    CAMPAIGN_GIVEUP = 1
    CAMPAIGN_LOW_TRAFFIC = 2
    CAMPAIGN_LOW_ROI = 3
    CAMPAIGN_OK = 4

    CAMPAIGN_OFF_LINE = 11
    CAMPAIGN_LESS_ADGROUPS = 12
　　CAMPAIGN_LOW_BIDMAX = 13
　　
　　CAMPAIGN_PLATFORM_CLOSE = 111
　　CAMPAIGN_PLATFORM_LOW_DISCOUNT = 112
　　CAMPAIGN_PLATFORM_LOW_ROI = 113
　　
　　CAMPAIGN_SCHEDULE_LOW_DISCOUNT = 121
　　CAMPAIGN_SCHEDULE_ROI_DIFF = 122
　　
　　CAMPAIGN_AREA_LESS_CITY = 131
　　CAMPAIGN_AREA_LOW_ROI = 132
　　
　　CAMPAIGN_NONSEARCH_CLOSE = 141
　　CAMPAIGN_NONSEARCH_LOW_ROI = 142

    CAMPAIGN_NO_ADGROUP = 201
    CAMPAIGN_NO_ADGROUP_HANDLE = 202
    CAMPAIGN_STOP = 203
    CAMPAIGN_NO_HANDLE = 204
    
    SHOP_IN_DEBT = 301     
    SHOP_BE_PUNISH = 302


class AdgroupType(object):
    
    ADGROUP_SMALL_CAT = 1
    ADGROUP_LESS_KEYWORD = 2
    ADGROUP_LOW_CPCMAX = 3
    ADGROUP_LOW_BID = 4
    ADGROUP_LOW_TRAFFIC = 5
    ADGROUP_LOW_CVR = 6
　　ADGROUP_HIGH_CPC_OF_BID = 7
    ADGROUP_HIGH_CPC_OF_QSCORE = 8
    ADGROUP_LOW_RELATIVE_SCORE = 9
    ADGROUP_LOW_CREATIVE_SCORE = 10
　　ADGROUP_LOW_BASE_SCORE = 11
　　ADGROUP_LOW_BIDMAX = 12
　　ADGROUP_LOW_BID = 13

CAMPAIGN_GIVEUP_REASON = {
        CampaignType.CAMPAIGN_NO_ADGROUP:"计划内无推广组"
        ,CampaignType.CAMPAIGN_NO_ADGROUP_HANDLE:"计划内无推广组托管"
        ,CampaignType.CAMPAIGN_STOP:"计划暂停"
        ,CampaignType.CAMPAIGN_NO_HANDLE:"计划未托管"
        ,CampaignType.SHOP_IN_DEBT:"店铺欠费"
        ,CampaignType.SHOP_BE_PUNISH:"店铺直通车违禁"

        }

CAMPAIGN_LOW_TRAFFIC_REASON = {
        CampaignType.CAMPAIGN_PLATFORM_CLOSE:"计划站外或无线未开起"
        ,CampaignType.CAMPAIGN_PLATFORM_LOW_DISCOUNT:"计划站外折扣设置过低"
        ,CampaignType.CAMPAIGN_NONSEARCH_CLOSE:"计划定向未开起"
        ,CampaignType.CAMPAIGN_SCHEDULE_LOW_DISCOUNT:"计划分时折扣过低"
        ,CampaignType.CAMPAIGN_AREA_LESS_CITY:"计划地域勾选过少"
        ,CampaignType.CAMPAIGN_OFF_LINE:"计划提前下线"
        ,CampaignType.CAMPAIGN_LESS_ADGROUPS:"推广组不足"
        ,CampaignType.CAMPAIGN_LOW_BIDMAX:"计划最高出价设置过低"

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
        ,CampaignType.CAMPAIGN_NONSEARCH_LOW_ROI:"计划定向设置不合理"
        
        ,AdgroupType.ADGROUP_LOW_CVR:"宝贝转化率低"
        ,AdgroupType.ADGROUP_HIGH_CPC_OF_BID:"推广组CPC过高"
        ,AdgroupType.ADGROUP_HIGH_CPC_OF_QSCORE:"推广组质量分低导致CPC过高"
        
        }                

