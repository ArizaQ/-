import bs4  # 网页解析 获取数据
import re  # 文字匹配
import urllib.request, urllib.error  # 指定url
import xlwt  # excel操作
import sqlite3  # 数据库操作
from bs4 import BeautifulSoup

'''

爬取新浪新闻
只能得到一天的数据：所有网页只有40多页，全是2020.12.7！！！


'''

# baseurl= "https://search.sina.com.cn/?q=%e7%96%ab%e6%83%85&c=news&from=index&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page="
baseurl=r"http://sou.cyol.com/servlet/SearchServlet.do?isall=1&allContentKey=%E7%96%AB%E6%83%85&contentKey=%E7%96%AB%E6%83%85&titleKey=%E7%96%AB%E6%83%85&authorKey=%E7%96%AB%E6%83%85&nodeNameResult=&subNodeResult=&dateFrom=20191201&dateEnd=20200625&sort=date&op=adv&paperName=%E4%B8%AD%E5%9B%BD%E9%9D%92%E5%B9%B4%E6%8A%A5&siteID=&nodeID=0&pager.offset=0&pageNo="
# aNews= {} # {"link":"http://www.wiki.com","title":"covid19 is good","content":"XXXXXXXX","comment":"happy angry fuck it","":"","":""}
allNews=[]
def main():
    savepath = ".\\NewsZWQ.xls"
    page = 1
    while True:
        # 先爬100页
        # if(page>10): break
        # 每一页的链接
        url = baseurl +str(page)
        print("访问页面："+str(page)+"Link:"+url)
        # 每一页中所有新闻链接的list
        newsLinkAPage=getLink(url)
        # print(newsLinkAPage)
        if len(newsLinkAPage)==0:  # 没有新闻了！
            print('没有新闻了！')
            break
        for aNewsLink in newsLinkAPage:
            getAData(aNewsLink)# 一个详情页的链接
        page+=1

    print(len(allNews))
    saveData(allNews,savepath)
    #print(html)


    return
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
    print(len(newsLinks))
    return newsLinks
def getAData(newsPage):

    aNews = {}  # {"link":"http://www.wiki.com","title":"covid19 is good","content":"XXXXXXXX","comment1":"happy","comment2":"angy","comment3":"fuck it","comment4":"dont care","comment5":"sad","comment6":"positive"}
    newsHtml = askURL(newsPage)
    bs = BeautifulSoup(newsHtml, "html.parser")

    # 日期
    date = bs.select(".lai")[0]
    str= re.findall(r'\d',date.text)
    date=''
    for ch in str:
        date=date+ch
    # print(date)
    aNews["date"] = date[:-2]
    # print(aNews["date"])

    # 标题
    # title= bs.select(".main-title")[0]
    title= bs.select(".text_c > h1")
    # print(title[0].text)
    aNews["title"]= title[0].text

    # 正文
    contentsList= bs.select("#ozoom > p")
    # print(contentsList)
    fullContent=""
    for i in range(0,len(contentsList)):
        fullContent=fullContent+ contentsList[i].text.strip()
    aNews["content"]= fullContent
    # print(fullContent)

    # 评论
    # 没有网友愿意评论新浪新闻。。。
    aNews["comment"]= "not a word."
    # 链接
    aNews["link"] = newsPage
    print(aNews)
    allNews.append(aNews)
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
    col= ('新闻日期',"新闻标题","新闻内容","评论","链接",)
    print(len(datalist))
    for i in range(0,5):
        sheet.write(0,i,col[i])

    for i in range(0,len(datalist)):
        print("第%d条" %(i+1))
        data= datalist[i]
        sheet.write(i+1,0,data["date"])
        sheet.write(i + 1, 1, data["title"])
        sheet.write(i + 1, 2, data["content"])
        sheet.write(i + 1, 3, data["comment"])
        sheet.write(i + 1, 4, data["link"])
    book.save(savepath)
    return
if __name__=="__main__":
    main()