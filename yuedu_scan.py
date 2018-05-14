#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urlparse import urljoin
import requests
import csv
import sys
import MySQLdb    
sys.setdefaultencoding( "utf-8" )


url = "http://yuedu.fm/article/{page}/"
#已完成的页数序号，初时为0
page = 1
csv_file = open("rent.csv","ab+") #打开rent.csv
csv_writer = csv.writer(csv_file, delimiter=',') # 创建writer对象，指定文件与分隔符
while True:   #开始循环
    page += 1
    response = requests.get(url.format(page=page))  # 抓取目标页面
    html = BeautifulSoup(response.text,"lxml") # 创建一个BeautifulSoup对象
    title= html.select("#bd > div.wp.fl > div.item > div.item-base > div.item-name")  #标题
    if not title:
		continue
    titles = title[0].get_text()
    author= html.select("#bd > div.wp.fl > div.item > div.item-base > div.item-meta > em")[0].get_text()[1:] #文章作者
    Radio_anchor = html.select("#bd > div.wp.fl > div.item > div.item-base > div.item-meta > em")[1].get_text()[1:] #主播
    frequency = html.select("#bd > div.wp.fl > div.item > div.item-base > div.item-meta > span > span")[0].get_text() #播放次数
    text = html.select("#bd > div.wp.fl > div.item > div.item-intro.row > div")[0].get_text() #正文
    time = html.select("#bd > div.wp.fl > div.item > div.item-base > div.item-meta > em")[2].get_text()[1:] #播放时间
    nexts = html.select("#bd > div.wp.fl > div.item-pg.row > span.fr") #下一页
    #连接        
    conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="yuedufm",charset="utf8")      
    cursor = conn.cursor()
    cursor.execute("SET NAMES utf8")
    sql = "insert into tables(titles,Radio_anchor,author,frequency,time,text) values(%s,%s,%s,%s,%s,%s)" 
    param = (titles,Radio_anchor,author,frequency,time,text)        
    n = cursor.execute(sql,param)
    print 'insert',n    
    conn.commit()  #提交数据进数据库  
    conn.close()  #关闭数据库连接           
    #csv_writer.writerow([titles, Radio_anchor, author, frequency, time, text])
    if not nexts:
    	break
    print "fetch: ", url.format(page=page),titles #输出爬取页码URL

#csv_file.close()
