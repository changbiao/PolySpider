#!/usr/bin/env python
#coding:gbk

import sqlite3
import os
from PolySpider import Config

def check_sql(sql):
    if not sql or sql == '': 
        print('the [{}] is empty or equal None!'.format(sql))
        return False
    else: return True

def get_conn(path):
    '''
    �������ݿ�����
    ���path���ڲ�����һ���ļ�·�����򴴽��ļ����ݿ�����
    ���򴴽��ڴ����ݿ�����
    '''
    return sqlite3.connect(path)
    
def get_cursor(conn):
    '''
    ��ȡ�α꣬���connΪ�գ����ȡ�ڴ��α�
    '''
    return conn.cursor() if conn else get_conn('').cursor()
    
def close_all(conn, cu):
    '''
    �ر����ݿ��α��������ݿ����Ӷ���
    '''
    try:
        if not cu: cu.close()
    finally:
        if conn: conn.close()

def is_table_exist(cur, table_name):
    return True if cur.execute("SELECT count(*) FROM sqlite_master WHERE type= 'table' and name = ? ",(table_name,)).fetchone()[0] > 0 else False

def create_table(conn, sql):
    '''
    �������ݿ��
    '''
    if not check_sql(sql): return
    cu = get_cursor(conn)
    if Config.SHOW_SQL: print('������\nִ��sql:[{}]'.format(sql))
    cu.execute(sql)
    conn.commit()
    print('�������ݿ��ɹ�!')
            
def drop_table(conn, table):
    '''��������,��ɾ����������д������ݵ�ʱ��ʹ�ø�
    ������ʱ��Ҫ���ã�'''
    if table is not None and table != '':
        sql = 'DROP TABLE IF EXISTS ' + table
        if Config.SHOW_SQL: print('ִ��sql:[{}]'.format(sql))
        cu = get_cursor(conn)
        cu.execute(sql)
        conn.commit()
        print('ɾ�����ݿ��[{}]�ɹ�!'.format(table))
        close_all(conn, cu)
    else:
        print('the [{}] is empty or equal None!'.format(sql))

def save_or_update(conn, sql, data):
    '''
    ��������
    dataΪҪ��������ݣ���ʽΪlist�����Դ�Ŷ�������
    '''
    if not check_sql(sql): return
    if not data: return
    cu = get_cursor(conn)
    for d in data:
        if Config.SHOW_SQL: print('������������\nִ��sql:[{}],����:[{}]'.format(sql, d))
        cu.execute(sql, d)
        conn.commit()
        
def delete(conn, sql, data):
    '''ɾ������'''
    if not check_sql(sql): return
    if not data: return
    cu = get_cursor(conn)
    for d in data:
        if Config.SHOW_SQL: print('ɾ������\nִ��sql:[{}],����:[{}]'.format(sql, d))
        cu.execute(sql, d)
        conn.commit()
        
def getItemByAppName(cur, app_name):
    sql = "select * from app_info where app_name = ?"
    cur.execute(sql,(app_name,))
    return cur.fetchall()
    
def fetchall(conn, sql, conditions):
    '''
    ��ѯ��������
    conditions��where����������
    '''
    if not check_sql(sql): return
    cu,cons = get_cursor(conn),(conditions,)
    cu.execute(sql, cons) if data else cu.execute(sql)
    if Config.SHOW_SQL: print('��ѯ��������\nִ��sql:[{}]'.format(sql,conditions))
    return cu.fetchall()

def checkAppInfoExist(conn):
    #��������ڣ��򴴽���
    cur = get_cursor(conn)
    if  not is_table_exist(cur, 'app_info'):
        sql_table_create = '''
            CREATE TABLE app_info(
            id INTEGER PRIMARY KEY,
            apk_url TEXT,
            pakage_name VARCHAR(32),
            app_name VARCHAR(32),
            cover VARCHAR(32),
            version VARCHAR(32),
            rating_star VARCHAR(32),
            rating_count VARCHAR(32),
            category VARCHAR(32),
            android_version VARCHAR(32),
            download_times VARCHAR(32),
            author VARCHAR(32),
            last_update TEXT,
            description TEXT,
            imgs_url TEXT,
            apk_size VARCHAR(32)
            )
        '''
        create_table(conn,sql_table_create)
