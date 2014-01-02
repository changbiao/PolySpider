#!/usr/bin/env python
#coding:gbk
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from PolySpider.items import AppItem
from PolySpider import CommonUtils
import urllib2
class AppStarSpider(CrawlSpider):
	name = "hiapk"
	allowed_domains = ["apk.hiapk.com"]
	start_urls = [
                "http://apk.hiapk.com"
	]
        rules = [
            Rule(SgmlLinkExtractor(allow=("apk\.hiapk\.com/html/[0-9]*/[0-9]*/[0-9]*\.html", )),callback='parse_app'),
            Rule(SgmlLinkExtractor(allow=("apk\.hiapk\.com", ),deny=("down\.apk\.hiapk\.com","apk\.hiapk\.com/Download\.aspx", )), follow = True),
        ]
	def parse_app(self, response):	
            sel = Selector(response)
            item = AppItem()
            print "ץȡ��ʼ��%s" %response.url
            req=urllib2.Request("http://apk.hiapk.com" +   sel.xpath('//*[@id="main"]/div/div/div[1]/div[2]/div[1]/div[10]/a/@href').extract()[0])
            req.add_header('referer', response.url)

            item['apk_url'] = urllib2.urlopen(req).url
            item['app_name'] = CommonUtils.normalizeString(sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftName"]/text()').extract()[0])
            item['cover'] = sel.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[1]/div[1]/img/@src').extract()[0]
            item['version'] = CommonUtils.normalizeVersion(sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftVersionName"]/text()').extract()[0])
            item['category'] =  sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftCategory"]/text()').extract()[0]
            item['android_version'] =sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftSuitSdk"]/text()').extract()[0]
            item['download_times'] = sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_Download"]/text()').extract()[0]
            item['author'] =  sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftDeveloper"]/text()').extract()[0]
            item['last_update'] =   sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftPublishTime"]/text()').extract()[0]
            item['description'] =  sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_Description"]/text()').extract()[0]
            item['apk_size'] = sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Apk_SoftSize"]/text()').extract()[0]
            rating_star = sel.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div[3]/@class').extract()[0]
            if len(rating_star) < 21:
                item['rating_star'] = "0"
                item['rating_count'] = "0"
            else:
                item['rating_star'] = rating_star[21:-2] if len(rating_star) > 21 else "0"
                if "half" in item['rating_star']: item['rating_star'] = item['rating_star'][0] + ".5"
                item['rating_count'] = sel.xpath('//*[@id="ctl00_AndroidMaster_Content_Soft_StarProportion"]/div[2]/div[2]/div[3]/text()').extract()[0][:-3]
            #��ȡͼƬ��ַ��ͨ���ո����ָ����ͼƬ
            imgs =  sel.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div[4]/div[3]/ul/li/a/@href').extract()
            imgs_url = ""
            for img in imgs: imgs_url += img + " "
            item['imgs_url'] = imgs_url.strip()
            item['platform'] = "hiapk"
            print "ץȡ����������pipeline�������ݴ���"
            return item
