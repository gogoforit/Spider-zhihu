import requests
import re
import login
from MongodbConn import MongoPipeline
# def solve(info):
if __name__ =="__main__":
    conn = MongoPipeline()
    conn.open_connection('zhihu')
    info = input("请输入搜索内容:\n")
    url = 'https://www.zhihu.com/r/search?q=' + str(info) +  '&type=people&offset=10'

    #请求头
    header = {
    'Host':"www.zhihu.com",
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    'Accept':"*/*",
    'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'Accept-Encoding':"gzip, deflate, br",
    'X-Requested-With':"XMLHttpRequest",
    'Connection':"keep-alive"
    }

    finallyUrlList = []  #用于存入所有的用户url

    #处理第一页的信息
    html = requests.get(url,headers = header).text
    nexturl = re.findall('"next":"(.*?)"}',html,re.S)[0].replace("\\",'')
    urllist = re.findall("data-id=(.*?)>",html,re.S)
    for each in urllist:
        k = each.replace('\\', '').replace('\"', '')
        k = 'https://www.zhihu.com/people/'+k
        finallyUrlList.append(k)
        print(k)

    #循环，直到下一页为空为止
    while (nexturl!=None):

        nexturl = 'https://www.zhihu.com'+ nexturl
        html2 = requests.get(nexturl, headers=header).text

        print(nexturl)
        urllist = re.findall("data-id=(.*?)>",html2,re.S)
        for each in urllist:
            k = each.replace('\\','').replace('\"','')
            k = 'https://www.zhihu.com/people/' + k
            finallyUrlList.append(k)
            print(k)
        try:
            nexturl = re.findall('"next":"(.*?)"}',html2,re.S)[0].replace("\\",'')
        except:
            nexturl = None
    for each in finallyUrlList:
        dic = {}
        dic['url'] = each
        dic['flag'] = False
        dic['type'] = 'url'
        conn.process_item(dic,'info')
    # return finallyUrlList
    # login.send(finallyUrlList)