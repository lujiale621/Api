import requests
from lxml import etree
import execjs
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
}
def getnv(nr1):  # 输入搜索内容
    try:
        # nr1 = quote(nr1)
        url="http://www.5wx.org/modules/article/search.php"
        d = {'searchkey': nr1, 'searchtype': 'articlename'}
        xqq = requests.post(url,data=d,headers=header)
        if xqq.status_code != 200:
            return '网络请求超时'
        st = xqq.content.decode('utf-8')
        html = etree.HTML(st)
        # 链接
        # nr1 = quote(nr1)
        url="http://www.5wx.org/modules/article/search.php"
        d = {'searchkey': nr1, 'searchtype': 'articlename'}
        xqq = requests.post(url,data=d,headers=header)
        if xqq.status_code != 200:
            return ''
        hrefs = html.xpath('//div[@class="listIndexUpdata"]//ul/a/@href')
        pictures=html.xpath('//div[@class="listIndexUpdata"]//ul/a//img/@src')
        booknames = html.xpath('//div[@class="listIndexUpdata"]//ul//img/@alt')
        briefs = html.xpath('//div[@class="listIndexUpdata"]//ul//li[@style="height:55px;overflow: hidden;margin-top:5px;"]/text()')
        lastupdatachapters = html.xpath('//div[@class="listIndexUpdata"]//ul//font//b/text()')
        infos=html.xpath('//div[@class="listIndexUpdata"]//ul//li[@style="margin-bottom:5px;"]')
        authors=[]
        types=[]
        statuss=[]
        updatetimes=[]
        for se in infos:
            s=se.xpath('.//font/text()')[0]
            authors.append(s)
            s1 = se.xpath('.//font/text()')[1]
            types.append(s1)
            s2 = se.xpath('.//font/text()')[2]
            statuss.append(s2)
            s3 = se.xpath('.//font/text()')[3]
            updatetimes.append(s3)
        sult=[]
        for (name, author, url, cover, introduce, lastupdatachapter, updatetime,type,status) in zip(booknames, authors, hrefs, pictures, briefs,lastupdatachapters, updatetimes,types,statuss):
            sult.append({'name': name, 'author': author, 'url': url, 'cover': cover,'introduce': introduce, 'lastupdatachapter': lastupdatachapter,'updatetime': updatetime,'type':type,'status':status})
        return sult
    except:
        return ''


def getmore(url):
    try:
        xqq = requests.get(url,headers=header)
        if xqq.status_code != 200:
            return '网络请求超时'
        st = xqq.content.decode('utf-8')
        html = etree.HTML(st)
        hrefs = html.xpath('//div[@class="articleInfo"]//div[@class="articleInfoLeft"]//a/@href')
        pictures=html.xpath('//div[@class="articleInfo"]//img/@src')
        booknames = html.xpath('//div[@class="articleInfo"]//div[@class="articleInfoRight"]//h1/text()')
        authors=html.xpath('//div[@class="articleInfo"]//div[@class="articleInfoRight"]//b[@style="font-size:12px;"]/text()')
        lastupdatachapters = html.xpath('//div[@class="articleInfo"]//div[@class="articleInfoRight"]//span//a/text()')
        updatatimes=html.xpath('//div[@class="articleInfo"]//div[@class="articleInfoRight"]//dt//span/text()')
        briefs = html.xpath('//div[@class="articleInfo"]//div[@class="articleInfoRight"]//dd/text()')
        info=html.xpath('//div[@class="articleInfo"]//div[@class="articleInfoRight"]//ol/p')[0]
        types=[]
        readers=[]
        recomms=[]
        statuss=[]
        booksizes=[]
        s=info.xpath('./strong/text()')[0]
        types.append(s)
        s1 = info.xpath('./strong/text()')[1]
        readers.append(s1)
        s2 = info.xpath('./strong/text()')[2]
        recomms.append(s2)
        s3 = info.xpath('./strong/text()')[3]
        statuss.append(s3)
        s4 = info.xpath('./strong/text()')[4]
        booksizes.append(s4)
        sult = []
        for (name, author, url, cover, introduce, lastupdatachapter, updatatime,type,status,reader,recomms,booksize) in zip(booknames, authors, hrefs, pictures, briefs,lastupdatachapters, updatatimes,types,statuss,readers,recomms,booksizes):
            sult.append({'name': name, 'author': author, 'url': url, 'cover': cover,'introduce': introduce, 'lastupdatachapter': lastupdatachapter,'updatatime': updatatime,'type':type,'status':status,'readers':readers,'recomms':recomms,'booksizes':booksizes})
        return sult
    except:
        return ''
def getdetail (url):#给页面地址，解出所有章名和地址
    try:
        xqq = requests.get(url, headers=header)
        if xqq.status_code != 200:
            return '网络请求超时'
        st = xqq.content.decode('utf-8')
        html = etree.HTML(st)
        htmltxt = etree.tostring(html, encoding='GBK').decode("GBK")
        # 链接
        # nr1 = quote(nr1)
        sult=[]
        hrefs = html.xpath('//div[@class="readerListBody"]//ul[@id="newlist"]//span/a/@href')
        for (link) in zip(hrefs):
            sult.append({'href':link})
        return sult
    except:
        return ''
def getcontent (url):#给章回地址，进入内容
    try:
        xqq = requests.get(url, headers=header)
        if xqq.status_code != 200:
            return ''
        st = xqq.content.decode('utf-8')
        html = etree.HTML(st)
        ids=html.xpath('//div[@id="content"]//p/@data-id')
        ps=html.xpath('//div[@id="content"]//p')
        contents=[]
        for (id,content) in zip(ids,ps):
            contents.append({'id': int(id),'content':content})
        contents.sort(key=lambda x:x['id'])
        sult=[]
        for (content) in zip(contents):
            ts=content[0]['content'].xpath('.//text()')
            for st in ts:
                sult.append({'content':st.strip()})
        return sult
    except Exception as e:
        print(e)
        return ''

def getrecommend(art):
    try:
        url="http://www.5wx.org/"
        xqq = requests.get(url, headers=header)
        if xqq.status_code != 200:
            return ''
        st = xqq.content.decode('utf-8')
        html = etree.HTML(st)
        titles=html.xpath('//div[@class="indexHot"]//ul//li//strong/text()')
        covers=html.xpath('//div[@class="indexHot"]//ul//li//img/@src')
        briefs=html.xpath('//div[@class="indexHot"]//ul//li//span/text()')
        links=html.xpath('//div[@class="indexHot"]//ul//li//a/@href')
        sult=[]
        for (title,cover,brief,link) in zip(titles,covers,briefs,links):
            sult.append({'title': title,'covers':cover,'brief':brief,'link':link})
        return sult
    except Exception as e:
        print(e)
        return ''
def gethot(arg):
    try:
        url = "http://www.5wx.org/"
        xqq = requests.get(url, headers=header)
        if xqq.status_code != 200:
            return ''
        st = xqq.content.decode('utf-8')
        html = etree.HTML(st)
        titles = []
        covers = []
        briefs = []
        links = []
        titles = html.xpath('//div[@class="indexRecommend"]//ol//li//img/@alt')
        covers = html.xpath('//div[@class="indexRecommend"]//ol//li//img/@src')
        briefs = html.xpath('//div[@class="indexRecommend"]//ol//li//span/text()')
        links = html.xpath('//div[@class="indexRecommend"]//ol//li//a/@href')
        sult = []
        for (title, cover, brief, link) in zip(titles, covers, briefs, links):
            sult.append({'title': title, 'covers': cover, 'brief': brief, 'link': link})
        return sult
    except Exception as e:
        print(e)
        return ''
def readerrecom(arg):
    try:
        url = "http://www.5wx.org/"
        xqq = requests.get(url, headers=header)
        if xqq.status_code != 200:
            return ''
        st = xqq.content.decode('utf-8')
        html = etree.HTML(st)
        titles = html.xpath('//div[@class="webSidebar"]//div[@class="webSidebarBOX"][4]//ul//li/a/text()')
        recoms = html.xpath('//div[@class="webSidebar"]//div[@class="webSidebarBOX"][4]//ul//li/i/text()')
        links = html.xpath('//div[@class="webSidebar"]//div[@class="webSidebarBOX"][4]//ul//li/a/@href')
        sult = []
        for (title, recom, link) in zip(titles, recoms, links):
            sult.append({'title': title, 'recom': recom, 'link': link})
        return sult
    except Exception as e:
        print(e)
        return ''
def readerlove(arg):
    try:
        url = "http://www.5wx.org/"
        xqq = requests.get(url, headers=header)
        if xqq.status_code != 200:
            return ''
        st = xqq.content.decode('utf-8')
        html = etree.HTML(st)
        titles = html.xpath('//div[@class="webSidebar"]//div[@class="webSidebarBOX"][3]//ul//li/a/text()')
        recoms = html.xpath('//div[@class="webSidebar"]//div[@class="webSidebarBOX"][3]//ul//li/i/text()')
        links = html.xpath('//div[@class="webSidebar"]//div[@class="webSidebarBOX"][3]//ul//li/a/@href')
        sult = []
        for (title, recom, link) in zip(titles, recoms, links):
            sult.append({'title': title, 'readerlove': recom, 'link': link})
        return sult
    except Exception as e:
        print(e)
        return ''
def getsort(msg):
    try:
        url = "http://www.5wx.org/"+msg
        xqq = requests.get(url, headers=header)
        if xqq.status_code != 200:
            return ''
        st = xqq.content.decode('utf-8')
        html = etree.HTML(st)
        title = html.xpath('//div[@class="listIndexUpdata"]//h4/text()')
        lists = html.xpath('//div[@class="listIndexUpdata"]//ul//tr')
        links=[]
        booknames=[]
        lastarts=[]
        authors=[]
        updatatimes=[]
        statuss=[]
        for list in lists[1:]:
            bookname=list.xpath('.//td[1]//a/text()')
            link=list.xpath('.//td[1]//a/@href')
            lastart = list.xpath('.//td[2]//a/text()')
            author = list.xpath('.//td[3]/text()')
            updatatime = list.xpath('.//td[4]/text()')
            status = list.xpath('.//td[5]/text()')
            booknames.append(bookname)
            lastarts.append(lastart)
            authors.append(author)
            updatatimes.append(updatatime)
            statuss.append(status)
            links.append(link)
        sult = []
        for (bookname, lastart, author,updatatime,status,link) in zip(booknames, lastarts, authors,updatatimes,statuss,links):
            sult.append({'bookname': bookname, 'link':link,'lastart': lastart, 'author': author,'updatatime':updatatime,'status':status})
        return sult
    except Exception as e:
        print(e)
        return ''
if __name__ == '__main__':
    getrecommend("http://www.5wx.org/read/0/81/163.html")