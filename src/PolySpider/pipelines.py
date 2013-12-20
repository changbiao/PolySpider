#!/usr/bin/env python
#coding:gbk

from PolySpider import Config
from PolySpider import SqliteUtils
import pybcs
import re
import urllib
import upyun
import os

class PolySpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class AppStarFileUploadPipeline(object):
    def process_item(self, item, spider):
        if spider.name != 'app_star': return item
        url = item['apk_url']
        
        ##���ݻ�ȡ��apk���ص�ַ��apk�ļ������ٶ���
        #����ƥ���ļ���
        name = re.compile('^.+/([^/]+)$').match(url).group(1).encode('utf8')
        #�����ļ�������
        print 'Start Download apk %s locally' %name
        if not os.path.exists('apk/'): os.makedirs('apk/')
        urllib.urlretrieve(url, 'apk/' + name)
        print 'Download Finished'
        #�����ļ������� Done
        '''
        #�ϴ����ٶ���
        bcs = pybcs.BCS('http://bcs.duapp.com/', Config.BAIDU_AK, Config.BAIDU_SK, pybcs.HttplibHTTPC) 
        poly_bucket = bcs.bucket(Config.BAIDU_BUCKET)
        #����һ��object
        print 'Start Upload apk %s to BaiduYun' %name
        obj = poly_bucket.object('/apk/' + name)
        print "%s\n%s\n%s\n%s\n" %(Config.BAIDU_AK,Config.BAIDU_SK,Config.BAIDU_BUCKET,name)
        obj.put_file('apk/' + name)
        print 'Upload Finished'
        #�ϴ����ٶ��� Done
        '''
        '''
        #�ϴ���UpYun
        # ���� `bucket` Ϊ�ռ�����,`username` �� `password` �ֱ�Ϊ��Ȩ����Ա�ʺź����룬��ѡ��
        # ���� `timeout` Ϊ HTTP ����ʱʱ�䣬Ĭ�� 60 �룬��ѡ��
        # ���ݹ��ڵ���������������ƴ洢 API Ŀǰ�ṩ�˵��š���ͨ��ͨ���ƶ���ͨ��������㣬
        # �ڳ�ʼ��ʱ���ɲ��� `endpoint` �������ã����ѡ��ֵ�У�
        # upyun.ED_AUTO     �������������Զ�ѡ�����㣬Ĭ��
        # upyun.ED_TELECOM  ���Ž����
        # upyun.ED_CNC      ��ͨ��ͨ�����
        # upyun.ED_CTT      �ƶ���ͨ�����

        up = upyun.UpYun(Config.UPYUN_BUCKET, Config.UPYUN_USERNAME, Config.UPYUN_PASSWORD, timeout=30, endpoint=upyun.ED_AUTO)
        print "Bucket:%s | UserName:%s" %(Config.UPYUN_BUCKET, Config.UPYUN_USERNAME)
        up.put('/apk/' + name, 'apk/' + name)
        #�ϴ���UpYun Done
        '''
        
        return item
class AppStarDatabasePipeline(object):
    def process_item(self, item, spider):
        con = SqliteUtils.get_conn(Config.SQLITE_PATH)
        cur = SqliteUtils.get_cursor(con)

        #��������ڣ��򴴽���
        if  not SqliteUtils.is_table_exist(cur, 'app_info'):
            sql_table_create = '''
                CREATE TABLE app_info(
                id INTEGER PRIMARY KEY,
                apk_url VARCHAR(32))
            '''
            SqliteUtils.create_table(con,sql_table_create)
        #��������
        sql_insert = '''
            INSERT INTO app_info values(null,?)
        '''
        data = [(item['apk_url'],)]
        SqliteUtils.save_or_update(con, sql_insert, data)
        return item
