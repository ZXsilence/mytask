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
            
            score1 = 0
            for word in keyword1:
                if not word or word.isalnum():
                    continue
                if  word in word_set:
                    score1 += 1
            score2 = 0
            for word in keyword2:
                if not word or word.isalnum():
                    continue
                if  word in word_set:
                    score2 += 1

            keyword = keyword1 if score2 > score1 else keyword2

        except Exception,e:
            keyword = ''
        
        return keyword

