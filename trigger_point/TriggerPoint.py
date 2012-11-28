#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Chen Ke
@contact: chenke@MaimiaoTech.com
@date: 2012-06-26 10:28
@version: 0.0.0
@license: Copyright MaimiaoTech.com
@copyright: Copyright MaimiaoTech.com

"""
import os
import sys
import string
import mimetypes
import cStringIO as StringIO
import platform
import copy

curr_path = os.path.dirname(__file__)
sys.path.append(os.path.join(curr_path, '../word_segment/'))

ATTRIBUTE_VALUE_SEGMENT_THRESHOLD = 4

from enums import TriggerPointType
from word_segment import WordSegment

class TriggerPointGenerator(object):

    def __init__(self): 
        self.segmenter = WordSegment()

    def make_trigger_point(self, attribute):
        #transform value, "是,否,不...etc"
        if len(attribute['attribute_value']) >= ATTRIBUTE_VALUE_SEGMENT_THRESHOLD:

            word_list = self.segmenter.do_segment(attribute['attribute_value'])
        else:
            word_list = [attribute['attribute_value']]

        attribute['trigger_point_list'] = []
        for word in word_list:
            #filter single words
            if len(word) == 1:
                continue
            #filter nosense word, "其他,\/!@#$%^&*()_...etc",
            attribute['trigger_point_list'].append({'type':TriggerPointType.DEFAULT, 'trigger_point':word})

    def attribute_trigger_point(self, attributeList):
        attributeList = copy.deepcopy(attributeList)
        for attribute in attributeList:
            self.make_trigger_point(attribute)

        return attributeList
