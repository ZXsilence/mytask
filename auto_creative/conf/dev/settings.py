#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zhoujiebin
@contact: garcia.wul@alibaba-inc.com
@date: 2012-09-04 13:28
@version: 0.0.0
@license: Copyright alibaba-inc.com
@copyright: Copyright alibaba-inc.com

"""
import os
import sys

currDir = os.path.normpath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(currDir,os.path.pardir))
PROJECT_PAR = os.path.normpath(os.path.join(PROJECT_ROOT, os.path.pardir))
SEGMENT_PATH = os.path.normpath(os.path.join(currDir, '../segment/'))
    
sys.path.insert(0,SEGMENT_PATH)
sys.path.insert(0,PROJECT_PAR)

'禁用词文件'
ban_path = {'sick_terms':os.path.join(currDir, './filter_terms/sick_terms'),\
        'channel_terms': os.path.join(currDir, './filter_terms/channel_terms'),\
        'brand_terms': os.path.join(currDir, './filter_terms/brand_terms'),\
        }

sys.path.append(os.path.join(currDir, '../segment/'))
from word_segment import WordSegment
segmenter = WordSegment()

