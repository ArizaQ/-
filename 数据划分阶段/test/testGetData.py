import bs4  # 网页解析 获取数据
import re  # 文字匹配
import urllib.request, urllib.error  # 指定url
import xlwt  # excel操作
import sqlite3  # 数据库操作
from bs4 import BeautifulSoup


aNewsLink= r'https://weibo.cn/comment/Jyegcsu35?uid=2656274875&rl=0#cmtfrm'
allNews=[]


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


def getAData(newsPage):
    aNews = {}  # {"link":"http://www.wiki.com","title":"covid19 is good","content":"XXXXXXXX","comment1":"happy","comment2":"angy","comment3":"fuck it","comment4":"dont care","comment5":"sad","comment6":"positive"}
    newsHtml = askURL(newsPage)
    bs = BeautifulSoup(newsHtml, "html.parser")

    # 日期
    print('getting date:')
    date = bs.select("div > span.ct")[0]
    aNews["date"]= date.text
    print(aNews["date"])
    # 正文
    print('getting content:')
    contents= bs.select("div > span.ctt")[0]
    print(contents.text)
    fullContent=contents.text
    aNews["content"]= fullContent
    # print(fullContent)
    #点赞数 转发数
    print("getting cnts:")
    cntFusion= bs.select("div > span > a")
    cntFusions=[]
    for fusion in cntFusion:
        cntFusions.append(fusion.text)
    temp=1
    for fusion in cntFusions:
        if "转发[" in fusion:
            aNews["转发数"]=fusion
            temp+=1
        if "赞[" in fusion:
            aNews["点赞数"]= fusion
            temp+=1
        if temp>=3: break
    print(cntFusions)

    # aNews["转发数"]=
    # aNews["点赞数"]=


    # 评论
    print('getting comments:')
    raw_comments= bs.select("div.c > span.ctt")
    comments=[]
    for comment in raw_comments:
        comments.append(comment.text)
    commentNum=5;
    if len(comments)<5 :
        commentNum=len(comments)
    for i in range(0,commentNum):
        strTemp="comment"+str(i)
        aNews[strTemp]= comments[i]
    for i in range(commentNum,5):
        strTemp = "comment" + str(i)
        aNews[strTemp] = "no more comments"
    # aNews["comments"]= comments
    print(comments)
    # 链接
    aNews["link"] = newsPage
    print(aNews)
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

    getAData(aNewsLink)
    # saveData(getAData(aNewsLink),".\\covid19News.xls")
    # saveData(allNews,".\\covid19News.xls")
