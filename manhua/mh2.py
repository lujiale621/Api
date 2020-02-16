import requests
from lxml import etree
import threading
import re

import json

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
}

def searchmanhua(nrl):  # 输入搜索内容
    try:
            url = "https://m.tohomh123.com/action/Search?keyword="+nrl
            xqq = requests.get(url, headers=header)
            if xqq.status_code != 200:
                return '网络请求超时'
            st = xqq.content.decode('utf-8')
            html = etree.HTML(st)
            lists=html.xpath('//div[@class="classList"]//ul/li')
            covers=[]
            titles=[]
            links=[]
            lastupdatatimes=[]
            for list in lists:
                link=list.xpath('.//a[1]/@href')[0]
                cover=list.xpath('.//img/@src')
                title=list.xpath('.//img/@alt')
                lastupdata=list.xpath('.//span/text()')
                links.append(link)
                covers.append(cover)
                titles.append(title)
                lastupdatatimes.append(lastupdata)
            sult = []
            for (title, cover, link, lastupdata) in zip(titles, covers, links, lastupdatatimes):
                sult.append({'title': title, 'cover': cover, 'link': link, 'lastupdata': lastupdata})
            return sult
    except Exception as e:
        print(e)
        return ''

def manhuadetail(nrl):
    try:
        url = "https://m.tohomh123.com" + nrl
        xqq = requests.get(url, headers=header)
        if xqq.status_code != 200:
            return '网络请求超时'
        st = xqq.content.decode('utf-8')
        html = etree.HTML(st)
        cover=html.xpath('//div[@class="coverForm"]//img/@src')
        title=html.xpath('//div[@class="info d-item-content"]//h1/text()')
        types=html.xpath('//div[@class="info d-item-content"]//p[1]//a/text()')
        type=''
        for st in types:
            type=type+st+""
        author=html.xpath('//div[@class="info d-item-content"]//p[2]/text()')
        updatatime=html.xpath('//div[@class="info d-item-content"]//p[3]/text()')
        lastart=html.xpath('//div[@class="info d-item-content"]//p[4]/text()')
        links=html.xpath('//div[@class="chapters"]//ul//li/a/@href')
        arts=html.xpath('//div[@class="chapters"]//ul//li/a/text()')
        brief=html.xpath('//div[@class="detailContent"]//p[1]/text()')
        sult=[]
        sult.append({'title': title,'cover':cover, 'type': type, 'author': author, 'updatatime': updatatime, 'lastart': lastart,
                     'brief': brief})
        for (link,art) in zip(links,arts):
            sult.append({'href':link,'art':art})
        return sult
    except:
        return ''
def manhuacontent(nrl):
    try:
        ajsxurl="https://m.tohomh123.com/action/play/read"
        url = "https://m.tohomh123.com" + nrl
        xqq = requests.get(url, headers=header)
        if xqq.status_code != 200:
            return '网络请求超时'
        st = xqq.content.decode('utf-8')
        html = etree.HTML(st)
        js=html.xpath('//script[@type="text/javascript"]/text()')[0]
        did = re.findall('did=.*;', js)   #did
        sid = re.findall('sid=.*;', js)   #sid
        iid = re.findall('iid =.*;', js)  #请求页数
        pcount=re.findall('pcount=.*;', js)#这一章总共有多少张图
        ardid=re.search(r'[0-9]+',did[0]).group()
        arsid = re.search(r'[0-9]+', sid[0]).group()
        ariid = re.search(r'[0-9]+', iid[0]).group()
        arpcount = re.search(r'[0-9]+', pcount[0]).group()
        sult=[]
        pictures=[]
        sult.append({'did':ardid,'sid':arsid,'iid':ariid,'pcount':arpcount,'ajsxurl':ajsxurl})
        thread(arpcount,ardid,arsid,ajsxurl,pictures)
        sult.append(pictures)
        return sult
    except Exception as e:
        print(e)
        return ''
def getre(ardid,arsid,index,ajsxurl,pictures):
    try:
        data = {'did': ardid, 'sid': arsid, 'iid': index}
        xqq = requests.get(ajsxurl, data=data, headers=header, timeout=3)
        st = xqq.content.decode('utf-8')
        pictures.append(st)
    except:
        st='{"IsError":false,"MessageStr":null,"errorid":'+str(index)+'}'
        pictures.append(st)

def thread(arpcount,ardid,arsid,ajsxurl,pictures):
    threads=[]
    for index in range(0,int(arpcount)):
        t=threading.Thread(target=getre,args=(ardid,arsid,index,ajsxurl,pictures))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
#返回最新更新和最热们 5个参数
def manhuasort(arg):
    url="https://m.tohomh123.com/"+arg
    xqq = requests.get(url, headers=header)
    if xqq.status_code != 200:
        return '网络请求超时'
    st = xqq.content.decode('utf-8')
    html = etree.HTML(st)
    sult=[]
    newcovers=[]
    newtitles=[]
    newupdata=[]
    newhref=[]
    news=html.xpath('//div[@id="classList_1"]//li')
    for li in news:
        href=li.xpath('./a/@href')
        title=li.xpath('./a/@title')
        cover=li.xpath('.//img/@src')
        updata=li.xpath('.//span[@class="tip"]/text()')
        newcovers.append(cover)
        newtitles.append(title)
        newupdata.append(updata)
        newhref.append(href)
    news=[]
    for (cover, title,updata,href) in zip(newcovers, newtitles,newupdata,newhref):
        news.append({'cover': cover, 'titles': title,'updatatime':updata,'href':href})
    hotcovers=[]
    hottitles=[]
    hotupdata=[]
    hothref=[]
    hots=html.xpath('//div[@id="classList_2"]//li')
    for li in hots:
        href=li.xpath('./a/@href')
        title=li.xpath('./a/@title')
        cover=li.xpath('.//img/@src')
        updata=li.xpath('.//span[@class="tip"]/text()')
        hotcovers.append(cover)
        hottitles.append(title)
        hotupdata.append(updata)
        hothref.append(href)
    hots=[]
    for (cover, title,updata,href) in zip(hotcovers, hottitles,hotupdata,hothref):
        hots.append({'cover': cover, 'titles': title,'updatatime':updata,'href':href})
    sult.append(news)
    sult.append(hots)
    return sult
if __name__ == '__main__':
    # print(searchmanhua('斗罗大陆'))
    # print(manhuadetail('/douluodaliu/'))
    # print(manhuacontent('/douluodaliu/653.html'))
    print(manhuasort("f-1------updatetime--3.html"))