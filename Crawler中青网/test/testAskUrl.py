import bs4  # 网页解析 获取数据
import re  # 文字匹配
import urllib.request, urllib.error  # 指定url
import xlwt  # excel操作
import sqlite3  # 数据库操作
from bs4 import BeautifulSoup
testUrl="http://sou.cyol.com/servlet/SearchServlet.do?isall=1&allContentKey=%E7%96%AB%E6%83%85&contentKey=%E7%96%AB%E6%83%85&titleKey=%E7%96%AB%E6%83%85&authorKey=%E7%96%AB%E6%83%85&nodeNameResult=&subNodeResult=&dateFrom=20191201&dateEnd=20200625&sort=date&op=adv&paperName=%E4%B8%AD%E5%9B%BD%E9%9D%92%E5%B9%B4%E6%8A%A5&siteID=&nodeID=0&pager.offset=0&pageNo=1"

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
    eldiv = bs.select(".jsg1 >  a")
    # eldiv =bs.select(".box-result >h2 >  a")
    for link in eldiv:
        link["href"]= link["href"]
        print(link["href"])
        newsLinks.append(link["href"])
    # print(newsLinks)
    print(len(newsLinks)+"links in one page")
    return newsLinks

if __name__=="__main__":
    # askURL(testUrl)
    getLink(testUrl)
    # getLink(testUrl)
