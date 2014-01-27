#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import copy

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('api_test')
 
from TaobaoSdk import SimbaInsightWordscatsGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

class SimbaInsightWordscatsGet(object):
    
    MAX_NUM = 200

    @classmethod
    @tao_api_exception(5)
    def _get_words_cats(cls, word_cats, filter,nick=None):
        """
        get words cats 
        """
        req = SimbaInsightWordscatsGetRequest()
        if nick:
            req.nick = nick
        req.word_categories = word_cats
        req.filter = filter 
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.in_word_categories

    @classmethod
    def get_words_cats_pv(cls, wordscats,nick=None):
        """
        wordscats 应该是小写，简体，半角字符串，而且每个word不能包含逗号和^号
        example wordscats = [mp3^^1512, mp4^^1512, 手机^^50905]
        """
        wordscats_str = ','.join(wordscats)
        in_word_categories = SimbaInsightWordscatsGet._get_words_cats(wordscats_str, 'pv',nick)
        wordscats_pv = []
        for in_word_category in in_word_categories:
            wordscats_pv.append(in_word_category.toDict())
        return change_obj_to_dict_deeply(wordscats_pv)

    @classmethod
    def get_words_cats(cls, word_list, cats_list,nick=None):
        wordcats = []
        for i in range(len(word_list)):
            for cat in cats_list[i]:
                wordcats.append(str(word_list[i])+'^^'+str(cat))
        wordscats_info = {}
        while wordcats != []:
            subwordcats = wordcats[:cls.MAX_NUM]
            wordcats = wordcats[cls.MAX_NUM:]
            subwordcats_str = ','.join(subwordcats)
            in_word_categories = SimbaInsightWordscatsGet._get_words_cats(subwordcats_str, 'PV|CLICK|AVGCPC|COMPETITION|CTR')
            for in_word_category in in_word_categories:
                in_word_category_dict = in_word_category.toDict()
                if in_word_category_dict.has_key('word') and in_word_category_dict.has_key('category_id'):
                    key = in_word_category_dict['word'] + '^^' + str(in_word_category_dict['category_id'])
                    wordscats_info[key] = in_word_category_dict
        
        catinfos_list = []
        for i in range(len(word_list)):
            catinfos = []
            for cat in cats_list[i]:
                key = unicode(word_list[i])+'^^'+str(cat)
                if wordscats_info.has_key(key):
                    catinfos.append(wordscats_info[key])
                else:
                    catinfos.append({})
            catinfos_list.append(catinfos)
        return change_obj_to_dict_deeply(catinfos_list)
     
if __name__ == '__main__':
    nick = 'chinchinstyle'
    wordscats_info = SimbaInsightWordscatsGet.get_words_cats(['手机','婚庆床品红'], [[1512,1513],[50008824,1512]],nick)
    for wordscats in wordscats_info:
        print wordscats

