#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import re
import os
from scrapy.exceptions import DropItem
from PolySpider.config import Config
from PolySpider.util import CategoryUtil
from PolySpider.sql import App
from PolySpider.sql import AppDetail

import urllib
import pybcs
from PolySpider.util import ApkUtil
from PolySpider.util import FileUploadUtil
from PolySpider.util import CommonUtil

APP_TABLE_INSERT = False
APP_DETAIL_TABLE_INSERT = False

class PolySpiderPipeline(object):
    def process_item(self, item, spider):
        return item

'''
ִ��˳��ID��100
����Ӧ�õķ����Pipeline~
'''
class CategorizingPipeline(object):
    def process_item(self,item,spider):
        #���category��û������� �ᱨ��
        item['category'] = CategoryUtil.getCategoryIds(item['category'].encode('gbk','ignore'))
        return item

'''
ִ��˳��ID��101
���ps_app�����Ƿ���ڸ�App����
��������ڣ����¼��App����
������ڣ����author,���Ϊ�գ������author
'''
class CheckAppPipeline(object):
    def process_item(self,item,spider):
        app_name = item['app_name']
        app = App.get_app_by_app_name(app_name)
        if not app:
            #�������
            for category in item['category'].split(","):
                item['category'] = category + ":1" + ","
            #��������
            APP_TABLE_INSERT = True
            item['app_id'] = App.insert_app(item)
        else:
            item['app_id'] = app['id']
            #���·���
            #�ж�author�Ƿ�Ϊ�գ����Ϊ�գ������app��
            if app['author'] == "" and item['author'] != "":
                App.update_app_author(app['id'], item['author'])
        return item

'''
ִ��˳��ID��102
����ps_app_detail�����Ƿ���ڸ�App_Detail����(ͨ��app_id, verison, flatform��Ψһ��ʶ)
��������ڣ����¼��App����
������ڣ�����һЩ������Ϣ��Ȼ�󽫸�ItemDrop��
'''
class CheckAppDetailsPipeline(object):
    def process_item(self,item,spider):
        app_detail = AppDetail.get_app_detail_by_item(item)
        if not app_detail:
            #����Apk | ����Apk����¼pakage_name | �ϴ�Apk��UpYun
            apk_operation(item)
            #��������
            AppDetail.insert_app_detail(item)
        else:
            #TODO �����漰�����²���-->rating_point | rating_count | download_times | apk_url | cover | 
            raise DropItem("Crawled app has been record in databse. No newer version has been found!")
        
    def apk_operation(self, item):
        '''
        ִ��˳��ID��102
        �ļ��ϴ���������
        ����Apk��Ϣ,��ȡpakage_name
        �ϴ���UpYun/BaiduYun
        '''
        url = item['apk_url']
        ##���ݻ�ȡ��apk���ص�ַ��apk�ļ������ٶ���
        #����ƥ���ļ���
        name = re.compile('^.+/([^/]+)$').match(url).group(1).encode('utf8')
        #�����ļ�������
        print '��ʼ��������apk�� %s ' %name
        if not os.path.exists('apk/'): os.makedirs('apk/')
        #��ʼ����
        #���ý���������������url���ļ�����
        #CommonUtil.progressbar(url,'apk/' + name)
        print '�������'
        #�����ļ������� Done
        
        #����APK�ļ�����ȡ�����info_list
        #Ŀǰֵ��ȡ�������pakage_name���Ժ�������ӱ����Ҫ������
        print '��ʼ����Apk����'
        #info_list = ApkUtil.getInfoList(name)
        #item['pakage_name'] = info_list['packageInfo']['orig_package']
        item['pakage_name'] = ''
        print '�������'
        #Done
        return item
        
        '''
        #�ϴ����ٶ���
        bcs = pybcs.BCS('http://bcs.duapp.com/', Config.BAIDU_AK, Config.BAIDU_SK, pybcs.HttplibHTTPC) 
        poly_bucket = bcs.bucket(Config.BAIDU_BUCKET)
        #����һ��object
        print '��ʼ�ϴ�apk %s ��BaiduYun' %name
        obj = poly_bucket.object('/apk/' + name)
        print "%s\n%s\n%s\n%s\n" %(Config.BAIDU_AK,Config.BAIDU_SK,Config.BAIDU_BUCKET,name)
        obj.put_file('apk/' + name)
        print '�ϴ����'
        #�ϴ����ٶ��� Done

        #�ϴ���UpYun
        print '��ʼ�ϴ�apk %s ��UpYun' %name
        up = FileUploadUtil.UpYun()
        up.put('apk/' + name, 'apk/' + name)
        print '�ϴ����'
        #�ϴ���UpYun Done
        '''

class UpdateCategoryPipeline(object):
    def process_item(self,item,spider):
        if not APP_TABLE_INSERT:
            #TODO ���¼���category
            category = ""
            
            #����ps_app���category
            App.update_app_category(app['id'], category)
        return item


#'''
#ִ��˳��ID��100
#�жϰ汾�ţ����ݰ汾�����ж��Ƿ���к�������
#'''
#class VersionCmpPipeline(object):
#    def process_item(self,item,spider):
#        con = SqliteUtil.get_conn(Config.SQLITE_PATH)
#        #��������ڣ��򴴽���
#        SqliteUtil.checkAppInfoExist(con)
#        oldItem = SqliteUtil.getItemByAppName(con,item['app_name'])
#        if oldItem == []:
#            print "���ݿ����޸�App��¼��ִ�в������"
#        elif CommonUtil.cmpVersion(oldItem[0][5], item['version']): 
#            raise DropItem("Crawled app has been record in databse. No newer version has been found!")
#        return item


'''
ִ��˳��ID��103
���ݿ������߸��²���
'''
class DatebasePipeline(object):
    def process_item(self,item,spider):
        con = SqliteUtil.get_conn(Config.SQLITE_PATH)
        if SqliteUtil.getItemByAppName(con,item['app_name']) != []:
            #��������
            print "���ݿ��������"
            sql = '''
                UPDATE  app_info SET
                    apk_url = ? ,
                    pakage_name = ?,
                    cover = ?,
                    version = ?,
                    rating_star = ?,
                    rating_count = ?,
                    category = ?,
                    android_version = ?,
                    download_times = ?,
                    author = ?,
                    last_update = ?,
                    description = ?,
                    imgs_url = ?,
                    apk_size = ?,
                    platform = ?
                WHERE app_name = ? '''
            data = [(
                item['apk_url'],
                item['pakage_name'],
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
                item['imgs_url'],
                item['apk_size'],
                item['platform'],
                item['app_name'])]
        else:
            #��������
            print '���ݿ��������'
            sql = '''INSERT INTO app_info values(null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
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
                    item['imgs_url'],
                    item['apk_size'],
                    item['platform'])]
                    
        SqliteUtil.save_or_update(con, sql, data)
        print '���ݿ��������'
        return item
