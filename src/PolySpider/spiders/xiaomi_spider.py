#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from PolySpider.items import AppItem

from PolySpider.config import Config
from PolySpider.util import CommonUtil

class AppStarSpider(BaseSpider):
	name = "xiaomi"
	allowed_domains = ["xiaomi.com"]
	start_urls = [
                "http://app.xiaomi.com/"
	]
        
        def parse(self,response):
            '''
            ��Ӧ����ϸҳ�ĸ�ʽΪ http://www.appstar.com.cn/ace/store/n.htm
            n��30��ʼ���ܹ������3W�����
            ��������ѭ���ֱ��������Ӧurl�����󣬲�����yield���ظ�Scrapy��������ץȡ��response����parse_app�������Դ���ͽ���
            '''
            for i in range(1,1 + Config.APPSTAR_MAX_APPS):
                req = Request(url="http://app.xiaomi.com/detail/"+str(i),callback = self.parse_app)
                yield req
        

        def parse_app(self, response):	
            '''
            request��Callback������������ҳ������ץ�������ݣ�����xpathɸѡ����
            xpath�̳̣�http://www.w3school.com.cn/xpath/
            '''
            sel = Selector(response)
            item= AppItem()
            print "ץȡ��ʼ��%s" %response.url
            item['apk_url'] = "http://app.xiaomi.com" +  sel.xpath('/html/body/div[2]/div[1]/div[3]/div[1]/a/@href').extract()[0]
            item['app_name'] = CommonUtil.dropBrackets(sel.xpath('/html/body/div[2]/div[1]/div[2]/h1/text()').extract()[0])
            item['cover'] = sel .xpath("/html/body/div[2]/div[1]/div[3]/div[1]/div[1]/img/@src").extract()[0]
            item['version'] = CommonUtil.normalizeVersion(sel.xpath('/html/body/div[2]/div[2]/ul[1]/li[2]/h4/text()').extract()[0])
            item['rating_star'] = sel.xpath('/html/body/div[2]/div[1]/div[3]/div[1]/div[2]/@class').extract()[0][11:]
            item['rating_count'] = '0'
            item['category'] = sel.xpath('/html/body/div[2]/div[2]/ul[1]/li[1]/h4/text()').extract()[0]
            item['android_version'] = '0'
            item['download_times'] = '0'
            item['author'] = sel.xpath('/html/body/div[2]/div[2]/ul[1]/li[6]/h4/text()').extract()[0]
            item['last_update'] =  sel.xpath('/html/body/div[2]/div[2]/ul[1]/li[3]/h4/text()').extract()[0]
            descriptions = sel.xpath('/html/body/div[2]/div[1]/div[3]/div[2]/div[1]/p/text()').extract()
            alldescription=''
            for description in descriptions:
                alldescription=alldescription+description
                
            item['description'] = alldescription.strip()
            item['apk_size'] = sel.xpath('/html/body/div[2]/div[2]/ul[1]/li[5]/h4/text()').extract()[0]
            #��ȡͼƬ��ַ��ͨ���ո����ָ����ͼƬ
            imgs =  sel.xpath('//*[@id="J_thumbnail_wrap"]/img').extract()
            imgs_url = ""
            for img in imgs: imgs_url += img + " "
            item['imgs_url'] = imgs_url.strip()
            item['platform'] = "xiaomi"
            print "ץȡ����������pipeline�������ݴ���"
            return item