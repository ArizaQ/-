import requests
import re

from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47"}
baseurl = 'https://m.weibo.cn/comments/hotflow?id=4581579726788695&mid=4581579726788695&max_id_type=0&page='
allNews=[]

# def sina():
#     head = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47"}
#     baseurl = 'https://m.weibo.cn/comments/hotflow?id=4581579726788695&mid=4581579726788695&max_id_type=0&page='
#     ii=0
#     while ii<= 100:
#         ii+=1
#         url= baseurl+str(ii)
#         print('asking:'+url)
#         html = requests.get(url, headers=head)
#         content_json = html.json()
#         print(content_json)
#         for cnt in range(0,len(content_json['data']['data'])):
#             print(''.join(re.findall('[\\u4e00-\\u9fa5]' , content_json['data']['data'][cnt]['text'])))
#             # 提取英文： [a-zA-Z]
#         break
#         # for jj in range(0,len(content_json['data'])):# len:字典的长度
#         #     data = content_json['data'][jj]['text']  # 评论信息
#         #     with open(r'D:\数据科学作业\CrawlerCovid19Weibo\test\sina\weibo.txt') as ff:
#         #         # 提取汉字
#         #         hanzi= ''.join(re.findall('[\\u4e00-\\u9fa5]' , data))  # 正则的汉字的编码范围
#         #         ff.write(hanzi+'\n')
def getAllNews():
    baseurlNews= 'https://m.weibo.cn/api/container/getIndex?containerid=2304132656274875_-_WEIBO_SECOND_PROFILE_WEIBO&luicode=10000011&lfid=2302832656274875&type=uid&value=2656274875'
    cnt=0
    while cnt<10:
        url= baseurl+str(cnt)
        html = requests.get(url, headers=head)
        content_json = html.json()
        for cnt in range(0,len(content_json['data']['data'])):
            print(''.join(re.findall('[\\u4e00-\\u9fa5]' , content_json['data']['data'][cnt]['text'])))
            # 提取英文： [a-zA-Z]
        break

# def getANews(newsHtml):
#     bs = BeautifulSoup(newsHtml, "html.parser")
#     content = bs.select('.weibo - text').text
#     return content
#
# def getComment(newsHtml):
#     baseurl = 'https://m.weibo.cn/comments/hotflow?id=4581579726788695&mid=4581579726788695&max_id_type=0&page='
#     ii = 0
#     comments= []
#     while ii <= 5:
#         ii += 1
#         url = baseurl + str(ii)
#         print('asking:' + url)
#         html = requests.get(url, headers=head)
#         content_json = html.json()
#         print(content_json)
#         for cnt in range(0, len(content_json['data']['data'])):
#             comments.append(''.join(re.findall('[\\u4e00-\\u9fa5]', content_json['data']['data'][cnt]['text'])))
#             print(''.join(re.findall('[\\u4e00-\\u9fa5]', content_json['data']['data'][cnt]['text'])))
#             # 提取英文： [a-zA-Z]
#     return comments
#
# def getDetail(newsHtml):
#     url = baseurl + '0'
#     bs = BeautifulSoup(newsHtml, "html.parser")
#     transmitCnt=bs.select('.tab-item > i')
#     commrntCnt= bs.select('.tab-item cur > i')
#     favorCnt= bs.select()
getAllNews()