#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wulingping
@contact: wulingping@maimiaotech.com
@date: 2014-10-08 16:42
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import unittest
import sys
sys.path.append('./')
import MTextTestRunner
import settings
import datetime

import test_arears_get
import test_fuwu_sale_link_gen
import test_clouddata_mbp_data_get_normal
import test_itemcats_authorize_get
import test_itemcats_get
import test_item_get
import test_item_img_delete_and_upload_and_joint_img
import test_items_list_get
import test_item_update
import test_logistics_address_search
import test_mm_simba_tools_items_top_get
import test_picture_category_get
import test_seller_catslist_get
import test_picture_upload_and_delete
import test_shopcats_list_get
import test_shop_get
import test_simba_account_balance_get
import test_simba_adgroup_add_and_delete_and_exist_and_update_and_deleteget_and_changeget_and_adgroupsget
import test_simba_adgroupsbycampaignid_get
import test_simba_adgroup_onlineitemsvon_get
import test_simba_campaigns_get_and_update
import test_simba_campaign_add
import test_simba_campaign_area_get
import test_simba_campaign_area_update
import test_simba_campaign_areaoptions_get
import test_simba_campaign_channeloptions_get
import test_simba_campaign_budget_get_and_update
import test_simba_campaign_platform_get_and_update
import test_simba_campaign_schedule_get_and_update
import test_simba_creative_add_delete_changeget
import test_simba_adgroup_adgroupcatmatchs_get
import test_simba_adgroup_catmatch_update
import test_simba_adgroup_nonsearchprices_update
import test_simba_adgroup_nonsearchstates_update
import test_picture_category_add
import test_clouddata_mbp_data_get

import test_promotionmisc_activity_range_add
import test_promotionmisc_activity_range_all_remove
import test_promotionmisc_activity_range_list_get
import test_promotionmisc_activity_range_remove
import test_promotionmisc_item_activity_add
import test_promotionmisc_item_activity_delete
import test_promotionmisc_item_activity_get
import test_promotionmisc_item_activity_list_get
import test_promotionmisc_item_activity_update
import test_promotionmisc_mjs_activity_all_API_total_test
import test_wangwang_eservice_groupmember_get
import test_wangwang_eservice_receivenum_get

import test_vas_subscribe_get
import test_vas_order_search
import test_user_seller_get
import test_topats_4api_total_test
import test_taobao_user_seller_get
import test_taobao_trades_2APIs
import test_taobao_time_get_NOT_USE
import test_taobao_fuwu_scores_get
import test_simba_tools_items_top_get
import test_simba_rpt_custEffectBase_2apis
import test_simba_rpt_campaignEffectBase_2api
import test_simba_rpt_campadgroupEffectBase_2api
import test_simba_rpt_adgroupbase_4api

import test_simba_insight_catsdata_get
import test_simba_insight_catsforecastnew_get
import test_simba_insight_catsinfo_get
import test_simba_insight_catstopwordnew_get
import test_simba_insight_catsworddata_get
import test_simba_insight_relatedwords_get
import test_simba_insight_wordsareadata_get
import test_simba_insight_wordsdata_get
import test_simba_insight_wordspricedata_get
import test_simba_insight_wordssubdata_get
import test_simba_keyword_rankingforecast_get
import test_simba_keywordids_deleted_get
import test_simba_keywords_changed_get
import test_simba_keywords_delete
import test_simba_keywords_qscore_get
import test_simba_keywords_recommend_get
import test_simba_keywordsbyadgroupid_get
import test_simba_keywordsbykeywordids_get
import test_simba_keywordscat_qscore_get
import test_simba_login_authsign_get
import test_simba_keywords_pricevon_set 
import test_simba_keywordsvon_add
import test_simba_customers_authorized_get
import test_mobile_discount
alltests = unittest.TestSuite([test_arears_get.alltests
                               ,test_simba_login_authsign_get.alltests
                               ,test_fuwu_sale_link_gen.alltests
                               ,test_clouddata_mbp_data_get_normal.alltests
                               ,test_itemcats_authorize_get.alltests
                               ,test_itemcats_get.alltests
                               ,test_item_get.alltests
                               ,test_item_img_delete_and_upload_and_joint_img.alltests
                               ,test_items_list_get.alltests
                               ,test_item_update.alltests
                               ,test_logistics_address_search.alltests
                               ,test_mm_simba_tools_items_top_get.alltests
                               ,test_picture_category_get.alltests
                               ,test_seller_catslist_get.alltests
                               ,test_shopcats_list_get.alltests
                               ,test_shop_get.alltests
                               ,test_simba_account_balance_get.alltests
                               ,test_simba_adgroup_add_and_delete_and_exist_and_update_and_deleteget_and_changeget_and_adgroupsget.alltests
                               ,test_simba_adgroupsbycampaignid_get.alltests
                               ,test_simba_adgroup_onlineitemsvon_get.alltests
                               ,test_simba_campaigns_get_and_update.alltests
                               ,test_simba_campaign_add.alltests
                               ,test_simba_campaign_area_get.alltests
                               ,test_simba_campaign_area_update.alltests
                               ,test_simba_campaign_areaoptions_get.alltests
                               ,test_simba_campaign_channeloptions_get.alltests
                               ,test_simba_campaign_budget_get_and_update.alltests
                               ,test_simba_campaign_platform_get_and_update.alltests
                               ,test_simba_campaign_schedule_get_and_update.alltests
                               ,test_simba_creative_add_delete_changeget.alltests
                               ,test_simba_adgroup_adgroupcatmatchs_get.alltests
                               ,test_simba_adgroup_catmatch_update.alltests
                               ,test_simba_adgroup_nonsearchprices_update.alltests
                               ,test_simba_adgroup_nonsearchstates_update.alltests
                               ,test_picture_upload_and_delete.alltests
                               ,test_picture_category_add.alltests
                               ,test_clouddata_mbp_data_get.alltests
                               #promotionmisc暂时不跑
                               #,test_promotionmisc_activity_range_add.alltests
                               #,test_promotionmisc_activity_range_all_remove.alltests
                               #,test_promotionmisc_activity_range_list_get.alltests
                               #,test_promotionmisc_activity_range_remove.alltests
                               #,test_promotionmisc_item_activity_add.alltests
                               #,test_promotionmisc_item_activity_delete.alltests
                               #,test_promotionmisc_item_activity_get.alltests
                               #,test_promotionmisc_item_activity_list_get.alltests
                               #,test_promotionmisc_item_activity_update.alltests
                               #,test_promotionmisc_mjs_activity_all_API_total_test.alltests
                               ,test_wangwang_eservice_groupmember_get.alltests
                               ,test_wangwang_eservice_receivenum_get.alltests
                               ,test_vas_subscribe_get.alltests
                               ,test_vas_order_search.alltests
                               ,test_user_seller_get.alltests
                               ,test_topats_4api_total_test.alltests
                               ,test_taobao_user_seller_get.alltests
                               ,test_taobao_trades_2APIs.alltests
                               ,test_taobao_time_get_NOT_USE.alltests
                               ,test_taobao_fuwu_scores_get.alltests
                               ,test_simba_tools_items_top_get.alltests
                               ,test_simba_rpt_custEffectBase_2apis.alltests
                               ,test_simba_rpt_campaignEffectBase_2api.alltests
                               ,test_simba_rpt_campadgroupEffectBase_2api.alltests
                               ,test_simba_rpt_adgroupbase_4api.alltests
                               ,test_simba_insight_catsdata_get.alltests
                               ,test_simba_insight_catsforecastnew_get.alltests
                               ,test_simba_insight_catsinfo_get.alltests
                               ,test_simba_insight_catstopwordnew_get.alltests
                               ,test_simba_insight_catsworddata_get.alltests
                               ,test_simba_insight_relatedwords_get.alltests,
                               test_simba_insight_wordsareadata_get.alltests,
                               test_simba_insight_wordsdata_get.alltests,
                               test_simba_insight_wordspricedata_get.alltests,
                               test_simba_insight_wordssubdata_get.alltests,
                               test_simba_keyword_rankingforecast_get.alltests,
                               test_simba_keywordids_deleted_get.alltests,
                               test_simba_keywords_changed_get.alltests,
                               test_simba_keywords_delete.alltests,
                               test_simba_keywords_qscore_get.alltests,
                               test_simba_keywords_recommend_get.alltests,
                               test_simba_keywordsbyadgroupid_get.alltests,
                               test_simba_keywordsbykeywordids_get.alltests,
                               test_simba_keywords_pricevon_set.alltests,
                               test_simba_keywordsvon_add.alltests,
                               test_simba_customers_authorized_get.alltests,
                               test_mobile_discount.alltests
                               ])
#alltests = unittest.TestSuite([test_simba_rpt_adgroupbase_4api.alltests])
if __name__ == "__main__":
    if settings.NeedLog:
        fb = file('./report/report_%s.html'%datetime.date.today(),'wb')
        mrunner = MTextTestRunner.TextTestRunner(stream=fb,title='The Result Of Unit Test',description='The first run')
    else:
        mrunner = MTextTestRunner.TextTestRunner()
    mrunner.run(alltests)
    #unittest.main(testRunner = mrunner)
