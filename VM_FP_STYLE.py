from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re
import pyhdb
import datetime

def get_connect():
    conn_obj = pyhdb.connect(
        host='10.150.16.99',
        port = 30015,
        user = 'sapabap2',
        password = 'Sap_7890'
    )
    return conn_obj

def get_tem(conn):
    cursor = conn.cursor()
    cursor.execute('insert into ZANG_FIRSTPAGE_STYLE (BRAND_ID,DATE_ID,STYLE_ID,STYLECOLOR_ID,ETLDATE) values(%s,%s,%s,%s,%s)',('VERO MODA',current_date,style_id,stylecolor_id,current_daytime))

def delete_tem(conn):
    cursor = conn.cursor()
    cursor.execute('delete from ZANG_FIRSTPAGE_STYLE where DATE_ID=current_date')



url=('https://www.veromoda.com.cn/')
headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}# 设置头文件信息 #

resp=requests.get(url,headers=headers).content
soup=BeautifulSoup(resp,'html.parser')

container = soup.find('div', class_="container")
area_all=soup.find_all('area')[11:]


global stylecolor_id
current_date= datetime.datetime.now()
current_daytime= current_date.strftime('%Y-%m-%d %H:%M:%S')
conn=get_connect()

#initial
delete_tem(conn)

for area in area_all:
    # print(area)
    url1=area['href']
    style_pos = url1.find('design=')
    #print(style_pos)
    stylecolor_id=(url1[style_pos+7:])
    if style_pos >= 0:
        print(stylecolor_id)
        style_id = (stylecolor_id[0:9])
        get_tem(conn)
    else:
        None

conn.commit()

print("It's done'")
