import bs4  # 网页解析 获取数据
import re  # 文字匹配
import urllib.request, urllib.error  # 指定url
import xlwt  # excel操作
import sqlite3  # 数据库操作
from bs4 import BeautifulSoup


aNewsLink= r'http://data.people.com.cn//rmrb/pd.html?qs=%7B%22cds%22%3A%5B%7B%22cdr%22%3A%22AND%22%2C%22cds%22%3A%5B%7B%22fld%22%3A%22title%22%2C%22cdr%22%3A%22OR%22%2C%22hlt%22%3A%22true%22%2C%22vlr%22%3A%22OR%22%2C%22val%22%3A%22%E7%96%AB%E6%83%85%22%7D%2C%7B%22fld%22%3A%22subTitle%22%2C%22cdr%22%3A%22OR%22%2C%22hlt%22%3A%22true%22%2C%22vlr%22%3A%22OR%22%2C%22val%22%3A%22%E7%96%AB%E6%83%85%22%7D%2C%7B%22fld%22%3A%22introTitle%22%2C%22cdr%22%3A%22OR%22%2C%22hlt%22%3A%22true%22%2C%22vlr%22%3A%22OR%22%2C%22val%22%3A%22%E7%96%AB%E6%83%85%22%7D%2C%7B%22fld%22%3A%22contentText%22%2C%22cdr%22%3A%22OR%22%2C%22hlt%22%3A%22true%22%2C%22vlr%22%3A%22OR%22%2C%22val%22%3A%22%E7%96%AB%E6%83%85%22%7D%5D%7D%5D%2C%22obs%22%3A%5B%7B%22fld%22%3A%22dataTime%22%2C%22drt%22%3A%22DESC%22%7D%5D%7D&tr=Y&pageNo=1&pageSize=50&position=0'
allNews=[]


def askURL(url):
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
        print('wrong in askUrl in one news')
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    # print(html)

    return html


def getAData(newsPage):

    aNews = {}  # {"link":"http://www.wiki.com","title":"covid19 is good","content":"XXXXXXXX","comment1":"happy","comment2":"angy","comment3":"fuck it","comment4":"dont care","comment5":"sad","comment6":"positive"}
    newsHtml = askURL(newsPage)
    bs = BeautifulSoup(newsHtml, "html.parser")

    # 日期
    date = bs.select(".sha_left> span")[0]
    # print(date.text)
    aNews["date"] = date.text

    # 标题
    # title= bs.select(".main-title")[0]
    title= bs.select(".title")
    # print(title[0].text)
    aNews["title"]= title[0].text

    # 正文
    contentsList= bs.select(".detail_con > p")
    # print(contentsList)
    fullContent=""
    for i in range(0,len(contentsList)):
        fullContent=fullContent+ contentsList[i].text.strip()
    aNews["content"]= fullContent
    print(fullContent)

    # 评论
    # 没有网友愿意评论新浪新闻。。。
    # 链接
    aNews["link"] = newsPage
    return aNews




    # # 获取内容
    # contentsList= bs.select(".article-content > p >.bjh-p")
    # fullContent=""
    # for i in range(0,len(contentsList)):
    #     fullContent=fullContent+ contentsList[i].text
    # aNews["content"]= fullContent
    #
    # '''
    # 获取评论：
    # 没评论？？？
    # '''
    # allNews.append(aNews)
    #
    # for key,value  in aNews.items():
    #     print(key+" : "+value)


def saveData(datalist,savepath):
    '''
    :param savepath: 储存路径
    :return: Null
    '''
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet= book.add_sheet('疫情新闻',cell_overwrite_ok=True)
    col= ('新闻链接',"新闻标题","新闻内容","评论1","评论2","评论3","评论4","评论5","评论6")
    print(len(datalist))
    for i in range(0,3):
        sheet.write(0,i,col[i])

    # data= datalist[0]
    data = datalist
    sheet.write(1,0,data["link"])

    book.save(savepath)
    return



# def getData(newsPage):
#     jobHtml= askURL(newsPage)
#     bs = BeautifulSoup(jobHtml, "html.parser")
#     for job in jobList:
#         if newsPage== job["link"]:
#             jNames = bs.select(".cn > h1")
#             job["title"]=jNames["title"][0]
#             cnameList= bs.select(".cname a")
#             job["cname"]= cnameList[0].text
#
#             jobMsgList= bs.select(".job_msg > p")
#             jobMsgStr= ""
#             for str in jobMsgList:
#                 jobMsgStr= jobMsgStr+str.text
#             job["jobMsg"]= jobMsgStr
#             days = bs.select(".ltype")
#             info = days[0]["title"].split("|")
#
#             job["jobInfo"]= info[4].strip()[0:5]
#
#
#     return

if __name__=="__main__":


    saveData(getAData(aNewsLink),".\\covid19News.xls")
    # saveData(allNews,".\\covid19News.xls")
