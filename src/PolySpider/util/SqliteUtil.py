#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from PolySpider.config import Config
import sqlite3

def check_sql(sql):
    '''
    ���sql����Ƿ�Ϊ��
    '''
    if not sql or sql == '': 
        print('the [{}] is empty or equal None!'.format(sql))
        return False
    else: return True
    
def is_table_exist(table_name):
    '''
    ���table_name�����ݿ���Ƿ����
    '''
    con = sqlite3.connect(Config.SQLITE_PATH)
    return True if con.cursor().execute("SELECT count(*) FROM sqlite_master WHERE type= 'table' and name = ? ",(table_name,)).fetchone()[0] > 0 else False

def checkTableExist():
    '''
    ������ݿ����Ƿ���ڱ�
    ������ݿ�����ps_app��ps_app_detail���򴴽���
    '''
    if not is_table_exist('ps_app'):
        sql_table_create = '''
            CREATE TABLE ps_app(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_name VARCHAR(32),
                author VARCHAR(32),
                category VARCHAR(32)
            );
        '''
        create_table(sql_table_create)
    if not is_table_exist('ps_app_detail'):
        sql_table_create = '''
            CREATE TABLE ps_app_detail(
                app_id INTEGER,
                version VARCHAR(32),
                platform VARCHAR(32),
                apk_url TEXT,
                apk_size VARCHAR(32),
                pakage_name VARCHAR(32),
                cover VARCHAR(32),
                rating_point VARCHAR(32),
                rating_count VARCHAR(32),
                android_version VARCHAR(32),
                download_times VARCHAR(32),
                description TEXT,
                imgs_url TEXT,
                last_update TEXT,
                primary key (app_id, version, platform)
            );
        '''
        create_table(sql_table_create)

def close_all(con):
    '''
    �ر����ݿ��α��������ݿ����Ӷ���
    '''
    try:
        if not con.cursor(): con.cursor().close()
    finally:
        if con: con.close()

def execute_sql(sql, data = ""):
    '''
    ִ��sql���
    dataĬ��Ϊ��,dataΪlist����ִ�ж������ݲ���
    '''
    con = sqlite3.connect(Config.SQLITE_PATH)
    if not check_sql(sql): return
    cur = con.cursor()
    if data == "":
        cur.execute(sql)
    else:
        for d in data:
            if Config.SHOW_SQL: print('ִ��sql:[{}],����:[{}]'.format(sql, d))
            cur.execute(sql, d)
    con.commit()
    close_all(con)

def create_table(sql):
    '''
    �������ݿ��
    '''
    execute_sql(sql)
    print('�������ݿ��ɹ�!')

def drop_table(table):
    '''
    ��������,��ɾ����������д������ݵ�ʱ��ʹ�ø÷�����ʱ��Ҫ���ã�
    '''
    if table is not None and table != '':
        sql = 'DROP TABLE IF EXISTS ' + table
        execute_sql(sql)
    else:
        print('the [{}] is empty or equal None!'.format(sql))

def save(sql, data):
    '''
    ��������
    dataΪҪ��������ݣ���ʽΪlist�����Դ�Ŷ�������
    '''
    if not data: return
    execute_sql(sql, data)
    print('�������ݳɹ�!')

def save_return_id(sql, data):
    '''
    ��������
    dataΪҪ���������
    ���ز������ɵ�id��Ҫ��idΪINTEGER PRIMARY KEY AUTOINCREMENT��ʽ
    '''
    id = 0
    if not data: return
    con = sqlite3.connect(Config.SQLITE_PATH)
    if not check_sql(sql): return
    cur = con.cursor()
    if Config.SHOW_SQL: print('ִ��sql:[{}],����:[{}]'.format(sql, data))
    cur.execute(sql, data)
    id = cur.lastrowid
    con.commit()
    close_all(con)
    return id
    
def update(sql, data):
    '''
    ��������
    dataΪҪ��������ݣ���ʽΪlist�����Դ�Ŷ�������    
    '''
    if not data: return
    execute_sql(sql, data)
    print('�������ݳɹ�!')
        
def delete(sql, data):
    '''
    ɾ������
    '''
    if not data: return
    execute_sql(sql, data)
    print('ɾ�����ݳɹ�!')

###################################################################



def getItemByAppName(con, app_name):
    cur = get_cursor(con)
    sql = "select * from app_info where app_name = ?"
    cur.execute(sql,(app_name,))
    return cur.fetchall()
    
def fetchall(con, sql, conditions):
    '''
    ��ѯ��������
    conditions��where����������
    '''
    if not check_sql(sql): return
    cu,cons = get_cursor(con),(conditions,)
    cu.execute(sql, cons) if data else cu.execute(sql)
    if Config.SHOW_SQL: print('��ѯ��������\nִ��sql:[{}]'.format(sql,conditions))
    return cu.fetchall()


