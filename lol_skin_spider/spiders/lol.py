# -*- coding: utf-8 -*-
import scrapy
import requests
import re
import json
from lol_skin_spider.items import LolSkinSpiderItem


class LolSpider(scrapy.Spider):
    name = 'lol'
    allowed_domains = ['qq.com']
    start_urls = ['https://lol.qq.com/data/info-heros.shtml']
    name_url='https://lol.qq.com/biz/hero/champion.js'      #英雄信息列表URL

    def parse(self, response):
        html=requests.get(self.name_url).content
        hero_names=re.findall(r'id":"(.*?)"',html.decode(),re.S)  #英雄名
        # key = re.findall(r'key":"(.*?)"', html.decode(), re.S)  #图片id 名
        for hero_name in hero_names:
            yield scrapy.Request(url='https://lol.qq.com/biz/hero/%s.js'%hero_name,callback=self.parse_image)


    def parse_image(self,response):
        item = LolSkinSpiderItem()
        #str.encode()  把一个字符串转换为其raw bytes形式 bytes.decode()   把raw bytes转换为其字符串形式
        html = response.text.encode().decode('unicode_escape')
        item['skin_name']=re.findall(r'name":"(.+)","title',html,re.S)+re.findall(r'name":"(.*?)","chromas',html,re.S)[1:]
        item['hero'] = re.findall(r'name":"(.+)","title', html, re.S)[0]
        ids=re.findall(r'id":"(\d+)","num',html,re.S)
        item['image_urls']=['https://ossweb-img.qq.com/images/lol/web201310/skin/big%s.jpg'%id for id in ids]
        yield item













