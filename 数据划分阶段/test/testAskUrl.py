from xml import etree

import bs4  # 网页解析 获取数据
import re  # 文字匹配
import urllib.request, urllib.error  # 指定url

import requests
import xlwt  # excel操作
import sqlite3  # 数据库操作
from bs4 import BeautifulSoup
testUrl="https://weibo.cn/cctvxinwen?page=1"
from lxml import etree

def askURL(url):
    # 获取网页url信息String
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47"}
    # head["User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
    # Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47"] 用户代理：告诉目标网站服务器我们是什么类型的机器（我们可以接受什么水平的文件内容 header
    # 模拟浏览器头部信息向服务器发消息
    headers = {
        'Cookie': '_T_WM=65929012417; MLOGIN=1; WEIBOCN_WM=3349; H5_wentry=H5; backURL=https%3A%2F%2Fweibo.cn; SCF=Auke0MD2XI9FOk105zyxbv2HHCoblv0Eu9pqjvJe2pzMasDJRHqFaHlzyqVv_I_GxK3YxSLQ19Rg8jS51-HHFnE.; SUB=_2A25NDTZ3DeRhGeBI7lIZ-SnEzTyIHXVuDlo_rDV6PUJbktAKLRDzkW1NRpCOn0yu_hu275WGdDYhYGvzNqbvCCFy; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFHh2SwTvArbaeKPiY-YIwO5NHD95QcSo-71h.N1hq7Ws4DqcjLi--fiKnfi-8hi--fi-82iK.4i--NiKy8iKn4i--4i-i8iK.4-Btt; SSOLoginState=1611220519; M_WEIBOCN_PARAMS=lfid%3D100103type%253D1%2526q%253D%25E5%25A4%25AE%25E8%25A7%2586%25E6%2596%25B0%25E9%2597%25BB%26luicode%3D20000174',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47",

    }

    # 封装
    request = urllib.request.Request(url, headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        # res = requests.get(url='https://weibo.cn/search/mblog', headers=headers)
        # html = etree.HTML(res.text.encode('utf-8'))

    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        print("error in askURL!")

    # print(html)
    return html

# def getLink(url):
#     # 一页中所有岗位链接
#     allNews=[]
#     allNewsContent=[]
#     allNewsComments=[]
#
#     # 访问新闻标题页/列表页
#     html= askURL(url)
#     bs= BeautifulSoup(html, "html.parser")
#     eldiv = bs.select("body > div.c > div > span.ctt")
#     print(eldiv)
#     for link in eldiv:
#         # link["href"]= link["href"]
#         aNews={}
#         aNews['content']= link.text
#         print(link.text)
#         allNewsContent.append(link.text)
#         # newsLinks.append(link["href"])
#     # print(newsLinks)
#     return allNews
def getLink(url):
    # 一页中所有岗位链接
    allLinks1Page=[]
    # 访问新闻标题页/列表页
    html= askURL(url)
    bs= BeautifulSoup(html, "html.parser")
    eldiv = bs.select("body > div.c > div > a.cc")
    print(eldiv)
    for link in eldiv:
        allLinks1Page.append( link["href"])
        print('gettingLink:')
        print(link["href"])

    return allLinks1Page

if __name__=="__main__":
    # askURL(testUrl)
    getLink(testUrl)
    # getLink(testUrl)
