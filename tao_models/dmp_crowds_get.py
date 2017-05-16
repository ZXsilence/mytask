#encoding=utf8
'''
Created on 2012-8-10

@author: dk
'''
import sys
import os
import logging
import logging.config
import json
import datetime
from copy import deepcopy


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import DmpCrowdsGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class DmpCrowdsGet(object):

    page_size = 200
    
    @classmethod
    @tao_api_exception()
    def get_dmp_crowds(cls, nick, soft_code = 'YZB'):
        req = DmpCrowdsGetRequest()
        req.is_query_all = 1
        req.offset = 0
        req.limit = 50 #时间原因，先不分页了
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.results)

if __name__ == '__main__':
    from tao_models.zuanshi_category_rpts_get import ZuanshiCategoryRptsGet 
    nick = '优美妮旗舰店'
    nick = '飞利浦润氏专卖店'
    sdate = datetime.datetime.now() - datetime.timedelta(days=1)
    nick_list = ["麦苗科技营销","麦苗科技001","chinchinstyle","philips泰璞专卖店","飞利浦盛元专卖店","飞利浦天涯专卖店","philips飞利浦金穗专卖店","飞利浦路迪斯达专卖店","philips飞浦专卖店","飞利浦京创专卖店","飞利浦润诚专卖店","飞利浦隆达专卖店","飞利浦乾升专卖店","philips瑞新成专卖店","philips澳格尔专卖店","philips宇润翔专卖店","philips金舜源专卖店","philips悠芊专卖店","飞利浦科电佳业专卖店","philips飞利浦流翔专卖店","飞利浦星源专卖店","飞利浦上游专卖店","飞利浦璞旭专卖店","智翔母婴专营店","喜贝母婴专营店","飞利浦大华专卖店","飞利浦鼎豪专卖店","飞利浦百诚网络专卖店","飞利浦鼎盛年华专卖店","avent新安怡贝朗专卖店","philips飞利浦丽新专卖店","好意贝母婴专营店","philips新合作专卖店","飞利浦趣浪专卖店","飞利浦拓威隆专卖店","飞利浦官方旗舰店","philips鑫龙吉专卖店","鼎旗母婴专营店","philips华泰鸿业专卖店","欣灵母婴专营店","avent新安怡海纳专卖店","奥翼母婴专营店","飞利浦新安怡旗舰店","飞利浦润氏专卖店","bruinrocks","周哼哼","弓长t","凯络上海","天酷母婴专营店","avent新安怡蓓幼专卖店","东潮母婴专营店","飞利浦新顶华专卖店","飞利浦本汇专卖店","飞利浦畅卓专卖店","philips飞利浦宏通专卖店","philips飞利浦万翔专卖店","philips飞利浦巢悦专卖店","philips飞利浦威铭专卖店","格力威铭专卖店","鑫鑫东莞格力一级代理","飞利浦铭居专卖店","philips飞利浦爱多专卖店","上海君交电器专营店","奉昊天","发发发通信","戎庭蕊","凌征凤","西洋简单一点","宝宝的玩具梦","孕惠妈咪","befueice旗舰店","q15000190727","iixin","黯香袭我","觅水的双鱼","e男沙龙","shanbaocun521","birlalakshmi","nneway","栋梁鸟旗舰店","天之歌零食屋","u美优","糖玩总动员旗舰店","悟空互助游","starsplastic旗舰店","天自然家庭农场","默小鱼儿","快乐高尔夫2009","童嘉嘉好练字","tb214842_33","globemilk荷高旗舰店","espritping","艾菲益智玩具舰旗店","南峰旗舰店","小真真258115","赐福堂电器专营店","limeizhi2009","美画美家生活馆","沙洛尔运动旗舰店","orange_design","宜霖服饰专营店","爱尔育尔母婴旗舰店","何处而不自得","悠闲华果","linku518","乖乖雪er_","青青货架","淘淘服装企业店","洁太旗舰店","首尔lady","竹林枫911125","igoccc","唯你旗舰店","蒙绿娃旗舰店","帝国家居旗舰店","爱只为你存在00","小一峰童装旗舰店","英雄煮","t7运动旗舰店","克普瑞丝娜旗舰店","wzl6032wzl77","豪比狼旗舰店","hong870714","悦客工厂店","优美妮旗舰店","zxc8858asd","wjeunn8","小面团_er","chao521013","金仕达食品专营店","飞利浦勇盛剑祥专卖店","gej2258","yuzhiqu旗舰店","朴舍家居公司","硕果包装","壹衫旗舰店","御尚堂生活电器旗舰店","冠标户外旗舰店","美七食品有限公司","梦飞扬家居建材","蒙娜丝旗舰店","啊呀呀潮品屋","洛瑞汽车用品","绝世大淘王","cxjmlj","8811zhuzhu","马寅威","娇江南","佩美诗时尚","潘小丫女鞋","琅翠zippo专营店","疆艺品旗舰店","宇艺格尔旗舰店","瑰根旗舰店","嗨妈咪o","mark是","爱珠母婴专营店","nisi耐司旗舰店","须臾顿悟","英仑风情","野蛮生长2","tb_0916126","lushijie1991","mahongsheng201314","scenekid数码旗舰店","张雅军01","weier旗舰店","泳不放弃90","程子伟轩","尚优潮流专柜","a814434634","依千琪睡衣家居服","greenmaple旗舰店","zerojeas旗舰店","fangyu689","阿曼达美丽岛","jiaxin06211","zhpc0258","qwer22778","三个爱55","chenhuahezuo","v小豆v","furnitureclinic旗舰店","火束车品旗舰店","墨香久久图书专营店","诚信经营0011","雅阁家居旗舰店","快乐蚂蚁旗舰店","ounclothing","雪见草璐","福鼎市品定之茶叶有限公司","佳雨洁具有限公司","陈梦yi666","北京学海轩图书专营店","tb2565984_2012","施耐德学捷专卖店","蓝色平原","foreverlovehaohao","三胖蛋创酷专卖店","缤纷世界li","初语折扣店","一直很安静mmhj","0夏天的橄榄枝0","pouch旗舰店","恒健达科技","刀刀5555","yuyayyy","peak匹克闽中启专卖店","梵羽熙旗舰店","金山百货商城","天空之美3","麦苗网络技术","羽莎啦旗舰店","元本良厂旗舰店","33爱在心里","老板欧奕专卖店","liu1182898730","hyf4tiancai","农民进口","tx男装","丘比酷旗舰店","oimaster旗舰店","蓝色的mint","525j我爱我家网","525j装饰旗舰店","genxinli123","skadi箱包旗舰店","朱浩珲","wby2xy","东莞家宝","温国雄88","艾藤直营店","item艾藤旗舰店","hkshomme旗舰店","春虫虫oo","chinasxjy","花常红","首席釹琯","锋少天野","秦汉阁旗舰店","商道维新数码专营店","味美乐","emmanuel609","久久达雷洛专卖店","乐修侠","信泰德服饰专营店","韩都风尚男装专营店","yifu12349","圣亚0356","美哈旗舰店","夕颜服饰专营店","米洛薇旗舰店","欧阳闹闹2206","nba华尔专卖店","初心旗舰店","百加莱企业","惊束旗舰店","迷恋你的笑","鸿源兴业旗舰店","源泉家居旗舰店","chenqiliang_0760","黄花菜豆小黄花","杰朴森旗舰店","凯旋达通数码专营店","溪美箱包专营店","z245892307","x至诚数码","wachar","欣然家居生活馆","韩若拉旗舰店","sleaf旗舰店","迈峰昌明专卖店","米先生旗舰店","光痕家居旗舰店","翔云在线","dgfynet","佳尔美家纺旗舰店","忽略55","杰霸服饰专营店","xxzzee","amazing骚骚","e街收藏","金域通酒类专营店","台州精车数控刀具","联想天晴东方专卖店","那木村旗舰店","letitbe旗舰店","岂止美旗舰店","沃滤汽车用品旗舰店","麦夕服饰旗舰店","red水蜜桃","诗丹娜品牌店","郭俸君","遇上闺蜜","鹏叶旗舰店","dushan368","爱立普数码专营店","鹏翔家居旗舰店","喜盈盈旗舰店","辰普旗舰店","日韩潮流部落","衣蓓姿旗舰店","mbox饰品旗舰店","弼马翁车品旗舰店","邱琪茵","ttkm123","潮韵轩旗舰店","宝尼baby","穿越不断","丰范家居旗舰店","迷你屋睡帐","奇缘爱恋旗舰店","飞利浦那波里专卖店","迷死衣路","pimio学捷专卖店","首富然然","峪momo","恒亨旗舰店","如意珠宝玉坊","追尚索胜专卖店","飞利浦斯雷康专卖店","倔强也是一种坚强","胖大帅旗舰店","hisense海信网盈专卖店","乡村高尔夫户外专营店"]
    for nick in nick_list:
        try:
            rpt_list = ZuanshiCategoryRptsGet.get_category_rpts(nick, sdate, sdate)
        except Exception,e:
            continue
        print nick
        try_list = DmpCrowdsGet.get_dmp_crowds(nick)
    import pdb; pdb.set_trace()  # XXX BREAKPOINT
    print try_list
