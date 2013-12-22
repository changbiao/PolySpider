#!/usr/bin/env python
#coding:gbk

from PolySpider import Config
from PolySpider import SqliteUtils
from PolySpider import CommonUtils
from PolySpider import apkParser
from scrapy.exceptions import DropItem
import re
import os
import urllib
import upyun
import pybcs

class PolySpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class AppStarFileUploadPipeline(object):
    def process_item(self, item, spider):
        if spider.name != 'app_star': return item
        con = SqliteUtils.get_conn(Config.SQLITE_PATH)
        cur = SqliteUtils.get_cursor(con)
        #��������ڣ��򴴽���
        checkAppInfoExist(con)
        oldItem = SqliteUtils.getItemByAppName(cur,item['app_name'])
        if oldItem != [] and CommonUtils.cmpVersion(oldItem[0][5], item['version']): 
            print "Crawled app has been record in databse. No newer version has been found!"
            raise DropItem("Crawled app has been record in databse. No newer version has been found!")
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
        
        #����APK�ļ�����ȡ�����info_list
        #Ŀǰֵ��ȡ�������pakage_name���Ժ�������ӱ����Ҫ������
        info_list = apkParser.getInfoList(name)
        item['pakage_name'] = info_list['packageInfo']['orig_package']
        #Done
        
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
        with open('apk//' + name, 'rb') as f: res = up.put('apk/' + name, f, checksum=True)
        #�ϴ���UpYun Done
        '''
        return item
class AppStarDatabasePipeline(object):
    def process_item(self, item, spider):
        con = SqliteUtils.get_conn(Config.SQLITE_PATH)

        #��������ڣ��򴴽���
        checkAppInfoExist(con)
        
        #��������
        sql_insert = '''
            INSERT INTO app_info values(null,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
        print item
        data = [(
                item['apk_url'],
                item['pakage_name'],
                item['app_name'],
                item['cover'],
                item['version'],
                item['rating_star'],
                item['rating_count'],
                item['category'],
                item['android_version'],
                item['download_times'],
                item['author'],
                item['last_update'],
                item['description'],
                item['imgs_url'])]
        SqliteUtils.save_or_update(con, sql_insert, data)
        return item

def checkAppInfoExist(con):
    #��������ڣ��򴴽���
    cur = SqliteUtils.get_cursor(con)
    if  not SqliteUtils.is_table_exist(cur, 'app_info'):
        sql_table_create = '''
            CREATE TABLE app_info(
            id INTEGER PRIMARY KEY,
            apk_url VARCHAR(32),
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
            imgs_url TEXT	
            )
        '''
        SqliteUtils.create_table(con,sql_table_create)