import luigi
import subprocess 
from datetime import datetime, timedelta


class MusicData(luigi.Task):
    
    date = datetime.now()
    date_ago = date + timedelta(days=-1)
    date_fit = date_ago.strftime('%Y%m%d')
    
    def run(self):
        subprocess.run(["scrapy crawl music_spider"],shell=True)     
   
    def output(self):
        return luigi.LocalTarget('./music_{}.db'.format(self.date_fit))

class MovieData(luigi.Task):
      
    date = datetime.now()
    date_ago = date + timedelta(days=-1)
    date_fit = date_ago.strftime('%Y%m%d')
 
    def run(self):
        subprocess.run(["python movie_crawl.py"],shell=True)      

    def output(self):
        return luigi.LocalTarget('./movie{}.db'.format(self.date_fit))
 
    def requires(self):
        return [ MusicData() ]

class TransformData(luigi.Task):

    date = datetime.now()
    date_ago = date + timedelta(days=-1)
    date_fit = date_ago.strftime('%Y%m%d')

    def run(self):
        subprocess.run(["python multi_base.py"],shell=True) 
    
    def output(self):
        return luigi.LocalTarget('./{}_result.db'.format(self.date_fit))

    def requires(self):
        return [ MovieData(),MusicData()]
        
    

