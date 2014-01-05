#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from PolySpider.config import Config
from PolySpider.util import SqliteUtil
import sqlite3

def get_app_detail_by_item(item):
    con = sqlite3.connect(Config.SQLITE_PATH)
    cur = con.cursor()
    print item['app_id']
    sql = "select * from ps_app_detail where app_id = ? and version = ? and platform = ?"
    cur.execute(sql,(item['app_id'], item['version'], item['platform']))
    return cur.fetchall()

def insert_app_detail(item):
    #��������
    print '���ݿ�ps_app_detail��������'
    sql = '''INSERT INTO ps_app_detail values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    data = [(
         item['app_id'],
         item['version'],
         item['platform'],
         item['apk_url'],
         item['apk_size'],
         item['pakage_name'],
         item['cover'],
         item['rating_point'],
         item['rating_count'],
         item['android_version'],
         item['download_times'],
         item['description'],
         item['imgs_url'],
         item['last_update'],)]
    SqliteUtil.save(sql, data)