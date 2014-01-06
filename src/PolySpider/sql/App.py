#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import sqlite3

from PolySpider.config import Config
from PolySpider.util import SqliteUtil
from PolySpider.util import CategoryUtil
def get_app_by_app_name(app_name):
    print SqliteUtil.is_table_exist("ps_app")
    con = sqlite3.connect(Config.SQLITE_PATH)
    cur = con.cursor()
    sql = "select * from ps_app where app_name = ?"
    cur.execute(sql,(app_name,))
    return cur.fetchall()

def get_app_by_id(id):
    print SqliteUtil.is_table_exist("ps_app")
    con = sqlite3.connect(Config.SQLITE_PATH)
    cur = con.cursor()
    sql = "select * from ps_app where id = ?"
    cur.execute(sql,(id,))
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
def search_app_category(id):
    #����ĳ��app�ķ���
    con = sqlite3.connect(Config.SQLITE_PATH)
    cur = con.cursor()
    sql = "select category from ps_app where id= ?"
    cur.execute(sql,(id,))
    
    
    return cur.fetchall()
def count_app_categroy_sum():
    #ĳ��������app������
    sql = '''select category from ps_app '''
    count_categorys={}
    count_categorys['1000']=0
    con = sqlite3.connect(Config.SQLITE_PATH)
    cur = con.cursor()
    cur.execute(sql)
    categorys =cur.fetchall()
    for category in categorys:
        
        for temp in category[0].split(','):
            app_category = temp.split(':')[0]
            if app_category!='':
                if not count_categorys.get(app_category):
                    count_categorys[app_category]=1
                else:
                    count_categorys[app_category]=int(count_categorys[app_category])+1
            else:
                count_categorys['1000']=count_categorys['1000']+1
    data="["
    for count_category in count_categorys:
        data=data+'["'+unicode(str(CategoryUtil.DISCATEGORY.get(count_category)))+'",'+str(count_categorys[count_category])+"],"
    data=data[:-1]+"]"
    print data
    return data
            
            
def get_app_list(page_index,row_number,sort,order):
    #Ӧ���б�
    #page_index����ҳ�� row_number��ʾ����sort��ĳ��������order������
    con = sqlite3.connect(Config.SQLITE_PATH)
    cur = con.cursor()
    sql='''select * from ps_app order by ? limit ? offset ?'''
    startnum=(int(page_index)-1)*int(row_number)
    temp = sort+' '+order
    cur.execute(sql,(temp,row_number,startnum,))
    
    return cur.fetchall()

