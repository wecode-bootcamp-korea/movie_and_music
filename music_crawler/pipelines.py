# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from datetime import datetime, timedelta

date = datetime.now()
date_ago = date + timedelta(days=-1)
date_fit = date_ago.strftime('%Y%m%d')

class MusicCrawlerPipeline(object):
    
    def __init__(self): 
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("music_"+date_fit+".db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS music_tb""")
        self.curr.execute("""create table music_tb(
                            rank text,
                            song text,
                            musician text,
                            album text
                            )""")
    
    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert into music_tb values (?,?,?,?)""",(
            item['rank'],
            item['song'],
            item['musician'],
            item['album']   
        ))
        self.conn.commit()

