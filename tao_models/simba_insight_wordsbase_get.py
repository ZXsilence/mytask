#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import copy
import datetime
import logging
import traceback

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')
 
from TaobaoSdk import SimbaInsightWordsbaseGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

def get_avg(array):
    sum = 0
    for a in array:
        sum = sum + a
    return sum/len(array)

def get_week_data_hash_array(pv_array, click_array, competition_array, compare_days, day, pv_threshold = 5, total_days = 7):
    week_data_hash_array=[]
    for i in xrange(total_days - compare_days + 1):
        real_day = day - datetime.timedelta(days=i)
        local_pv_array = pv_array[i:i+compare_days]
        local_click_array = click_array[i:i+compare_days]
        local_competition_array = competition_array[i:i+compare_days]
        local_pv = get_avg(local_pv_array)
        if local_pv <= pv_threshold:
            week_data_hash_item = 0
        else:
            week_data_hash_item = hash(str(real_day) + str(local_pv_array) + str(local_click_array) + str(local_competition_array))
        week_data_hash_array.append(week_data_hash_item)
    return change_obj_to_dict_deeply(week_data_hash_array)

def is_same(list1, list2):
    if len(list1) != len(list2):
        return False
    for i in xrange(len(list1)):
        if list1[i] != list2[i]:
            return False
    return True

def check_words_same(item):
    same = 0
    if item['pv'] < 5:
        return same
    if is_same(item['pv_array'], item['click_array']):
        same = same + 1
        logger.info("comm_lib pv == click " + item['word'] + " " + str(id(item['pv_array'])) + " " + str(id(item['click_array'])))
    if is_same(item['click_array'], item['competition_array']):
        same = same + 1
        logger.info("comm_lib click == competition " + item['word'] + " " + str(id(item['click_array'])) + " " + str(id(item['competition_array'])))
    if is_same(item['competition_array'], item['pv_array']):
        same = same + 1
        logger.info("comm_lib competition == pv " + item['word'] + " " + str(id(item['competition_array'])) + " " + str(id(item['pv_array'])))
    if same > 0:
        error_msg=traceback.format_exc()
        logger.info("bad data %s", error_msg)
    return same

class SimbaInsightWordsbaseGet(object):
    
    MAX_WORDS = 170

    @classmethod
    @tao_api_exception(5)
    def _get_words_base(cls, time, word_list,nick=None):
        '''get words base'''
        req = SimbaInsightWordsbaseGetRequest()
        req.time = time
        req.words = ','.join(word_list)
        req.filter = 'PV|CLICK|AVGCPC|COMPETITION'
        if nick:
            req.nick = nick
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.in_word_bases

    @classmethod
    def get_words_base(cls, time, word_list,nick=None):
        """
        get words base 
        """
        word_list = copy.deepcopy(word_list)
        total_list = []
       
        while word_list:
            sub_word_list = word_list[:cls.MAX_WORDS]
            word_list = word_list[cls.MAX_WORDS:]
            sub_list = cls._get_words_base(time, sub_word_list,nick)
            total_list.extend(sub_list)

        return change_obj_to_dict_deeply(total_list)

    @classmethod
    def get_words_base_one_week_avg(cls, words_list,nick=None):
        'words_list 应该是小写，简体，半角字符串，而且每个word不应该包含逗号'
        in_word_bases = SimbaInsightWordsbaseGet.get_words_base('WEEK', words_list,nick)
        word_info_list = []
        for word_base in in_word_bases:
            word = word_base['word']
            in_record_base_list = word_base['in_record_base_list']
            word_info = {}
            word_info['word'] = word
            word_info['pv'] = 0
            word_info['click'] = 0
            word_info['competition'] = 0
            cost = 0
            for day_info in in_record_base_list:
                word_info['pv'] += day_info['pv']
                word_info['click'] += day_info['click']
                word_info['competition'] += day_info['competition']
                cost += (day_info.avg_price*day_info['click'])

            word_info['avg_price'] = cost/(word_info['click']+0.0000001) 
            word_info['pv'] /= 7.0
            word_info['click'] /= 7.0
            word_info['competition'] /= 7.0

            word_info_list.append(word_info)

        return change_obj_to_dict_deeply(word_info_list)

    @classmethod
    def get_words_base_one_week_avg_accurate(cls, words_list, compare_days=5, pv_threshold=5, time = 'WEEK',nick=None):
        'words_list 应该是小写，简体，半角字符串，而且每个word不应该包含逗号'
        in_word_bases = SimbaInsightWordsbaseGet._get_words_base(time, words_list,nick)
        word_info_list = []
        total_days = 0
        if time == 'WEEK':
            total_days = 7.0
        else: #time == 'MONTH':
            total_days = 30.0
        for word_base in in_word_bases:
            word = word_base.word
            in_record_base_list = word_base.in_record_base_list
            word_info = {}
            word_info['word'] = word
            word_info['pv'] = 0
            word_info['click'] = 0
            word_info['competition'] = 0
            pv_array = []
            click_array = []
            competition_array = []
            cost = 0
            for day_info in in_record_base_list:
                word_info['pv'] += day_info.pv
                word_info['click'] += day_info.click
                word_info['competition'] += day_info.competition
                cost += (day_info.avg_price*day_info.click)
                pv_array.append(day_info.pv)
                click_array.append(day_info.click)
                competition_array.append(day_info.competition)
            word_info['week_data_hash'] = hash(str(pv_array) + str(click_array) + str(competition_array))
            word_info['pv_array'] = pv_array
            word_info['click_array'] = click_array
            word_info['competition_array'] = competition_array
            #now = datetime.datetime.now()
            #word_info['week_data_date'] = now
            word_info['week_last_date'] = in_record_base_list[0].date
            end_date = datetime.datetime.now() - datetime.timedelta(0, 3600*24*3)
            #if in_record_base_list[0].date < end_date:
            #    for i in xrange(len(in_record_base_list)):
            #        logger.info("old_date %s : %s", str(in_record_base_list[i].date), word_info['word'])
            word_info['avg_price'] = cost/(word_info['click']+0.0000001) 
            word_info['pv'] /= total_days
            word_info['click'] /= total_days
            word_info['competition'] /= total_days
            if time == 'WEEK':
                word_info['week_data_hash_array'] = get_week_data_hash_array(pv_array, click_array, competition_array, compare_days, word_info['week_last_date'], pv_threshold)
            #if check_words_same(word_info) > 0 :
            #    logger.info("error in SimbaInsightWordsbaseGet")
            word_info_list.append(word_info)

        return change_obj_to_dict_deeply(word_info_list)

if __name__ == '__main__':
    nick = None
    words_list = ['nifeifie登山鞋','冲锋衣','登山包','户外鞋','徒步鞋', '夏天 男鞋', '夏季 男鞋', '夏 男鞋', '夏款 男鞋', '男 皮鞋', '男人 皮鞋', '男款 皮鞋', '男式 皮鞋', '男士 皮鞋', '男装 皮鞋']
    print SimbaInsightWordsbaseGet.get_words_base_one_week_avg_accurate(words_list)
    word_info_list = SimbaInsightWordsbaseGet.get_words_base('DAY',words_list,nick) 
    print 'word_info_list', word_info_list
    for word_info in word_info_list:
        print "==================="
        print word_info['word']
        for x in word_info['in_record_base_list']:
            print x
            print x['date'], x['pv']
    week_data_hash_array = get_week_data_hash_array([1,2,3,4,5,6,7], [1,2,3,4,5,6,7], [1,2,3,4,5,6,7], 2, datetime.datetime.now())
    for item in week_data_hash_array:
        print "hash " + str(item)
    print "============================="
    week_data_hash_array = get_week_data_hash_array([1,1,1,2,2,2,2], [1,1,1,2,2,2,2], [1,1,1,2,2,2,2], 2, datetime.datetime.now())
    for item in week_data_hash_array:
        print "hash " + str(item)
