from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from sqlalchemy.sql import *

date = datetime.now()
date_ago = date + timedelta(days=-1)
date_fit = date_ago.strftime('%Y%m%d')


engine_base = create_engine('sqlite:///'+date_fit+'_result.db')
Base = declarative_base()

class Results(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    date = Column(String(50))
    movieTop = Column(String(50))
    musicRank = Column(String(50))
    musicName = Column(String(50))
    musicName = Column(String(50))
    musicAlbum = Column(String(50))

Results.__table__.create(bind=engine_base, checkfirst=True)
Session_base = sessionmaker(bind=engine_base)
session_base = Session_base()

#def find_top_movie_and_music(date=date_fit): 

engine1 = create_engine('sqlite:///movie'+date_fit+'.db')
Session1 = sessionmaker(bind=engine1)
session1 = Session1()

engine2 = create_engine('sqlite:///music_'+date_fit+'.db')
Session2 = sessionmaker(bind=engine2)
session2 = Session2()

request1 = session1.execute('select * from movies where rank=1 ')

for row in request1:
    movieNum1 = row.movieNm

request2 = session2.execute(text("select * from music_tb where album like ('%'|| :name ||'%')"),{'name': movieNum1[0]}).fetchall()

for prop in request2:
    result = Results(date = date_fit,
                     movieTop = movieNum1,
                     musicRank = prop['rank'],
                     musicName = prop['song'],
                     musicAlbum = prop['album'])
    session_base.add(result)
    session_base.commit()

request_base = session_base.query(Results).all()

for row in request_base:
    print(row.id, row.date, row.movieTop, row.musicRank, row.musicName, row.musicAlbum)

