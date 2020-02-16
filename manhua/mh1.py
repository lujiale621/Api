import requests
from lxml import etree
import execjs
import re
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
}
def jstest(url):
    try:
        xqq = requests.get(url, headers=header)
        if xqq.status_code != 200:
            return ''
        st = xqq.content.decode('utf-8')
        html = etree.HTML(st)
        htmltxt = etree.tostring(html, encoding='GBK').decode("GBK")
        st = re.findall('qTcms_S_m_murl_e=".*"', htmltxt)
        par = st[0]
        data = re.findall('".*"', par)[0].replace('\"','')
        with open('mh1.js') as f:
            jsdata = f.read()

        ctx = execjs.compile(jsdata)
        pictures=ctx.call('base64_decode',data)
        list=pictures.split("$qingtiandy$");
        print(list)
    except:
        return ''
def searchmanhua(nrl):  # 输入搜索内容
    try:
            url = "https://www.imanhuaw.com/statics/search.aspx?key="+nrl
            xqq = requests.get(url, headers=header)
            if xqq.status_code != 200:
                return '网络请求超时'
            st = xqq.content.decode('utf-8')
            html = etree.HTML(st)
            lists=html.xpath('//ul[@class="mh-search-list searchrest clearfix"]//li')
            covers=[]
            titles=[]
            links=[]
            lastupdatatimes=[]
            status=[]
            types=[]
            collects=[]
            dianzhans=[]
            renqis=[]
            briefs=[]
            for list in lists:
                link=list.xpath('.//div[@class="mh-nlook-w"]//a/@href')
                cover=list.xpath('.//img/@src')
                title=list.xpath('.//img/@title')
                lastupdatatime=list.xpath('.//p[@class="mh-up-time fr"]/text()')
                statu=list.xpath('.//p[@class="mh-works-author"]/text()')
                type=list.xpath('.//p[@class="mh-works-tags"]//a/text()')
                collect=list.xpath('.//p[@class="mh-works-tags"]//span[1]//em/text()')
                dianzhan = list.xpath('.//p[@class="mh-works-tags"]//span[2]//em/text()')
                renqi = list.xpath('.//p[@class="mh-works-tags"]//span[3]//em/text()')
                brief = list.xpath('.//p[@class="mh-works-decs"]/text()')
                links.append(link)
                covers.append(cover)
                titles.append(title)
                lastupdatatimes.append(lastupdatatime)
                status.append(statu)
                types.append(type)
                collects.append(collect)
                dianzhans.append(dianzhan)
                renqis.append(renqi)
                briefs.append(brief)
            sult = []
            for (title, cover, link, lastupdatatime, statu, type, collect, dianzhan, renqi, brief) in zip(titles, covers, links, lastupdatatimes, status, types, collects,
                                  dianzhans, renqis, briefs):
                sult.append({'title': title, 'cover': cover, 'link': link, 'lastupdatatime': lastupdatatime, 'statu': statu,
                             'type': type, 'collect': collect, 'dianzhan': dianzhan,
                             'renqi': renqi, 'brief': brief})
            return sult
    except:
        return ''

def manhuadetail(nrl):
    try:
        url = "https://www.imanhuaw.com" + nrl
        xqq = requests.get(url, headers=header)
        if xqq.status_code != 200:
            return '网络请求超时'
        st = xqq.content.decode('utf-8')
        html = etree.HTML(st)
        links=html.xpath('//div[@class="cy_plist"]//ul//li/a/@href')
        arts=html.xpath('//div[@class="cy_plist"]//ul//li//p/text()')
        sult=[]
        for (link,art) in zip(links,arts):
            sult.append({'href':link,'name':art})
        return sult
    except:
        return ''
def manhuacontent(nrl):
    try:
        url = "https://www.imanhuaw.com" + nrl
        xqq = requests.get(url, headers=header)
        if xqq.status_code != 200:
            return '网络请求超时'
        st = xqq.content.decode('utf-8')
        html = etree.HTML(st)
        htmltxt = etree.tostring(html, encoding='GBK').decode("GBK")
        st = re.findall('qTcms_S_m_murl_e=".*"', htmltxt)
        par = st[0]
        data = re.findall('".*"', par)[0].replace('\"', '')
        with open('manhua/mh1.js') as f:
            jsdata = f.read()

        ctx = execjs.compile(jsdata)
        pictures = ctx.call('base64_decode', data)
        lists = pictures.split("$qingtiandy$");
        sult=[]
        for (link) in zip(lists):
            sult.append({'picture':link})
        return sult
    except:
        return ''
def manhuasort(arg):
    url="https://www.imanhuaw.com/imanhua"+arg
    xqq = requests.get(url, headers=header)
    if xqq.status_code != 200:
        return '网络请求超时'
    st = xqq.content.decode('utf-8')
    html = etree.HTML(st)
    test=etree.tostring(html, encoding='utf-8').decode("utf-8")
    print(test)
    sult=[]
    newcovers=[]
    newtitles=[]
    newupdata=[]
    newhref=[]
    newstatus=[]
    newtypes=[]
    newauthors=[]
    news=html.xpath('/html/body/div[2]/div[2]/div/div[2]/ul//li')
    for li in news:
        href=li.xpath('./div[1]/div/p/a/@href')
        title=li.xpath('./div[1]/div/div/a/img/@title')
        cover=li.xpath('./div[1]/div/div/a/img/@src')
        updata=li.xpath('./div[1]/div/p/a/span/text()')
        author=li.xpath('./div[2]/p[2]/span/text()')
        type=li.xpath('./div[2]/p[2]/a/text()')
        status=li.xpath('./div[2]/p[1]/text()')
        newcovers.append(cover)
        newtitles.append(title)
        newupdata.append(updata)
        newhref.append(href)
        newauthors.append(author)
        newtitles.append(title)
        newstatus.append(status)
        newtypes.append(type)
    news=[]
    for (cover, title,updata,href,author,title,type,status) in zip(newcovers, newtitles,newupdata,newhref,newauthors,newtitles,newstatus,newtypes):
        news.append({'cover': cover, 'titles': title,'updatatime':updata,'href':href,'author':author,'title':title,'status':status,'type':type})
    return news
if __name__ == '__main__':
    # print(searchmanhua('斗罗大陆'))
    # print(manhuadetail('/imanhua/douluodalu3longwangchuanshuo/'))
    print(manhuacontent('/imanhua/douluodalu3longwangchuanshuo/178868.html'))