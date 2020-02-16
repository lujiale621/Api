import requests
from lxml import etree
from urllib.parse import urlencode
import re
import execjs
header = {
    "Content-Type":"application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
}
def getanime(nr1):
    try:
        url = "http://www.imomoe.in/search.asp"
        print(url)
        d = {'searchword': nr1}
        data_gb2312 = urlencode(d, encoding='gb2312')
        xqq = requests.post(url, data=data_gb2312, headers=header)
        if xqq.status_code != 200:
            return '网络请求超时'
        st = xqq.content.decode('GBK')
        html = etree.HTML(st)
        # htmltxt = etree.tostring(html, encoding='GBK').decode("GBK")
        html=html.xpath('//div[@class="area"]//div[@class="pics"]')[0]
        titles=html.xpath('.//li//h2/a/text()')
        views=html.xpath('.//li/a/@href')
        covers=html.xpath('.//li//img/@src')
        alias=[]
        statusandtypes=[]
        res=html.xpath('.//li')
        for si in res:
            a=si.xpath('.//span/text()')[0]
            alias.append(a)
            b=si.xpath('.//span/text()')[1]
            statusandtypes.append(b)
        briefs=html.xpath('.//li//p/text()')
        print(briefs)
        sult=[]
        for (title, view, cover, alia,statusandtype,brief ) in zip(titles, views, covers, alias, statusandtypes,briefs):
            sult.append({'title': title, 'url': view, 'cover': cover, 'cover': cover,'statusandtype': statusandtype, 'brief': brief})
        return sult
    except:
        return ''
def geturl(url):
    try:
        url="http://www.imomoe.in"+url
        xqq = requests.get(url, headers=header)
        if xqq.status_code != 200:
            return '网络请求超时'
        st = xqq.content.decode('GBK')
        html = etree.HTML(st)
        htmltxt = etree.tostring(html, encoding='GBK').decode("GBK")
        links = html.xpath('//div[@id="play_0"]//li/a/@href')
        titles=html.xpath('//div[@id="play_0"]//li/a/@title')
        sult=[]
        for (title, link) in zip(titles, links):
            sult.append({'title': title, 'link': link})
        return sult
    except:
        return ''

def getview(url):
    try:
        url = "http://www.imomoe.in" + url
        xqq = requests.get(url, headers=header)
        if xqq.status_code != 200:
            return '网络请求超时'
        st = xqq.content.decode('GBK')
        html = etree.HTML(st)
        js=html.xpath('//div[@class="player"]//script[1]/@src')[0]
        jsurl = "http://www.imomoe.in"+js
        xqqjs = requests.get(jsurl, headers=header)
        if xqqjs.status_code != 200:
            return '网络请求超时'
        s = xqqjs.content.decode('GBK')
        ht = etree.HTML(s)
        jscode = etree.tostring(ht, encoding='utf-8').decode("utf-8")
        urllists=jscode.split("$")
        mp4 = re.compile(r'[a-zA-z]+://[^\s]*\.mp4$')
        m3u8 = re.compile(r'[a-zA-z]+://[^\s]*\.m3u8$')
        qq = re.compile(r'http://quan.qq.com/video/+')
        sult=[]
        mp4s=[]
        m3u8s=[]
        qqs=[]
        for url in urllists:
            m=mp4.match(url)
            if(m!=None):
                mp4s.append(m.string)
            s=m3u8.match(url)
            if(s!=None):
                m3u8s.append(s.string)
            d = qq.match(url)
            if(d!=None):
                qqs.append(d.string)
        sult.append({'m3u8s': m3u8s,'mp4s':mp4s,'qqs':qqs})
        return sult
    except:
        return ''
if __name__ == '__main__':
    print(getview('/player/7346-0-42.html'))