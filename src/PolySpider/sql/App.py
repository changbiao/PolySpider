#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from PolySpider.config import Config
from PolySpider.util import SqliteUtil
import sqlite3

def get_app_by_app_name(app_name):
    con = sqlite3.connect(Config.SQLITE_PATH)
    cur = con.cursor()
    sql = "select * from ps_app where app_name = ?"
    cur.execute(sql,(app_name,))
    return cur.fetchall()

def insert_app(item):
    #��������
    print '���ݿ�ps_app��������'
    sql = '''INSERT INTO ps_app values(null,?,?,?)'''
    data = (item['app_name'], item['author'], item['category'])
    result = SqliteUtil.save_return_id(sql, data)
    print result
    return result

def update_app_author(id, author):
    #��������
    print "���ݿ��������"
    sql = '''UPDATE ps_app set author = ? where id = ?'''
    data = [(author, id)]
    SqliteUtil.update(sql, data)

def update_app_category(id, category):
    #��������
    print "���ݿ��������"
    sql = '''UPDATE ps_app set category = ? where id = ?'''
    data = [(category, id)]
    SqliteUtil.update(sql, data)
