# -*- coding: utf-8 -*-
import scrapy


class MusicSpiderSpider(scrapy.Spider):
    name = 'music_spider'
    start_urls = ['http://www.mnet.com/chart/TOP100/20190623']

    def parse(self, response):
        top_selector = '.MMLITitle_Box'

        for music in response.css(top_selector):
            musician = '.MMLITitle_Info .MMLIInfo_Artist ::text'
            song = '.MMLITitleSong_Box .MMLI_Song ::text'
            album = '.MMLITitle_Info .MMLIInfo_Album ::text'
            yield {
                "song" : music.css(song).extract_first(),
                "musician" : music.css(musician).extract_first(),
                "album" : music.css(album).extract_first(),
            }
