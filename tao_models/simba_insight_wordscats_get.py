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
 
from TaobaoSdk import SimbaInsightWordscatsGetRequest 
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception

class SimbaInsightWordscatsGet(object):
    MAX_NUM = 200

    @classmethod
    @tao_api_exception(5)
    def _get_words_cats(cls, access_token, nick, word_cats, filter):
        """
        get words cats 
        """
        req = SimbaInsightWordscatsGetRequest()
        #req.nick = nick
        req.word_categories = word_cats
        req.filter = filter 

        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.in_word_categories

    @classmethod
    def get_words_cats_pv(cls, access_token, nick, wordscats):
        """
        wordscats 应该是小写，简体，半角字符串，而且每个word不能包含逗号和^号
        example wordscats = [mp3^^1512, mp4^^1512, 手机^^50905]
        """
        wordscats_str = ','.join(wordscats)
        in_word_categories = SimbaInsightWordscatsGet._get_words_cats(access_token, nick, wordscats_str, 'pv')
        wordscats_pv = []
        for in_word_category in in_word_categories:
            wordscats_pv.append(in_word_category.toDict())
        return wordscats_pv 

    @classmethod
    def get_words_cats(cls, access_token, word_list, cats_list):
        """
        """
        wordcats = []
        for i in range(len(word_list)):
            for cat in cats_list[i]:
                wordcats.append(str(word_list[i])+'^^'+str(cat))

        wordscats_info = {}
        while wordcats != []:
            subwordcats = wordcats[:cls.MAX_NUM]
            wordcats = wordcats[cls.MAX_NUM:]
            subwordcats_str = ','.join(subwordcats)
            in_word_categories = SimbaInsightWordscatsGet._get_words_cats(
                access_token, '', subwordcats_str, 'PV|CLICK|AVGCPC|COMPETITION|CTR')
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
        return catinfos_list 
     
if __name__ == '__main__':
    access_token = '620260146ZZc0465e1b4185f7b4ca8ba1c7736c28d1c675871727117' 
    
    wordscats_info = SimbaInsightWordscatsGet.get_words_cats(access_token, ['手机','婚庆床品红'], [[1512,1513],[50008824,1512]])
    for wordscats in wordscats_info:
        print wordscats
