import urllib.request as ul
import json, secret, csv, os
from datetime import datetime, timedelta
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import *


date = datetime.now()
date_ago = date + timedelta(days=-1)
date_fit = date_ago.strftime('%Y%m%d')

engine = create_engine('sqlite:///movie'+date_fit+'.db')
Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    date = Column(String(50))
    rank = Column(String(50))
    movieNm = Column(String(50))
    movieCd = Column(String(50))
    salesAmt = Column(String(50))
    audiCnt = Column(String(50))

Movie.__table__.create(bind=engine, checkfirst=True)

Session = sessionmaker(bind=engine)
session = Session()

movies = []

#당일 기준으로는 데이터를 끌어올수 없어서 전날 기준으로 데이터를 수집

api_key = secret.KEY['secret_key']

#API 키 가져오기

#currentPath = os.getcwd()
#file_path = currentPath + '/movie_list_'+date_fit+'.csv'
#csv_file = open(file_path, 'w', newline="")

def start_crawl(date = date_fit):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key='+api_key+'&targetDt='+date

    res = ul.urlopen(url, timeout=5)
    data = res.read()
    data_body = json.loads(data)
    
    for props in data_body['boxOfficeResult']['dailyBoxOfficeList']:
       movies.append({
                        'rank':props['rank'],
                        'movieNm':props['movieNm'],
                        'movieCd':props['movieCd'],
                        'salesAmt':props['salesAmt'],
                        'audiCnt':props['audiCnt']
       })

#크롤링 끝 가져온 데이터 csv로 저장.    
   
#    csv_columns = ['rank','movieNm','movieCd','salesAmt','audiCnt']
    
#    csvwriter = csv.DictWriter(csv_file, fieldnames=csv_columns);
#    csvwriter.writeheader();
    
#    for movie_list in movies:
#        csvwriter.writerow(movie_list)
    
#    csv_file.close()
# 크롤링 후 데이터 CSV에서 DB 저장으로 변경 2019/06/27

    for element in movies:
        result =  Movie(date = str(date),
                        rank=element['rank'],
                        movieNm=element['movieNm'],
                        movieCd=element['movieCd'],
                        salesAmt=element['salesAmt'],
                        audiCnt=element['audiCnt'])
        session.add(result)
        session.commit()
    
    request = session.query(Movie).all()
    
    for row in request:
       print(row.date,row.rank,row.movieNm,row.movieCd,row.salesAmt,row.audiCnt)

start_crawl()
