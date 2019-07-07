from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import urllib.request
import sqlite3
class WeatherDB:
    def openDB(self):
        self.con=sqlite3.connect("weather.db")
        self.cursor=self.con.cursor()
        try:
            self.cursor.execute("create table weathers (wCity varchar(16),wDate varchar(16),wWeather varchar(64),wTemp varchar(32),constraint pk_weather primary key(wCity,wData))")
        except:
            self.cursor.execute("delete from weather")

    def openDB(self):
        self.con.commit()
        self.con.close()

    def insert(self,city,data,weather,temp):
        try:
            self.cursor.execute("insert to weathers (wCity,wData,wWeather,wTemp) values(?,?,?,?)",(city,data,weather,temp))
        except Exception as err:
            print(err)

    def show(self):
        self.cursor.execute("select * from weathers")
        rows=self.cursor.fetchall()
        print("%-16s%-16s%-32s%-16s" %("city","data","weather","temp"))
        for row in rows:
            print("%-16s%-16s%-32s%-16s" %(row[0],row[1],row[2],row[3]))

class WeatherForeast:
    def _init_(self):         #初始化
        self.headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
        }
        self.cityCode={
            "北京":"101010100","上海":"101020100","广州":"101280101","深圳":"101280601"
        }
    def forecastCity(self,city):    #城市天气预报
        if city not in self.cityCode.keys():
            print(city+"code cannot be found")
            return
        url="http://www.weather.com.cn/weather/"+self.cityCode[city]+".shtml"
        try:
            req=urllib.request.Request(url,heades=self.headers)
            data=urllib.request.urlopen(req)
            data=data.read()
            dammit=UnicodeDammit(data,["utf-8","gbk"])
            data=dammit.unicode_markup
            soup=BeautifulSoup(data,"lxml")
            lis=soup.select("ul[class='t clearfix'] li")
            for li in lis:
                try:
                    date = li.select('h1')[0].text
                    weather = li.select('p[class="wea"]')[0].text
                    temp = li.select('p[class="tem"] span')[0].text + "/" + li.select('p[class="tem"] i')[0].text
                    print(city,date, weather, temp)
                    self.db.insert(city,date,weather,temp)
                except Exception as err:
                    print(err)
        except Exception as err:
            print(err)

    def process(self,cities):
        self.db=WeatherDB()
        self.db.openDB()

        for city in cities:
            self.forecastCity(city)

        self.db.closeDB()

ws=WeatherForeast()
ws.process(["北京","上海","广州","深圳"])
print("completed")


