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
baseurl=r'https://weibo.cn/cctvxinwen?page='
# aNews= {} # {"link":"http://www.wiki.com","title":"covid19 is good","content":"XXXXXXXX","comment":"happy angry fuck it","":"","":""}
allNews=[]
allNewsContent=[]
def main():
    i=1350;
    j=3;

    path= [".\\NewsWeibo0.xls",".\\NewsWeibo1.xls",".\\NewsWeibo2.xls",".\\NewsWeibo3.xls",".\\NewsWeibo4.xls",".\\NewsWeibo5.xls",".\\NewsWeibo6.xls",".\\NewsWeibo7.xls",".\\NewsWeibo8.xls",".\\NewsWeibo9.xls",".\\NewsWeibo10.xls",".\\NewsWeibo11.xls",".\\NewsWeibo12.xls",".\\NewsWeibo13.xls",".\\NewsWeibo14.xls",".\\NewsWeibo15.xls",".\\NewsWeibo16.xls",".\\NewsWeibo17.xls",".\\NewsWeibo18.xls",".\\NewsWeibo19.xls"]
    while i<=2250:
        doing(i,path[j])
        i+=100
        j+=1
        allNews.clear()
    return
def doing(i,path):
    # savepath = ".\\NewsWeibo.xls"
    page = i
    while True:
        # 先爬100页
        if(page>i+99): break
        # 每一页的链接
        url = baseurl + str(page)
        print("访问页面：" + str(page) + "Link:" + url)
        # 每一页中所有新闻链接的list
        newsLinkAPage = getLink(url)
        # print(newsLinkAPage)
        if len(newsLinkAPage) == 0:  # 没有新闻了！
            print('没有新闻了！')
            continue
        if len(newsLinkAPage) != 0:
            for aNewsLink in newsLinkAPage:
                getAData(aNewsLink)  # 一个详情页的链接
        page += 1
    print(len(allNews))
    saveData(allNews, path)

    # print(html)
    #print(html)


    return
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
def getAData(newsPage):
    aNews = {}  # {"link":"http://www.wiki.com","title":"covid19 is good","content":"XXXXXXXX","comment1":"happy","comment2":"angy","comment3":"fuck it","comment4":"dont care","comment5":"sad","comment6":"positive"}
    newsHtml = askURL(newsPage)
    bs = BeautifulSoup(newsHtml, "html.parser")

    # 日期
    print('getting date:')
    date = bs.select("div > span.ct")
    if(len(date)!=0) :
        date=date[0]
        aNews["date"] = date.text
    else:
        aNews["date"] ="no date"

    # print(aNews["date"])
    # 正文
    print('getting content:')
    contents= bs.select("div > span.ctt")
    fullContent=''
    if(len(contents)!=0):
        contents=contents[0]
        fullContent = contents.text
    else:
        fullContent="no content"
    # print(contents.text)
    aNews["content"]= fullContent
    # print(fullContent)
    #点赞数 转发数
    print("getting cnts:")
    cntFusion= bs.select("div > span > a")
    cntFusions=[]
    for fusion in cntFusion:
        cntFusions.append(fusion.text)
    temp=1
    isZhuanfa=False
    isDianzan=False
    for fusion in cntFusions:
        if "转发[" in fusion:

            aNews["转发数"]=getNumber(fusion)
            isZhuanfa=True
            temp+=1
        if "赞[" in fusion:
            aNews["点赞数"]= getNumber(fusion)
            isDianzan=True
            temp+=1
        if temp>=3: break
    if isDianzan==False:
        aNews["点赞数"] = 0
    if isZhuanfa==False:
        aNews["转发数"] = 0

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
    allNews.append(aNews)
    return aNews

def getNumber(fusion):
    str = re.findall(r'\d', fusion)
    date = ''
    for ch in str:
        date = date + ch
    # print(date)
    return date


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
    col= ('新闻日期',"转发数","点赞数","新闻内容","评论1","评论2","评论3","评论4","评论5","链接",)
    print(len(datalist))
    for i in range(0,10):
        sheet.write(0,i,col[i])

    for i in range(0,len(datalist)):
        print("第%d条" %(i+1))
        data= datalist[i]
        sheet.write(i + 1, 0, data["date"])
        sheet.write(i + 1, 1, data["转发数"])
        sheet.write(i + 1, 2, data["点赞数"])
        sheet.write(i + 1, 3, data["content"])
        sheet.write(i + 1, 4, data["comment0"])
        sheet.write(i + 1, 5, data["comment1"])
        sheet.write(i + 1, 6, data["comment2"])
        sheet.write(i + 1, 7, data["comment3"])
        sheet.write(i + 1, 8, data["comment4"])
        sheet.write(i + 1, 9, data["link"])
    book.save(savepath)
    return

def saveSimple(datalist,savepath):
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