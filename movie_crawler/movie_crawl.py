import urllib.request as ul
import json, secret, csv, os
from datetime import datetime, timedelta


movies = []

date = datetime.now()
date_ago = date + timedelta(days=-1)
date_fit = date_ago.strftime('%Y%m%d')

#당일 기준으로는 데이터를 끌어올수 없어서 전날 기준으로 데이터를 수집

api_key = secret.KEY['secret_key']

#API 키 가져오기

currentPath = os.getcwd()
file_path = currentPath + '/movie_list_'+date_fit+'.csv'
csv_file = open(file_path, 'w', newline="")

def start_crawl():
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key='+api_key+'&targetDt='+date_fit

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

#크롤링 끝 가져온 데이터 csv로 저장    
   
    csv_columns = ['rank','movieNm','movieCd','salesAmt','audiCnt']
    
    csvwriter = csv.DictWriter(csv_file, fieldnames=csv_columns);
    csvwriter.writeheader();
    
    for movie_list in movies:
        csvwriter.writerow(movie_list)
    
    csv_file.close()

    
start_crawl()
