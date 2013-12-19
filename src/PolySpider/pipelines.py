#!/usr/bin/env python
#coding:gbk

from PolySpider import settings
import pybcs, re, urllib

class PolySpiderPipeline(object):
    def process_item(self, item, spider):
        return item
    
class AppStarSpiderPipeline(object):
    def process_item(self, item, spider):
        if spider.name != 'app_star': return item
        url = item['apk_url']
        
        ##���ݻ�ȡ��apk���ص�ַ��apk�ļ������ٶ���
        
        #����ƥ���ļ���
        name = re.compile('^.+/([^/]+)$').match(url).group(1).encode('utf8')
        #�����ļ�������
        print 'Start Download apk %s locally' %name
        urllib.urlretrieve(url, 'apk/' + name)
        print 'Download Finished'
        #�ϴ����ٶ���
        bcs = pybcs.BCS('http://bcs.duapp.com/', settings.BAIDU_AK, settings.BAIDU_SK, pybcs.HttplibHTTPC) 
        poly_bucket = bcs.bucket(settings.BAIDU_BUCKET)
        #����һ��object
        print 'Start Upload apk %s to BaiduYun' %name
        obj = poly_bucket.object('/apk/' + name)
        obj.put_file('apk/' + name)
        print 'Upload Finished'
        return item
