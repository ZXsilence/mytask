#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import copy

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12651461', '80a15051c411f9ca52d664ebde46a9da')
 
from TaobaoSdk import SimbaInsightCatsforecastGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

class SpecialWord():
    word_list_a = [u'大方', u'说法', u'pv', u'的', u'视频']
    word_list_b = [u'大方', u'说话', u'pv', u'的', u'画面']

    @classmethod
    def _perm(cls, list, depth, result):
        if depth == len(list):
            word = ''
            for item in list:
                word += item
            result.append(word)
        else:
            for i in range(depth, len(list)):
                list[i], list[depth] = list[depth], list[i]
                SpecialWord._perm(list, depth + 1, result)
                list[i], list[depth] = list[depth], list[i]

    @classmethod
    def __init__(cls):
        special_word_list = []
        SpecialWord._perm(cls.word_list_a, 0, special_word_list)
        cls.special_word_list_a = special_word_list
        special_word_list = []
        SpecialWord._perm(cls.word_list_b, 0, special_word_list)
        cls.special_word_list_b = special_word_list
        
        cls.count = 0

    def get_curr_special_word_list(cls):
        cls.count += 1
        if cls.count % 2 == 0:
            return cls.special_word_list_a
        else:
            return cls.special_word_list_b


class SimbaInsightCatsforecastGet(object):
    s = SpecialWord()
    special_word_list = s.get_curr_special_word_list()
    print len(special_word_list)

    @classmethod
    def switch_special_word_list(cls, ):
        """
        switch_special_word_list
        """
        cls.special_word_list = cls.s.get_curr_special_word_list()


    @classmethod
    @tao_api_exception(5)
    def _get_words_cat_forecast(cls, access_token, words):
        """
        get words cat forecast 
        """
        req = SimbaInsightCatsforecastGetRequest()
        req.words = words

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.in_category_tops

    @classmethod
    def _get_words_cat_forecast_object(cls, access_token, words_list):
        'words_list 应该是小写，简体，半角字符串，而且每个word不应该包含逗号'
        words_str = ','.join(words_list)
        in_category_tops = SimbaInsightCatsforecastGet._get_words_cat_forecast(access_token, words_str)
        if not in_category_tops:
            return [None  for i in range(len(words_list))]

        if len(in_category_tops) == len(words_list):
            return in_category_tops
        if len(words_list) == 1 and len(in_category_tops) != 1:
            return [None]
        
        middle = len(words_list)/2
        words_list_half_p = words_list[0:middle]
        words_list_half_b = words_list[middle:len(words_list)]

        in_category_tops_p = SimbaInsightCatsforecastGet._get_words_cat_forecast_object(access_token, words_list_half_p)
        in_category_tops_b = SimbaInsightCatsforecastGet._get_words_cat_forecast_object(access_token, words_list_half_b)
        
        in_category_tops = []
        in_category_tops.extend(in_category_tops_p)
        in_category_tops.extend(in_category_tops_b)
        return in_category_tops


    @classmethod
    def get_words_cat_forecast_1(cls, access_token, words_list):
        in_category_tops = SimbaInsightCatsforecastGet._get_words_cat_forecast_object(access_token, words_list)
        cat_forecast_list = []
        for i_n_category_top in in_category_tops:
            word_cat_forecast_list = []
            try:
                if i_n_category_top:
                    for element in i_n_category_top.category_child_top_list:
                        word_cat_forecast_list.append(element.category_id)
            except Exception, data:
                pass
            cat_forecast_list.append(word_cat_forecast_list)

        return cat_forecast_list 

    @classmethod
    def get_words_cat_forecast_2(cls, access_token, words_list):
        'words_list 应该是小写，简体，半角字符串，而且每个word不应该包含逗号, 数组不小于50'
        #if len(words_list) < 50:
        #    return None 

        words_list_tmp = []
        for i in range(len(words_list)):
            words_list_tmp.append(words_list[i])
            words_list_tmp.append(cls.special_word_list[i])

        words_str = ','.join(words_list_tmp)
        in_category_tops = SimbaInsightCatsforecastGet._get_words_cat_forecast(access_token, words_str)

        raw_cat_forecast_list = []
        for i_n_category_top in in_category_tops:
            word_cat_forecast_list = []
            if i_n_category_top:
                i_n_category_top_dict = i_n_category_top.toDict()
                if i_n_category_top_dict.has_key('category_child_top_list'):
                    for element in i_n_category_top_dict['category_child_top_list']:
                        word_cat_forecast_list.append(element.category_id)
            raw_cat_forecast_list.append(word_cat_forecast_list)

        special_word_cat_info = []
        for i in range(len(raw_cat_forecast_list)):
            if raw_cat_forecast_list.count(raw_cat_forecast_list[i]) == len(words_list):
                special_word_cat_info = raw_cat_forecast_list[i]
                break
        
        print special_word_cat_info

        cat_forecast_list = []
        for i in range(len(raw_cat_forecast_list)):
            if raw_cat_forecast_list[i] == special_word_cat_info:
                if i == 0:
                    cat_forecast_list.append([])
                elif raw_cat_forecast_list[i-1] == special_word_cat_info:
                    cat_forecast_list.append([])
                else:
                    cat_forecast_list.append(raw_cat_forecast_list[i-1])
        
        return cat_forecast_list 

    @classmethod
    def get_words_cat_forecast_3(cls, access_token, words_list_in):
        'words_list 应该是小写，简体，半角字符串，而且每个word不应该包含逗号, 数组不小于50'
        words_list = []
        for word in words_list_in:
            if type(word) == type(''):
                word = word.decode('utf8')
            word = word.lower()
            words_list.append(word)

        words_list_tmp = []
        for i in range(len(words_list)):
            words_list_tmp.append(words_list[i])
            words_list_tmp.append(cls.special_word_list[i])

        words_str = ','.join(words_list_tmp)
        in_category_tops = SimbaInsightCatsforecastGet._get_words_cat_forecast(access_token, words_str)

        cat_forecast_list = []
        cat_forecast_dict = {}
        for i_n_category_top in in_category_tops:
            word_cat_forecast_list = []
            categroy_word = i_n_category_top.categroy_word
            if i_n_category_top:
                i_n_category_top_dict = i_n_category_top.toDict()
                if i_n_category_top_dict.has_key('category_child_top_list'):
                    for element in i_n_category_top_dict['category_child_top_list']:
                        word_cat_forecast_list.append(element.category_id)
            cat_forecast_dict[categroy_word] = word_cat_forecast_list

        for word in words_list:
            cat_forecast_list.append(cat_forecast_dict.get(word, []))

        return cat_forecast_list 

if __name__ == '__main__':
    access_token = '620260146ZZc0465e1b4185f7b4ca8ba1c7736c28d1c675871727117' 
    words = ['Mp3', 'mp4播放器', '手机', '减肥茶', 'mp5', '播放器mp4', '手机电池', '电池手机', '新款女装连衣裙笔记本', '你好']
    #words = ['Mp3']
    #cat_forecast_list  = SimbaInsightCatsforecastGet.get_words_cat_forecast_1(access_token, words)
    #for i in range(len(words)):
    #    print words[i], cat_forecast_list[i]

    cat_forecast_list = SimbaInsightCatsforecastGet.get_words_cat_forecast_2(access_token, words) 
    for i in range(len(words)):
        print words[i], cat_forecast_list[i]
    print "============="
    cat_forecast_list = SimbaInsightCatsforecastGet.get_words_cat_forecast_3(access_token, words) 
    for i in range(len(words)):
        print words[i], cat_forecast_list[i]
