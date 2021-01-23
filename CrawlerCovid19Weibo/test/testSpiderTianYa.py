import bs4  # 网页解析 获取数据
import re  # 文字匹配
import urllib.request, urllib.error  # 指定url
import xlwt  # excel操作
import sqlite3  # 数据库操作
from bs4 import BeautifulSoup

'''
'''

baseurl= "https://search.sina.com.cn/?q=%e7%96%ab%e6%83%85&c=news&from=index&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page="

# aNews= {} # {"link":"http://www.wiki.com","title":"covid19 is good","content":"XXXXXXXX","comment":"happy angry fuck it","":"","":""}
allNews=[]
def main():
    savepath = ".\\covid19NewsXH.xls"
    page = 1
    while True:
        # 每一页的链接
        url = baseurl +str(page)
        # 每一页中所有新闻链接的list
        newsLinkAPage=getLink(url)
        if len(newsLinkAPage)==0:  # 没有新闻了！
            break
        print(newsLinkAPage)
        # for aNewsLink in newsLinkAPage:
        #     getAData(aNewsLink)# 一个详情页的链接
        # getData(newsLinkAPage)
        page+=1
    # saveData(allNews,savepath)
    #print(html)


    return


def getLink(url):
    # 一页中所有岗位链接
    newsLinks=[]
    # 访问新闻标题页/列表页
    html= askURL(url)
    bs= BeautifulSoup(html, "html.parser")
    eldiv =bs.select(".box-result >h2 >  a")
    # print(eldiv)
    for link in eldiv:
        # print(link["href"])
        newsLinks.append(link["href"])
    print(newsLinks)
    print(len(newsLinks))
    return newsLinks

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

def getAData(newsPage):
    print("getting: "+newsPage)
    aNews = {}  # {"link":"http://www.wiki.com","title":"covid19 is good","content":"XXXXXXXX","comment1":"happy","comment2":"angy","comment3":"fuck it","comment4":"dont care","comment5":"sad","comment6":"positive"}
    newsHtml = askURL(newsPage)
    bs = BeautifulSoup(newsHtml, "html.parser")
    # 获取链接
    aNews["link"]= newsPage
    # 获取标题
    title= bs.select(".article-title > h2")[0]
    aNews["title"]= title.text

    # 获取内容
    contentsList= bs.select(".article-content > p >.bjh-p")
    fullContent=""
    for i in range(0,len(contentsList)):
        fullContent=fullContent+ contentsList[i].text
    aNews["content"]= fullContent

    '''
    获取评论：
    没评论？？？
    '''

    allNews.append(aNews)
    for item  in allNews:
        print(item)

    return

def saveData(datalist,savepath):
    '''
    :param savepath: 储存路径
    :return: Null
    '''
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet= book.add_sheet('疫情新闻',cell_overwrite_ok=True)
    col= ('新闻链接',"新闻标题","新闻内容","评论1","评论2","评论3","评论4","评论5","评论6")
    print(len(datalist))
    for i in range(0,9):
        sheet.write(0,i,col[i])
    for i in range(0,2):
        print("第%d条" %(i+1))
        data= datalist[i]
        for j in range(0,9):
            sheet.write(i+1,j,data[j])
    book.save(savepath)
    return











if __name__=="__main__":
    getLink("http://so.news.cn/#search/0/%E7%96%AB%E6%83%85/1")