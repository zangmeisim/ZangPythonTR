from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pyhdb
import datetime
import requests
import os

#url=urlopen('http://www.weather.com.cn/textFC/hb.shtml')
#soup=BeautifulSoup(url,'html.parser')
#getarea=soup.find('ul',class_="lq_contentboxTab2")

current_date= datetime.datetime.now()
current_daytime= current_date.strftime('%Y-%m-%d %H:%M:%S')

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
    cursor.execute('insert into ZANG_TEST_PY (PROVINCE,CITY,DATE_ID,WEATHER,WIND,MAX_TEM,MIN_TEM,ETL_DATETIME) values(%s,%s,%s,%s,%s,%s,%s,%s)',(province_name,city_name,current_date,weather,wind,max,min,current_daytime))

def delete_tem(conn):
    cursor = conn.cursor()
    cursor.execute('delete from ZANG_TEST_PY where DATE_ID=current_date')

conn = get_connect()
delete_tem(conn)

urls = ['http://www.weather.com.cn/textFC/hb.shtml', 'http://www.weather.com.cn/textFC/db.shtml', 'http://www.weather.com.cn/textFC/hd.shtml', 'http://www.weather.com.cn/textFC/hz.shtml', 'http://www.weather.com.cn/textFC/hn.shtml', 'http://www.weather.com.cn/textFC/xb.shtml', 'http://www.weather.com.cn/textFC/xn.shtml']
for url in urls:

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}# 设置头文件信息 #
    response = requests.get(url, headers=headers).content # 提交requests get 请求
    soup = BeautifulSoup(response, "html.parser") # 用Beautifulsoup 进行解析

    commid = soup.find('div', class_='conMidtab')
    commid2 = commid.findAll('div',class_='conMidtab2')
    for info in commid2:
        tr_list = info.findAll('tr')[2:]#get the 3rd 'tr' tag
        #print (tr_list)
        for index,tr in enumerate(tr_list): #enumerate can return the position of field
            td_list=tr.findAll('td')
            if index==0:
                province_name=td_list[0].text.replace('\n','') #get the text on every tag ,replace \n for ''
                city_name = td_list[1].text.replace('\n','')
                weather=td_list[5].text.replace('\n','')
                wind =td_list[6].text.replace('\n','')
                max = td_list[4].text.replace('\n', '')
                min = td_list[7].text.replace('\n', '')
                if max == '-':
                    max=min
                #print (province_name,city_name)
                get_tem(conn)
            else:
                city_name = td_list[0].text.replace('\n', '')
                weather = td_list[4].text.replace('\n', '')
                wind = td_list[5].text.replace('\n', '')
                max = td_list[3].text.replace('\n', '')
                min = td_list[6].text.replace('\n', '')
                if max == '-':
                    max=min
                #print (city_name,weather,wind,max,min)
                get_tem(conn)

conn.commit()
print("It's done'")
os.system('pause')