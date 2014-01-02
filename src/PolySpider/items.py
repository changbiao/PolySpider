#!/usr/bin/env python
#coding:gbk

from scrapy.item import Item, Field

class AppItem(Item):
    """
    ��ȡӦ�õľ�����Ϣ��
    apk_url: apk��������
    pakage_name: Ӧ�ð���
    app_name: Ӧ������
    cover: ����ͼƬurl��ַ
    version: �汾��
    rating_star: ������
    rating_count: ��������
    category: ���
    android_version: ֧�ֵ�Android�汾
    download_times: ���ش���
    author: ���߻�˾
    last_update: ������ʱ��
    description: Ӧ�ü��
    imgs_url: Ӧ�ý�ͼ����
    """
    app_url = Field()
    apk_url = Field()
    pakage_name = Field()
    app_name = Field()
    cover = Field()
    version = Field()
    rating_star = Field()
    rating_count = Field()
    category = Field()
    android_version = Field()
    download_times = Field()
    author = Field()
    last_update = Field()
    description = Field()
    imgs_url = Field()
    apk_size = Field()
    platform = Field()
    
    def __repr__(self):
        #Debug��Infoģʽ�£�Pipeline������ɺ󲻴�ӡItem����
        return "\n"
    