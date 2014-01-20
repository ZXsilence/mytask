#encoding=utf8
import os, sys
import pymongo
from pymongo import Connection
import logging

if pymongo.version.startswith("2.5"):
    import bson.objectid
    import bson.json_util
    pymongo.objectid = bson.objectid
    pymongo.json_util = bson.json_util
    sys.modules['pymongo.objectid'] = bson.objectid
    sys.modules['pymongo.json_util'] = bson.json_util

currDir = os.path.normpath(os.path.dirname(__file__))
APISDK = os.path.normpath(os.path.join(currDir,'../../../TaobaoOpenPythonSDK'))
BACKENDS = os.path.normpath(os.path.join(currDir,'../../../backends/'))
sys.path.append(APISDK)
sys.path.append(BACKENDS)

api_source = None
def set_api_source(source):
    global api_source
    api_source = source

SERVER_URL = "http://223.5.20.253:8002/router/rest"

MGDBS = {
        'api_conn':{
            'HOST':'app.maimiaotech.com',
            'PORT':2201,
            'USER':'',
            'PASSWORD':''
        }
    }

#利用mongodb 自带的connection poll 来管理数据库连接
api_conn = Connection(host=MGDBS['api_conn']['HOST'],port=MGDBS['api_conn']['PORT'])

APP_SETTINGS = {

        'SYB':{
            'name':'省油宝',
            'app_key':'12685542',
            'app_secret':'6599a8ba3455d0b2a043ecab96dfa6f9',
            'article_code':'ts-1796606',
            'soft_code':'SYB'
        },
        'BD':{
            'name':'北斗',
            'app_key':'21065688',
            'app_secret':'74aecdce10af604343e942a324641891',
            'article_code':'ts-1797607',
            'soft_code':'BD'
        },
        'ZZB':{
            'name':'无线省油宝',
            'app_key':'21402298',
            'app_secret':'4f36c8581d344f344b1b98104f5d006e',
            'article_code':'FW_GOODS-1886206',
            'soft_code':'ZZB'
        },
        'JX':{
            'name':'车手绩效',
            'app_key':'21569590',
            'app_secret':'2505da58f14cae10cbe9d2e651f2dbe4',
            'article_code':'FW_GOODS-1886294',
            'soft_code':'JX'
        },
        'TC':{
            'name':'淘词',
            'app_key':'21185579',
            'app_secret':'048978dcef7e423d5b3a8dff8b22265e',
            'article_code':'ts-1817244',
            'soft_code':'TC'
        }
        #'WY':{
        #    'name':'微页',
        #    'app_key':'',
        #    'app_secret':'',
        #    'article_code':'',
        #    'soft_code':'WY'
        #},
}

API_SOURCE = [
              'syb_webpage',                    #省油宝页面请求
              'syb_auto_campaign_optimize',     #省油宝长尾优化
              'syb_auto_non_campaign_optimize', #省油宝定向优化
              'syb_key_campaign_optimize',      #省油宝加力优化
              'syb_auto_creative_optimize',     #省油宝标题优化
              'syb_deal_keyword_update',        #省油宝成交词抓取脚本
              'syb_check_shop_status',          #省油宝店铺状态检查脚本
              'syb_user_alert',                 #省油宝用户到期提醒脚本
              'api_test',                       #api测试

              #北斗
              #掌中宝
              #query_db
              #report_db
              #短信通知脚本
              #邮件统计脚本
              # ...

              ]

API_NEED_SUBWAY_TOKEN = [
            'taobao.simba.rpt.adgroupbase.get',
            'taobao.simba.rpt.adgroupeffect.get',
            'taobao.simba.rpt.adgroupcreativebase.get',
            'taobao.simba.rpt.adgroupcreativeeffect.get',
            'taobao.simba.rpt.adgroupkeywordbase.get',
            'taobao.simba.rpt.adgroupkeywordeffect.get',
            'taobao.simba.rpt.adgroupnonsearchbase.get',
            'taobao.simba.rpt.adgroupnonsearcheffect.get',
            'taobao.simba.rpt.campadgroupbase.get',
            'taobao.simba.rpt.campadgroupeffect.get',
            'taobao.simba.rpt.campaignbase.get',
            'taobao.simba.rpt.campaigneffect.get',
            'taobao.simba.rpt.custbase.get',
            'taobao.simba.rpt.custeffect.get',
            'taobao.simba.rpt.demographicbase.get',
            'taobao.simba.rpt.demographiceffect.get'
        ]


