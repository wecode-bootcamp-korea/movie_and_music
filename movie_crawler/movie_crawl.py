import urllib.request as ul
import json, secret, csv, os
from datetime import datetime, timedelta


movies = []
date = datetime.now()
date_ago = date + timedelta(days=-1)
date_fit = date_ago.strftime('%Y%m%d')

secret = secret.KEY['secret_key']

def start_crawl():
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key='+secret+'&targetDt='+date_fit

    res = ul.urlopen(url, timeout=5)
    data = res.read()
    d = json.loads(data)
    
    for b in d['boxOfficeResult']['dailyBoxOfficeList']:
       movies.append({'rank':b['rank'],'movieNm':b['movieNm'],'movieCd':b['movieCd'],'salesAmt':b['salesAmt'],'audiCnt':b['audiCnt']})
    
    
    currentPath = os.getcwd()
    file_path = currentPath + '/movie_list_'+date_fit+'.csv'
    csv_columns = ['rank','movieNm','movieCd','salesAmt','audiCnt']
    
    csv_file = open(file_path, 'w', newline="")
    csvwriter = csv.DictWriter(csv_file, fieldnames=csv_columns)
    csvwriter.writeheader()
    for movie_list in movies:
        csvwriter.writerow(movie_list)
    csv_file.close()

    
start_crawl()
