#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: xieguanfu
@contact: xieguanfu@maimiaotech.com
@date: 2016-06-07 15:12
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""


class ApiCacheConfig(object):
    #api cache 配置,配置各个接口来源是否缓存,缓存的时间
    #什么时候开始需要缓存

    #有效期1天
    MAX_AGE_1 = 24*60

    #有效期6个小时
    MAX_AGE_2 = 6*60

    #有效期3个小时
    MAX_AGE_3 = 3*60

    #有效期1个小时
    MAX_AGE_4 = 60

    #有效期30分钟
    MAX_AGE_5 = 30

    #有效期10分钟
    MAX_AGE_6 = 10

    #有效期5分钟
    MAX_AGE_7 = 5

    start_cache_hour_1 = 8

    IS_GET_YES = True
    IS_GET_NO = False

    API_METHOD_CONFIG = {
        #'taobao.fuwu.sale.link.gen':
        #'taobao.fuwu.scores.get':
        'taobao.clouddata.mbp.data.flowback':{'cache_name':'mbp_data','is_get':IS_GET_NO},
        'taobao.clouddata.mbp.data.get':{'cache_name':'mbp_data','max_age':MAX_AGE_2,'is_get':IS_GET_YES},
        'taobao.areas.get':{'cache_name':'areas','max_age':MAX_AGE_1,'is_get':IS_GET_YES},
        'taobao.itemcats.authorize.get':{'cache_name':'itemcats_authorize','max_age':MAX_AGE_2,'is_get':IS_GET_YES},
        'taobao.itemcats.get':{'cache_name':'itemcats','max_age':MAX_AGE_1,'is_get':IS_GET_YES},

        #'taobao.item.img.delete':{'cache_name':'item_img','is_get':IS_GET_NO},
        #'taobao.item.img.upload':{'cache_name':'item_img','is_get':IS_GET_NO},
        #'taobao.item.joint.img':{'cache_name':'item_img','is_get':IS_GET_NO},
        #'taobao.item.update':{'cache_name':'item_img','is_get':IS_GET_NO},

        'taobao.items.onsale.get':{'cache_name':'item','max_age':MAX_AGE_4,'is_get':IS_GET_YES},
        'taobao.items.seller.list.get':{'cache_name':'item','max_age':MAX_AGE_4,'is_get':IS_GET_YES},
        'taobao.simba.adgroup.onlineitemsvon.get':{'cache_name':'item','max_age':MAX_AGE_4,'is_get':IS_GET_YES},
        'taobao.logistics.address.search':{'cache_name':'logistics_address','max_age':MAX_AGE_1,'is_get':IS_GET_YES},
        'taobao.picture.category.get':{'cache_name':'picture_category','max_age':MAX_AGE_3,'is_get':IS_GET_YES},
        #'taobao.picture.upload':
        #'taobao.promotionmisc.activity.range.add':
        #'taobao.promotionmisc.activity.range.list.get':
        #'taobao.promotionmisc.activity.range.remove':
        #'taobao.promotionmisc.item.activity.add':
        #'taobao.promotionmisc.item.activity.get':
        #'taobao.promotionmisc.item.activity.list.get':
        #'taobao.promotionmisc.item.activity.update':
        #'taobao.promotionmisc.mjs.activity.add':
        #'taobao.promotionmisc.mjs.activity.get':
        #'taobao.promotionmisc.mjs.activity.list.get':
        #'taobao.promotionmisc.mjs.activity.update':
        'taobao.sellercats.list.get':{'cache_name':'sellercats','max_age':MAX_AGE_1,'is_get':IS_GET_YES},
        'taobao.shopcats.list.get':{'cache_name':'shopcats','max_age':MAX_AGE_1,'is_get':IS_GET_YES},
        'taobao.shop.get':{'cache_name':'shop_get','max_age':MAX_AGE_1,'is_get':IS_GET_YES},
        'taobao.simba.account.balance.get':{'cache_name':'balance','max_age':MAX_AGE_6,'is_get':IS_GET_YES},
        'taobao.simba.adgroup.add':{'cache_name':'adgroup','is_get':IS_GET_NO},
        'taobao.simba.adgroup.delete':{'cache_name':'adgroup','is_get':IS_GET_NO},
        #'taobao.simba.adgroupids.deleted.get':
        'taobao.simba.adgroup.mobilediscount.delete':{'cache_name':'adgroup','is_get':IS_GET_NO},
        'taobao.simba.adgroup.mobilediscount.update':{'cache_name':'adgroup','is_get':IS_GET_NO},
        #'taobao.simba.adgroup.nonsearchprices.update':
        'taobao.simba.adgroupsbyadgroupids.get':{'cache_name':'adgroup','max_age':MAX_AGE_4,'is_get':IS_GET_YES}, 
        'taobao.simba.adgroupsbycampaignid.get':{'cache_name':'adgroup','max_age':MAX_AGE_4,'is_get':IS_GET_YES},
        'taobao.simba.adgroups.changed.get':{'cache_name':'adgroup','max_age':MAX_AGE_4,'is_get':IS_GET_YES},
        'taobao.simba.adgroup.update':{'cache_name':'adgroup','is_get':IS_GET_NO},
        #'taobao.simba.adgroups.item.exist':

        #campaign_area 不走缓存,总共调用量也不高,避免用户在直通车后台修改而不一致
        #'taobao.simba.campaign.area.get':{'cache_name':'campaign_area','max_age':MAX_AGE_2,'is_get':IS_GET_YES},
        #'taobao.simba.campaign.area.update':{'cache_name':'campaign_area','is_get':IS_GET_NO},
        'taobao.simba.campaign.areaoptions.get':{'cache_name':'campaign_areaoptions','max_age':MAX_AGE_1,'is_get':IS_GET_YES},
        'taobao.simba.campaign.budget.get':{'cache_name':'budget','max_age':MAX_AGE_3,'is_get':IS_GET_YES}, 
        'taobao.simba.campaign.budget.update':{'cache_name':'budget','is_get':IS_GET_NO},
        'taobao.simba.campaign.channeloptions.get':{'cache_name':'channeloptions','max_age':MAX_AGE_2,'is_get':IS_GET_YES},
        'taobao.simba.campaign.platform.get':{'cache_name':'campaign_platform','max_age':MAX_AGE_2,'is_get':IS_GET_YES},
        'taobao.simba.campaign.platform.update':{'cache_name':'campaign_platform','is_get':IS_GET_NO},
        'taobao.simba.campaign.schedule.get':{'cache_name':'campaign_schedule','max_age':MAX_AGE_2,'is_get':IS_GET_YES},
        'taobao.simba.campaign.schedule.update':{'cache_name':'campaign_schedule','is_get':IS_GET_NO},
        'taobao.simba.campaigns.get':{'cache_name':'campaign','max_age':MAX_AGE_1,'is_get':IS_GET_YES},
        'taobao.simba.campaign.update':{'cache_name':'campaign','is_get':IS_GET_NO},
        'taobao.simba.campaign.add':{'cache_name':'campaign','is_get':IS_GET_NO}, 

        #创意取消cache
        #'taobao.simba.creative.add':{'cache_name':'creative','is_get':IS_GET_NO},
        #'taobao.simba.creative.delete':{'cache_name':'creative','is_get':IS_GET_NO},
        ##'taobao.simba.creativeids.changed.get':
        #'taobao.simba.creatives.get':{'cache_name':'creative','max_age':MAX_AGE_2,'is_get':IS_GET_YES},
        #'taobao.simba.creative.update':{'cache_name':'creative','is_get':IS_GET_NO},

        #'taobao.simba.customers.authorized.get':

        #==============以下待修改==============
        'taobao.simba.insight.catsdata.get':{'cache_name':'catsdata','max_age':MAX_AGE_2,'is_get':IS_GET_YES},
        'taobao.simba.insight.catsforecastnew.get':{'cache_name':'catsforecastnew','max_age':MAX_AGE_2,'is_get':IS_GET_YES},
        #'taobao.simba.insight.catsinfo.get':
        #'taobao.simba.insight.catstopwordnew.get':
        #'taobao.simba.insight.catsworddata.get':
        #'taobao.simba.insight.relatedwords.get':
        #'taobao.simba.insight.wordsareadata.get':
        'taobao.simba.insight.wordsdata.get':{'cache_name':'wordsdata','max_age':MAX_AGE_2,'is_get':IS_GET_YES},
        #'taobao.simba.insight.wordspricedata.get':
        #'taobao.simba.insight.wordssubdata.get':
        #'taobao.simba.keywordids.deleted.get':
        #'taobao.simba.keyword.rankingforecast.get':

        #=============关键词缓存暂不开启================
        #'taobao.simba.keywordsbyadgroupid.get':{'cache_name':'keywords','max_age':MAX_AGE_4,'is_get':IS_GET_YES},
        #'taobao.simba.keywordsbykeywordids.get':{'cache_name':'keywords','max_age':MAX_AGE_4,'is_get':IS_GET_YES},
        ##'taobao.simba.keywords.changed.get':
        #'taobao.simba.keywords.delete':{'cache_name':'keywords','is_get':IS_GET_NO},
        #'taobao.simba.keywords.pricevon.set':{'cache_name':'keywords','is_get':IS_GET_NO},
        #'taobao.simba.keywordsvon.add':{'cache_name':'keywords','is_get':IS_GET_NO},



        'taobao.simba.keywords.qscore.get':{'cache_name':'qscore','max_age':MAX_AGE_2,'is_get':IS_GET_YES},
        #'taobao.simba.keywords.qscore.split.get':
        #'taobao.simba.keywords.realtime.ranking.get':
        #'taobao.simba.keywords.recommend.get':
        #'taobao.simba.login.authsign.get':
        #'taobao.simba.nonsearch.adgroupplaces.add':
        #'taobao.simba.nonsearch.adgroupplaces.get':
        #'taobao.simba.rpt.adgroupbase.get':
        #'taobao.simba.rpt.adgroupcreativebase.get':
        #'taobao.simba.rpt.adgroupcreativeeffect.get':
        #'taobao.simba.rpt.adgroupeffect.get':

        #=============关键词报表暂时不开启============
        'taobao.simba.rpt.adgroupkeywordbase.get':{'cache_name':'rpt_keyword_base','max_age':MAX_AGE_1,'is_get':IS_GET_YES,'start_cache_hour':start_cache_hour_1},
        'taobao.simba.rpt.adgroupkeywordeffect.get':{'cache_name':'rpt_keyword_effect','max_age':MAX_AGE_1,'is_get':IS_GET_YES,'start_cache_hour':start_cache_hour_1},

        #==============人群搜索====================
        'taobao.simba.rpt.targetingtag.get':{'cache_name':'rpt_targetingtag', 'max_age':MAX_AGE_1, 'is_get':IS_GET_YES, 'start_cache_hour':start_cache_hour_1},
        'taobao.simba.serchcrowd.get':{'cache_name':'serchcrowd', 'max_age':MAX_AGE_5, 'is_get':IS_GET_YES},
        'taobao.simba.serchcrowd.batch.delete':{'cache_name':'serchcrowd', 'is_get':IS_GET_NO},
        'taobao.simba.searchtagtemplate.get':{'cache_name':'searchtagtemplate', 'max_age':MAX_AGE_5, 'is_get':IS_GET_YES},
        'taobao.simba.serchcrowd.state.batch.update':{'cache_name':'serchcrowd', 'is_get':IS_GET_NO},
        'taobao.simba.searchcrowd.batch.add':{'cache_name':'serchcrowd', 'is_get':IS_GET_NO},
        'taobao.simba.serchcrowd.price.batch.update':{'cache_name':'serchcrowd', 'is_get':IS_GET_NO},
        #'taobao.simba.rpt.campadgroupbase.get':
        #'taobao.simba.rpt.campadgroupeffect.get':
        #'taobao.simba.rpt.campaignbase.get':
        #'taobao.simba.rpt.campaigneffect.get':
        #'taobao.simba.rpt.custbase.get':
        #'taobao.simba.rpt.custeffect.get':
        #'taobao.simba.rtrpt.adgroup.get':
        #'taobao.simba.rtrpt.bidword.get':
        #'taobao.simba.rtrpt.campaign.get':
        #'taobao.simba.rtrpt.creative.get':
        #'taobao.simba.tools.items.top.get':
        #'taobao.time.get':
        #'taobao.topats.result.get':
        #'taobao.topats.simba.campkeywordbase.get':
        #'taobao.topats.simba.campkeywordeffect.get':
        #'taobao.topats.task.delete':
        #'taobao.trade.fullinfo.get':
        #'taobao.trades.sold.get':
        #'taobao.user.seller.get':
        #'taobao.vas.order.search':
        #'taobao.vas.subscribe.get':
        #'taobao.wangwang.eservice.groupmember.get':

    }

    #update相关修改操作时各种cache按什么字段进行清除cache
    #允许所有接口都按照nick来清除,但是不建议,尽量按照可控制的最小粒度来更新缓存
    API_CACHE_KEY_CONFIG = {
        'campaign':{'remove_keys':['nick']},
        'adgroup':{'remove_keys':['nick']},
        'budget':{'remove_keys':['campaign_id']},
        'sellercats':{'remove_keys':['nick']},
        'logistics_address':{'remove_keys':['nick']},
        'itemcats':{'remove_keys':['nick']},
        'creative':{'remove_keys':['adgroup_id']},
        'shop_get':{'remove_keys':['nick']},
        'item':{'remove_keys':['nick']},
        'item_img':{'remove_keys':['num_iid']},
        #由于上传数据接口只是偶尔使用,mbp_data可以不清除cache
        'mbp_data':{'remove_keys':['sql_id','sid']},
        'campaign_platform':{'remove_keys':['campaign_id']},
        'campaign_area':{'remove_keys':['campaign_id']},
        'campaign_areaoptions':{'remove_keys':[]},
        'areas':{'remove_keys':[]},
        'campaign_schedule':{'remove_keys':['campaign_id']},
        'shopcats':{'remove_keys':[]},
        'itemcats_authorize':{'remove_keys':['nick']},
        'picture_category':{'remove_keys':['nick']},
        'balance':{'remove_keys':['nick']},
        'keywords':{'remove_keys':['nick']},
        'rpt_keyword_base':{'remove_keys':['nick','adgroup_id']},
        'rpt_keyword_effect':{'remove_keys':['nick','adgroup_id']},
        'serchcrowd':{'remove_keys':['nick']},
        'searchtagtemplate':{'remove_keys':['nick']},
        'rpt_targetingtag':{'remove_keys':['nick', 'campaign_id']},
    }

if __name__ == '__main__':
    cache_name_list = set(obj[1]['cache_name'] for obj in ApiCacheConfig.API_METHOD_CONFIG.iteritems())
    print cache_name_list
