#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import os
import sys
if sys.path[-1].split("\\")[-1] != "src": 
    c_path = os.getcwd()
    sys.path.append(c_path[:c_path.rfind("\\")])
    
#Sqlite3 Configuration
SQLITE_PATH = sys.path[-1] + "\\" + "app.db"
SHOW_SQL = False #True����ڿ���̨��ʾ��ϸ��SQL��ѯ

#App Star Constant
APPSTAR_MAX_APPS = 30000

#BaiduYun AK && SK
'''������Ҫ��дBaiYun�Ĺ�ԿAK��˽ԿSK��Bucket'''
BAIDU_AK = ''
BAIDU_SK = ''
BAIDU_BUCKET = ''

#UpYun
'''������Ҫ��д��������������������Ӧ��bucket���û���������'''
UPYUN_USERNAME = ''
UPYUN_PASSWORD = ''
UPYUN_BUCKET = ''