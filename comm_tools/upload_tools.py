#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: dongxuanliang
@contact: dongxuanliang@maimiaotech.com
@date: 2015-02-25 15:44
@version: 2015
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import os

def upload_file(file_obj,root_path,category,mode=None,with_scp=False):
    """
    file_obj: 文件对象
    root_paht：上传根目录
    category：文件类型
    mode：文件目录索引方式，按天索引或者按其他方式索引（目前未实现,默认不索引）
    with_scp：scp到静态资源服务器
    整个文件的绝对路径为:root+category+'/'+mode_path+file_name
    """
    #创建文件路径
    file_name = file_obj.name
    mode_path=''
    ext_path= category + '/' + mode_path
    package_path = root_path + ext_path
    if not os.path.exists(package_path):
        os.makedirs(package_path)
    abs_file_path = package_path + file_name
    #保存文件
    fw = open(abs_file_path,'wb+')
    for chunk in file_obj.chunks():
        fw.write(chunk)
    fw.close()
    relative_file_path = ext_path + file_name
    #scp到精通资源服务器
    if with_scp:
        print "================"
    return relative_file_path
