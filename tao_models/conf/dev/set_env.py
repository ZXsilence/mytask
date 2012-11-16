#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Li Yangmin
@contact: liyangmin@maimiaotech.com
@date: 2012-11-16 13:47
@version: 0.0.0
@license: Copyright maimiaotech.com
@copyright: Copyright maimiaotech.com

"""
import os
import sys

currDir = os.path.normpath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(currDir,os.path.pardir))
PROJECT_PAR = os.path.normpath(os.path.join(PROJECT_ROOT, os.path.pardir))
PYTHON_SDK = os.path.normpath(os.path.join(currDir, '../../../TaobaoOpenPythonSDK/'))
    
def getEnvReady():
    sys.path.insert(0,PYTHON_SDK)
    sys.path.insert(0,PROJECT_ROOT)

