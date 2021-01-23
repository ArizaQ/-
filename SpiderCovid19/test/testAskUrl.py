import bs4  # 网页解析 获取数据
import re  # 文字匹配
import urllib.request, urllib.error  # 指定url
import xlwt  # excel操作
import sqlite3  # 数据库操作
from bs4 import BeautifulSoup
testUrl="http://data.people.com.cn/rmrb/s?qs=%7B%22cds%22%3A%5B%7B%22cdr%22%3A%22AND%22%2C%22cds%22%3A%5B%7B%22fld%22%3A%22title%22%2C%22cdr%22%3A%22OR%22%2C%22hlt%22%3A%22true%22%2C%22vlr%22%3A%22OR%22%2C%22val%22%3A%22%E7%96%AB%E6%83%85%22%7D%2C%7B%22fld%22%3A%22subTitle%22%2C%22cdr%22%3A%22OR%22%2C%22hlt%22%3A%22true%22%2C%22vlr%22%3A%22OR%22%2C%22val%22%3A%22%E7%96%AB%E6%83%85%22%7D%2C%7B%22fld%22%3A%22introTitle%22%2C%22cdr%22%3A%22OR%22%2C%22hlt%22%3A%22true%22%2C%22vlr%22%3A%22OR%22%2C%22val%22%3A%22%E7%96%AB%E6%83%85%22%7D%2C%7B%22fld%22%3A%22contentText%22%2C%22cdr%22%3A%22OR%22%2C%22hlt%22%3A%22true%22%2C%22vlr%22%3A%22OR%22%2C%22val%22%3A%22%E7%96%AB%E6%83%85%22%7D%5D%7D%5D%2C%22obs%22%3A%5B%7B%22fld%22%3A%22dataTime%22%2C%22drt%22%3A%22DESC%22%7D%5D%7D&tr=Y&ss=1&pageNo=1&pageSize=50"

def askURL(url):
    # 获取网页url信息String
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47"}
    # head["User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
    # Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47"] 用户代理：告诉目标网站服务器我们是什么类型的机器（我们可以接受什么水平的文件内容 header
    # 模拟浏览器头部信息向服务器发消息

    # 封装
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')

    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        print("error in askURL!")

    # print(html)
    return html

def getLink(url):
    # 一页中所有岗位链接
    newsLinks=[]
    # 访问新闻标题页/列表页
    html= askURL(url)
    bs= BeautifulSoup(html, "html.parser")
    eldiv = bs.select(".sreach_div >.sreach_li>h3 >  a")
    # eldiv =bs.select(".box-result >h2 >  a")
    # print(eldiv)
    for link in eldiv:
        link["href"]= 'http://data.people.com.cn/'+link["href"]
        print(link["href"])
        newsLinks.append(link["href"])
    # print(newsLinks)
    print(len(newsLinks))
    return newsLinks

if __name__=="__main__":
    getLink(testUrl)
    # getLink(testUrl)
