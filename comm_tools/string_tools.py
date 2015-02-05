#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumc
@contact: liumingchao@maimiaotech.com
@date: 2014-06-09 14:27
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import sys
import os

class StringTools(object):
    
    @classmethod
    def load_word_set(cls):
        currDir = os.path.normpath(os.path.dirname(__file__))
        stop_file = os.path.join(currDir, '../../Algorithm/BidwordExtend/data/stop_words')
        word_file = os.path.join(currDir, '../../Algorithm/BidwordExtend/data/word_hash')

        stop_data = file(stop_file).read().split('\n')
        word_data = file(word_file).read().split('\n')
        word_set = [w.decode('utf-8') for w in stop_data]
        
        for line in word_data:
            line_data = line.split('\t')
            word = line_data[0]
            if type(word) == str:
                try:
                    word = word.decode('utf-8')
                except Exception:
                    pass
            word_set.append(word)

        return set(word_set)

    @classmethod
    def keyword_decode(cls, keyword_str, word_set):
        try:
            try:
                keyword1 = keyword_str.decode('gbk')
            except Exception,e:
                keyword1 = keyword_str.decode('utf-8')

            try:
                keyword2 = keyword_str.decode('utf-8')
            except Exception,e:
                keyword2 = keyword_str.decode('gbk')
            
            if keyword1 == keyword2:
                return keyword1

            score1 = 0
            for word in keyword1:
                if not word or word.isdigit():
                    score1 += 1
                elif  word in word_set:
                    score1 += 1
            score2 = 0
            for word in keyword2:
                if not word or word.isdigit():
                    score2 += 1
                elif  word in word_set:
                    score2 += 1
            
            score1 = float(score1) / len(keyword1)
            score2 = float(score2) / len(keyword2)
            keyword = keyword2 if score2 > score1 else keyword1
            #if score1 == 0 and score2 == 0:
            #    keyword = keyword2

        except Exception,e:
            keyword = ''
        
        return keyword

