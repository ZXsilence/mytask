#encoding=utf8
__author__ = 'zhoujiebing@maimiaotech.com'

import copy 
import datetime
import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ClouddataMbpDataGetRequest 
from TaobaoSdk import TaobaoClient
from tao_models.common.decorator import  tao_api_exception, ysf_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from api_server.conf.settings import APP_SETTINGS,SERVER_URL

logger = logging.getLogger(__name__)

class ClouddataMbpDataGet(object):

    @classmethod
    def _decode_clouddata(cls,rsp):
        
        column_list = rsp.__dict__.get('column_list',[])
        row_list =  rsp.__dict__.get('row_list',[]) 
        elements = []
        if column_list == [] or row_list == []:
            return elements
        for row in row_list:
            values = row.values
            rpt = {}
            for i in range(len(values)):
                key = column_list[i]
                rpt[key] = values[i]
            elements.append(rpt)
        return elements
    
    @classmethod
    @ysf_exception()
    @tao_api_exception()
    def get_data_from_clouddata(cls, sql_id, query_dict):
        ret = []
        page_count = 0
        while True:
            query_dict_single = copy.copy(query_dict)
            query_dict_single['sub_limit'] = 5000
            query_dict_single['sub_offset'] = page_count*query_dict_single['sub_limit']
            parameter = ",".join([str(k)+"="+str(v) for k,v in query_dict_single.items()])
            req = ClouddataMbpDataGetRequest() 
            req.sql_id = sql_id
            req.parameter = parameter
            soft_code = 'YZB'
            rsp = ApiService.execute(req, None, soft_code)
            #app_key = APP_SETTINGS[soft_code]['app_key']
            #app_secret = APP_SETTINGS[soft_code]['app_secret']
            #params = ApiService.getReqParameters(req)
            #taobao_client = TaobaoClient(SERVER_URL,app_key,app_secret)
            #access_token = '620042781c28e996fc0808e9ff762074923ZZfdd0df557292686194'
            #rsp = ApiService.getResponseObj(taobao_client.execute(params, access_token, {}))
            if rsp.isSuccess():
                res = cls._decode_clouddata(rsp)
                ret.extend(res)
                if len(res) < query_dict_single['sub_limit']:
                    break
                page_count += 1
            else:
                return []

        return ret
    
    @classmethod
    def get_item_pc_page_url(cls, shop_id, auction_id, sdate, edate):
        """获取商品PC流量去向"""
        return_keys = (('dt','日期'),('shop_id','店铺id'),('auction_id','商品id'),('access_url','去向url'),('uv','uv'))
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "auction_id":auction_id, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 111851 
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret, return_keys

    @classmethod
    def get_shop_pc_page_url(cls,shop_id,sdate,edate):
        """获取全店PC流量去向"""
        return_keys = (('dt','日期'),('shop_id','店铺id'),('auction_id','商品id'),('access_url','去向url'),('uv','uv'))
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id,  "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 111871
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret, return_keys
    
    @classmethod
    def get_shop_area_rpt_sum(cls, shop_id, edate):
        """获取店铺最近30天地域报表"""
        return_keys = (('shop_id','shop_id'), ('region_name','地域名称') , \
                       ('ipv','ipv'),('iuv','iuv'),('pv','pv'),('uv','uv'),('view_repeat_num','浏览回头客'),\
                       ('alipay_winner_num','支付买家数'), ('alipay_auction_num','支付商品数'), \
                       ('alipay_trade_amt','支付金额'),('alipay_trade_num','支付订单数'))
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "edate":edate_str}
        result_list = []

        sql_id = 111869 
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret, return_keys

    @classmethod
    def get_shop_pc_nature_query(cls, shop_id, sdate, edate):
        """获取店铺pc自然query报表"""
        return_keys = (('thedate','日期'), ('seller_id','seller_id'), ('shop_id','shop_id'), ('auction_id','商品id') , \
                       ('query','搜索词'),('pv','pv'),('click','click'),('uv','uv'),\
                       ('order_winner_num','下单买家数'), ('alipay_winner_num','支付买家数'), ('alipay_auction_num','支付商品数'), \
                       ('alipay_trade_amt','支付金额'),('alifav_num','收藏数'),('alicart_num','加购数'))
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 111846 
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret, return_keys

    @classmethod
    def get_shop_mobile_nature_query(cls, shop_id, sdate, edate):
        """获取店铺mobile自然query报表"""
        return_keys = (('thedate','日期'), ('seller_id','seller_id'), ('shop_id','shop_id'), ('auction_id','商品id') , \
                       ('query','搜索词'),('pv','pv'),('uv','uv'),\
                       ('order_winner_num','下单买家数'), ('alipay_winner_num','支付买家数'), ('alipay_auction_num','支付商品数'), \
                       ('alipay_trade_amt','支付金额'),('alifav_num','收藏数'),('alicart_num','加购数'))
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 111847
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret, return_keys
    
    @classmethod
    def get_item_traffic_trade_d(cls, shop_id, sdate, edate):
        return_keys = (('thedate','日期'), ('seller_id','seller_id'), ('shop_id','shop_id'), ('auction_id','商品id') , \
                       ('ipv','pv'), ('iuv','uv'), ('bounce_rate','跳失率'), ('gmv_trade_num','下单订单数'), ('alipay_trade_num','支付订单数'), \
                       ('gmv_winner_num','下单买家数'), ('alipay_winner_num','支付买家数'), ('gmv_auction_num','下单商品数'), \
                       ('alipay_auction_num','支付商品数'), ('gmv_trade_amt','下单金额'), ('alipay_trade_amt','支付金额'))

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 104456 
        #历史截止20160212
        if edate <= datetime.datetime(2016,2,12):
            sql_id = 106790
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret, return_keys

    @classmethod
    def get_item_platform_traffic_trade_d(cls, shop_id, sdate, edate):
        return_keys = (('thedate','日期'), ('seller_id','seller_id'), ('shop_id','shop_id'), ('auction_id','商品id') , \
                       ('platform_type','平台'), ('ipv','pv'), ('iuv','uv'), ('gmv_trade_num','下单订单数'), ('alipay_trade_num','支付订单数'), \
                       ('gmv_winner_num','下单买家数'), ('alipay_winner_num','支付买家数'), ('gmv_auction_num','下单商品数'), \
                       ('alipay_auction_num','支付商品数'), ('gmv_trade_amt','下单金额'), ('alipay_trade_amt','支付金额'))

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 104414 
        #历史截止20160212
        if edate <= datetime.datetime(2016,2,12):
            sql_id = 106791
        if edate <= datetime.datetime(2015,12,31):
            sql_id = 106867
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret, return_keys

    @classmethod
    def get_shop_platform_traffic_trade_d(cls, shop_id, sdate, edate):
        return_keys = (('thedate','日期'), ('seller_id','seller_id'), ('shop_id','shop_id'), \
                       ('platform_type','平台'), ('pv','pv'), ('uv','uv'), ('ipv','ipv'), ('iuv','iuv'), ('gmv_trade_num','下单订单数'), ('alipay_trade_num','支付订单数'), \
                       ('gmv_winner_num','下单买家数'), ('alipay_winner_num','支付买家数'), ('gmv_auction_num','下单商品数'), \
                       ('alipay_auction_num','支付商品数'), ('gmv_trade_amt','下单金额'), ('alipay_trade_amt','支付金额'))

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 105157
        #历史截止20160212
        if edate <= datetime.datetime(2016,2,12):
            sql_id = 106789
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret, return_keys

    @classmethod
    def get_shop_traffic_trade_d(cls, shop_id, sdate, edate):
        return_keys = (('thedate','日期'), ('seller_id','seller_id'), ('shop_id','shop_id'), \
                       ('pv','pv'), ('uv','uv'), ('ipv','ipv'), ('iuv','iuv'),('visit_repeat_num','visit_repeat_num'),
                       ('trade_repeat_num','trade_repeat_num'),\
                       ('gmv_trade_num','下单订单数'), ('alipay_trade_num','支付订单数'), \
                       ('gmv_winner_num','下单买家数'), ('alipay_winner_num','支付买家数'), ('gmv_auction_num','下单商品数'), \
                       ('alipay_auction_num','支付商品数'), ('gmv_trade_amt','下单金额'), ('alipay_trade_amt','支付金额'))

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 106777
        #历史截止20160212
        if edate <= datetime.datetime(2016,2,12):
            sql_id = 106788
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret, return_keys
    
    @classmethod
    def get_item_pc_page_effect_d(cls, shop_id, sdate, edate):
        return_keys = (('thedate','日期'), ('seller_id','seller_id'), ('shop_id','shop_id'), ('auction_id','商品id') , \
                       ('page_duration','页面停留时间'), ('bounce_cnt','一次入店次数'), ('landing_cnt','入店次数'), ('landing_uv','入店uv'), ('exit_cnt','出店次数'))
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 104413 
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret, return_keys
    
    @classmethod
    def get_one_item_pc_page_effect_d(cls, shop_id, auction_id, sdate, edate):
        return_keys = (('thedate','日期'), ('seller_id','seller_id'), ('shop_id','shop_id'), ('auction_id','商品id') , \
                       ('page_duration','页面停留时间'), ('bounce_cnt','一次入店次数'), ('landing_cnt','入店次数'), ('landing_uv','入店uv'), ('exit_cnt','出店次数'))
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "auction_id":auction_id, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 111848
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret, return_keys
    
    @classmethod
    def get_item_platform_search_effect_d(cls, shop_id, sdate, edate):
        return_keys = (('thedate','日期'), ('seller_id','seller_id'), ('shop_id','shop_id'), ('item_id','商品id') , \
                       ('platform_id','平台'), ('avg_search_rank','平均排名'), ('imps_cnt','展现'), ('clk_cnt','点击'), \
                       ('landing_cnt','入店次数'), ('uv','入店uv'),\
                       ('crt_ord_cnt','下单订单数'), ('pay_ord_cnt','支付订单数'), \
                       ('crt_ord_byr_cnt','下单买家数'), ('pay_ord_byr_cnt','支付买家数'), ('crt_ord_item_qty','下单商品数'), \
                       ('pay_ord_item_qty','支付商品数'), ('crt_ord_amt','下单金额'), ('pay_ord_amt','支付金额'),\
                       ('shop_clt_cnt','店铺收藏数'),('item_clt_cnt','商品收藏数'),('cart_item_qty','加购数'))

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 104412 
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret, return_keys


    @classmethod
    def get_shop_item_info_d(cls, shop_id, sdate, edate):
        """获取店铺所有宝贝信息"""

        return_keys = (('seller_id','seller_id'), ('shop_id','shop_id'), ('auction_id','商品id') , \
                       ('auction_name','商品名称'), ('on_sale_time','上架时间'), ('auction_price','商品价格'), \
                       ('cate_level1_id','一级类目id'), ('cate_level2_id','二级类目id'), ('item_property_set','属性集合'))

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 104692 
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret, return_keys
    
    @classmethod
    def get_item_info(cls, shop_id, sdate, edate, auction_id):
        """获取店铺某宝贝信息"""

        return_keys = (('seller_id','seller_id'), ('shop_id','shop_id'), ('auction_id','商品id') , \
                       ('auction_name','商品名称'), ('on_sale_time','上架时间'), ('auction_price','商品价格'), \
                       ('cate_level1_id','一级类目id'), ('cate_level2_id','二级类目id'), ('item_property_set','属性集合'))

        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "sdate":sdate_str, "edate":edate_str, "auction_id":auction_id}
        result_list = []

        sql_id = 104756
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret, return_keys
    
    @classmethod
    def get_shop_item_zz_effect_d(cls, shop_id, sdate, edate):
        return_keys = (('thedate','日期'), ('seller_id','seller_id'), ('shop_id','shop_id'), ('item_id','商品id') , \
                       ('src_id','来源id'), ('src_parent_id','父来源id'), ('src_name','平台'), ('ipv','ipv'), ('iuv','iuv'), \
                       ('ord_byr_cnt','下单买家数'), ('ord_amt','下单金额'), ('ord_item_qty','下单商品数'), \
                       ('pay_byr_cnt','支付买家数'),('pay_amt','支付金额'), \
                       ('pay_item_qty','支付商品数'), ('item_clt_cnt','商品收藏数'), ('cart_item_qty','商品加购数'))

        result_list = []

        sql_id = 104719
        ret = []
        all_days = (edate - sdate).days
        page_count = 0
        page_flag = True 
        while page_flag:
            new_sdate = sdate + datetime.timedelta(page_count * 6)
            new_edate = new_sdate + datetime.timedelta(5)
            if new_edate >= edate:
                new_edate = edate
                page_flag = False

            sdate_str = new_sdate.strftime("%Y%m%d")
            edate_str = new_edate.strftime("%Y%m%d")
            query_dict = {"shop_id":shop_id, "sdate":sdate_str, "edate":edate_str}
            sub_ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
            ret.extend(sub_ret)
            page_count += 1

        return ret, return_keys

    @classmethod
    def get_shop_list(cls, sdate):
        date_str = sdate.strftime("%Y%m%d")
        query_dict = {"date":date_str}
        result_list = []

        sql_id = 104656 
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret
    
    @classmethod
    def get_shop_cats(cls, shop_id, sdate, edate):
        
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "sdate":sdate_str, "edate":edate_str}
        result_list = []

        sql_id = 104658 
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret

    @classmethod
    def get_shop_pc_web_log_d(cls, shop_id, sdate, edate):
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "sdate":sdate_str, "edate":edate_str}
        sql_id = 111923
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret

    @classmethod
    def get_shop_pc_nature_query_carlos(cls,shop_id,sdate,edate):
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "sdate":sdate_str, "edate":edate_str}
        sql_id = 111910
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret

    @classmethod
    def get_shop_mobile_nature_query_carlos(cls,shop_id,sdate,edate):
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        query_dict = {"shop_id":shop_id, "sdate":sdate_str, "edate":edate_str}
        sql_id = 111911
        ret = ClouddataMbpDataGet.get_data_from_clouddata(sql_id, query_dict)
        return ret

def get_all_shop_cats():
    """查看飞利浦授权店铺包含飞利浦字眼的商品的二级类目情况(次二级类目是从根开始数，不是从叶子开始，注意)"""
    file_data = file('/home/zhoujb/Algorithm/BidwordExtend/data/api_cat.csv').read().split('\n')
    
    cat_dict = {}
    for line in file_data:
        line_data = line.split(',')
        if len(line_data) < 5:
            continue

        cat_dict[int(line_data[4])] = line_data[2]


    sdate = datetime.datetime(2015,12,29,0,0)
    edate = sdate
    shop_list = ClouddataMbpDataGet.get_shop_list(sdate)
    file_obj = file('shop_cats2.csv', 'w')
    for shop in shop_list:
        shop_cats = ClouddataMbpDataGet.get_shop_cats(int(shop['shop_id']), sdate, edate)
        cats = [cat_dict.get(int(a['cate_level2_id']),'其他') for a in shop_cats]
        file_obj.write('%s:%s\n' % (shop['shop_id'], ','.join(cats)))
    file_obj.close()

if __name__ == '__main__':
    sdate = datetime.datetime(2017,6,22,0,0)
    edate = datetime.datetime(2017,6,28,0,0)
    shop_id = 105296061
    res = ClouddataMbpDataGet.get_shop_pc_web_log_d(shop_id,sdate,edate)
    print res
