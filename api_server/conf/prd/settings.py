#encoding=utf8
import os, sys
import pymongo
from pymongo import Connection
import logging
import MySQLdb
from DBUtils.PooledDB import PooledDB

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
API_HOST = 'eco.taobao.com'
API_HOST = 'gw.api.taobao.com'
API_PORT = 80
SERVER_URL = "https://%s:%s/router/rest" %(API_HOST,API_PORT)
API_HOST = "gw.api.taobao.com"
SERVER_URL = "http://%s:%s/router/rest" %(API_HOST,API_PORT)

API_THRIFT = {
        #'host':'api.maimiaotech.com',
        'host':'10.242.173.131',
        'port':30005
    }

api_source = None
def set_api_source(source):
    global api_source
    if api_source:
        print 'api_source has already been set:',api_source
        return 
    api_source = source
    print 'set api_source:',api_source

def get_api_source():
    global api_source
    return api_source
API_VIRTUAL_TEST=False

logger = logging.getLogger("api_server")
hdlr = logging.FileHandler('/alidata1/logs/api_server.log')
hdlr.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(name)s:%(lineno)-15d %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
logger.propagate = False

logger2 = logger

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
        'QN':{
            'name':'省油宝千牛插件',
            'app_key':'21402298',
            'app_secret':'4f36c8581d344f344b1b98104f5d006e',
            'article_code':'FW_GOODS-1886206',
            'soft_code':'QN'
        },
        'TC':{
            'name':'淘词',
            'app_key':'21185579',
            'app_secret':'048978dcef7e423d5b3a8dff8b22265e',
            'article_code':'ts-1817244',
            'soft_code':'TC'
        },
        'YZB':{
            'name':'优钻宝',
            'app_key':'23196049',
            'app_secret':'2bb89aa556b1698b1a7225f521d41e42',
            'article_code':'FW_GOODS-1000078795',
            'soft_code':'YZB'
        },
        'WY':{
            'name':'微页',
            'app_key':'21682149',
            'app_secret':'21b808683af61a3929d9d9cd67057b1f',
            'article_code':'FW_GOODS-1906099',
            'soft_code':'WY'
        },
        #'JX':{
        #    'name':'车手绩效',
        #    'app_key':'21569590',
        #    'app_secret':'2505da58f14cae10cbe9d2e651f2dbe4',
        #    'article_code':'FW_GOODS-1886294',
        #    'soft_code':'JX'
        #},

        # 省油宝内购服务，app_key、app_secret都与省油宝保持一致，soft_code仅用于订单获取脚本insert_orders，在调用ApiService的execute方法时，会统一转换成'SYB'
        'TGJHS': {
            'name': '托管计划数量+1',
            'app_key': '12685542',
            'app_secret': '6599a8ba3455d0b2a043ecab96dfa6f9',
            'article_code': 'FW_GOODS-1000498060',
            'soft_code': 'TGJHS'
        },
        'LHBSY': {
            'name': '领航版功能试用',
            'app_key': '12685542',
            'app_secret': '6599a8ba3455d0b2a043ecab96dfa6f9',
            'article_code': 'FW_GOODS-1000497964',
            'soft_code': 'LHBSY'
        },
        'CT': {
            'name': '车图',
            'app_key': '12685542',
            'app_secret': '6599a8ba3455d0b2a043ecab96dfa6f9',
            'article_code': 'FW_GOODS-1000497765',
            'soft_code': 'CT'
        },
        'XQY': {
            'name': '详情页',
            'app_key': '12685542',
            'app_secret': '6599a8ba3455d0b2a043ecab96dfa6f9',
            'article_code': 'FW_GOODS-1000498191',
            'soft_code': 'XQY'
        },
        'ZD': {
            'name': '诊断',
            'app_key': '12685542',
            'app_secret': '6599a8ba3455d0b2a043ecab96dfa6f9',
            'article_code': 'FW_GOODS-1000498061',
            'soft_code': 'ZD'
        }
}

# 省油宝内购服务soft_code
PURCHASE_SOFT_CODE_TUPLE = ('TGJHS', 'LHBSY', 'CT', 'XQY', 'ZD')

# SYB In-Application Purchase，key为SYB版本item_code，sub_type：1=周期型，2=计量型
IAP_SETTINGS = {
    # 基础 --> 托管计划数量+1，领航版功能试用，车图，详情页，诊断
    'ts-1796606-3': [
        {
            'article_code': 'FW_GOODS-1000498060',
            'sub_type': 1
        },
        {
            'article_code': 'FW_GOODS-1000497964',
            'sub_type': 1
        },
        {
            'article_code': 'FW_GOODS-1000497765',
            'sub_type': 2
        },
        {
            'article_code': 'FW_GOODS-1000498191',
            'sub_type': 2
        },
        {
            'article_code': 'FW_GOODS-1000498061',
            'sub_type': 2
        }
    ],
    # 进阶 --> 托管计划数量+1，领航版功能试用，车图，详情页，诊断
    'ts-1796606-v5': [
        {
            'article_code': 'FW_GOODS-1000498060',
            'sub_type': 1
        },
        {
            'article_code': 'FW_GOODS-1000497964',
            'sub_type': 1
        },
        {
            'article_code': 'FW_GOODS-1000497765',
            'sub_type': 2
        },
        {
            'article_code': 'FW_GOODS-1000498191',
            'sub_type': 2
        },
        {
            'article_code': 'FW_GOODS-1000498061',
            'sub_type': 2
        }
    ],
    # 旗舰 --> 领航版功能试用，车图，详情页，诊断
    'ts-1796606-v5_old': [
        {
            'article_code': 'FW_GOODS-1000497964',
            'sub_type': 1
        },
        {
            'article_code': 'FW_GOODS-1000497765',
            'sub_type': 2
        },
        {
            'article_code': 'FW_GOODS-1000498191',
            'sub_type': 2
        },
        {
            'article_code': 'FW_GOODS-1000498061',
            'sub_type': 2
        }
    ],
    # 领航 --> 车图，详情页，诊断
    'ts-1796606-v10': [
        {
            'article_code': 'FW_GOODS-1000497765',
            'sub_type': 2
        },
        {
            'article_code': 'FW_GOODS-1000498191',
            'sub_type': 2
        },
        {
            'article_code': 'FW_GOODS-1000498061',
            'sub_type': 2
        }
    ],
    # 领航顾问 --> 车图，详情页，诊断
    'ts-1796606-v6': [
        {
            'article_code': 'FW_GOODS-1000497765',
            'sub_type': 2
        },
        {
            'article_code': 'FW_GOODS-1000498191',
            'sub_type': 2
        },
        {
            'article_code': 'FW_GOODS-1000498061',
            'sub_type': 2
        }
    ],
    # 云车手 --> 车图，详情页
    'ts-1796606-v7': [
        {
            'article_code': 'FW_GOODS-1000497765',
            'sub_type': 2
        },
        {
            'article_code': 'FW_GOODS-1000498191',
            'sub_type': 2
        }
    ],
    # 资深云车手 --> 车图，详情页
    'ts-1796606-v9': [
        {
            'article_code': 'FW_GOODS-1000497765',
            'sub_type': 2
        },
        {
            'article_code': 'FW_GOODS-1000498191',
            'sub_type': 2
        }
    ]
}

IAP_TOTAL_LIST = [
    {
        'name': '自动计划数加油包',
        'article_code': 'FW_GOODS-1000498060',
        'item_code': 'FW_GOODS-1000498060-1',
        'sub_type': 1
    },
    {
        'name': '领航版功能试用',
        'article_code': 'FW_GOODS-1000497964',
        'item_code': 'FW_GOODS-1000497964-1',
        'sub_type': 1
    },
    {
        'name': '资深设计创意车图制作',
        'article_code': 'FW_GOODS-1000497765',
        'item_code': 'FW_GOODS-1000497765-1',
        'sub_type': 2
    },
    {
        'name': '资深设计详情页定制服务',
        'article_code': 'FW_GOODS-1000498191',
        'item_code': 'FW_GOODS-1000498191-1',
        'sub_type': 2
    },
    {
        'name': '资深车手1对1详细诊断',
        'article_code': 'FW_GOODS-1000498061',
        'item_code': 'FW_GOODS-1000498061-1',
        'sub_type': 2
    }
]

#API调用源注册，只有注册过的source才允许调用API
API_SOURCE = [
              'normal_test',                    #普通测试
              'check_shop_infos',               #check_shop_infos脚本
              'crm_scripts',                    #crm脚本
              'queryall',                       #queryall脚本
              'user_center',                    #user_center
              'data_center',                    #data_center
              'analysis',                       #analysis

              #省油宝
              'syb_webpage',                    #省油宝页面请求
              'syb_auto_campaign_optimize',     #省油宝长尾优化
              'syb_auto_non_campaign_optimize', #省油宝定向优化
              'syb_hot_campaign_optimize',      #省油宝测款优化
              'syb_key_campaign_optimize',      #省油宝加力优化
              'syb_auto_creative_optimize',     #省油宝标题优化
              'syb_deal_keyword_update',        #省油宝成交词抓取脚本
              'syb_user_alert',                 #省油宝用户到期提醒脚本

              #千牛插件
              'qn_webpage',                    #千牛插件页面请求
              'qn_auto_campaign_optimize',     #千牛插件长尾优化
              'qn_auto_non_campaign_optimize', #千牛插件定向优化
              'qn_key_campaign_optimize',      #千牛插件加力优化
              'qn_auto_creative_optimize',     #千牛插件标题优化
              'qn_deal_keyword_update',        #千牛插件成交词抓取脚本
              'qn_user_alert',                 #千牛插件用户到期提醒脚本

              #北斗
              'bd_webpage',
              'bd_auto_campaign_optimize',      #北斗长尾优化
              'bd_deal_keyword_update',         #北斗成交词抓取脚本
              'bd_user_alert',                  #北斗用户到期提醒脚本

              #淘词
              'tc_webpage',                     #淘词页面请求

              #strategy
              'st_webpage',                     #strategy页面请求

              #strategy
              'crm_webpage',                     #crm页面请求

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


#from api_server.thrift.ApiCenterClient import ApiCenterClient
#api_client  = ApiCenterClient('localhost',9090)
