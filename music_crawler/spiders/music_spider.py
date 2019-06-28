# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime, timedelta

date = datetime.now()
date_ago = date + timedelta(days=-1)
date_fit = date_ago.strftime('%Y%m%d')

class MusicSpiderSpider(scrapy.Spider):
    name = 'music_spider'

    start_urls = ["http://www.mnet.com/chart/TOP100/"+date_fit]

    def parse(self, response):
        rank = response.xpath('//*[@id="content"]/div[4]/div[2]/table/tbody/tr/td[2]/div/span/text()').extract()
        musician = response.xpath('//*[@id="content"]/div[4]/div[2]/table/tbody/tr/td/div/div/div[2]/a[1]/text()').extract()
        song = response.css('.MMLI_Song::text').extract()
        album = response.css('.MMLIInfo_Album::text').extract()
        
        for item in zip(rank, musician, song ,album): 
            item = {
               "rank" : item[0].strip(),
               "musician" : item[1].strip(),
               "song" : item[2].strip(),
               "album" : item[3].strip(),
            } 
            yield item
