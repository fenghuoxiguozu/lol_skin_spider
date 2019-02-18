# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
from lol_skin_spider import settings
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request


class LolSkinSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class LOLImagesPipeline(ImagesPipeline):
    # 发送下载请求
    def get_media_requests(self, item, info):
        request_objs=super(LOLImagesPipeline,self).get_media_requests(item,info)
        for request_obj in request_objs:
            request_obj.item=item
        return request_objs

#这个方法是在图片将要存储时调用，俩获取这个图片存储的路径
    def file_path(self, request, response=None, info=None):
        path=super(LOLImagesPipeline,self).file_path(request,response,info)
        hero=request.item.get('hero')
        image_store=settings.IMAGES_STORE
        hero_path=os.path.join(image_store,hero)
        if not os.path.exists(hero_path):
            os.mkdir(hero_path)
        image_name=path.replace('full/','')
        image_path=os.path.join(hero_path,image_name)
        return image_path

