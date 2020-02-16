import requests
from lxml import etree
import re
def moviesearch (nr1):#输入搜索内容
  try:
    xq = []
    header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    }
    data = {
      "wd": "%s"%nr1,
      "submit": "search"
    }
    url = "http://www.zuidazy1.com/index.php?m=vod-search"
    xqq = requests.post(url,headers=header,data=data,timeout=5)
    if xqq.status_code !=200:
          return ''
    tree = etree.HTML(xqq.text)
    xqq = tree.xpath('/html/body/div[@class="xing_vb"]/ul/li/span/a/@href')
    for i in xqq:
      xq.append(re.findall('/?m=(.*)',i)[0])
    mz = tree.xpath('/html/body/div[@class="xing_vb"]/ul/li/span/a/text()')
    lx = tree.xpath('/html/body/div[@class="xing_vb"]/ul/li/span[@class="xing_vb5"]/text()')
    sj = tree.xpath('//div/ul/li/span[4]/text()')
    z6 = []
    for (i,o,p,s) in zip(mz,xq,lx,sj):
      z6.append({'name':i,'url':"zd"+o,'genre':p,"time":s})
    return z6
  except:
    return ''
def moviedetail (url):#给页面地址，解出所有集名和地址
  try:
    tt = []
    header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3469.400"
    }
    url = re.sub('zdvod-detail-id','vod-detail-id',url,re.S)
    url = "http://www.zuidazy1.com/?m="+url
    xqq = requests.get(url,headers=header,timeout=5).text
    tree = etree.HTML(xqq)
    fm = tree.xpath('//div/div/div/div/img/@src')[0]
    js = tree.xpath('//div/ul/li/div/span')[1]
    sy = tree.xpath('//ul/li[7]/span')[0]
    dq = tree.xpath('//ul/li[5]/span')[0]
    zy = tree.xpath('//ul/li[3]/span')[0]
    sj = tree.xpath('//ul/li[9]/span')[0]
    yy = tree.xpath('//ul/li[6]/span')[0]
    dy = tree.xpath('//ul/li[2]/span')[0]
    lx = tree.xpath('//ul/li[4]/span')[0]
    mzo = tree.xpath("//div[@class='vodh']/h2/text()")[0]
    if js == []:
      js = ["无简介"]
    m3u8 = tree.xpath('//*[@id="play_1"]/ul/li/input/@value')
    online = tree.xpath('//*[@id="play_2"]/ul//li/input/@value')
    xz = tree.xpath('//*[@id="down_1"]/ul/li/input/@value')
    if xz == []:
      for i in range(len(m3u8)):
        xz += ["无"]
    if m3u8 == []:
      for i in range(len(xz)):
        m3u8 += ["无"]
    if online == []:
      for i in range(len(m3u8)):
        online += ["无"]
    jis = re.findall('/>(.*)\$http',xqq)
    mzjs = {'data':{'name':mzo,'cover':fm,'introduce':js.text,'Release':sy.text,'genre':lx.text,"time":sj.text,'director':dy.text,'performer':zy.text,'region':dq.text,'Language':yy.text}}
    mzjss = []
    for (i,o,p,j) in zip(m3u8,online,xz,jis):
      mzjss.append({'m3u8url':i,'onlineurl':o,'download':p,'num':j})
    mzjs['list']=mzjss
    return mzjs
  except:
    return ''
if __name__ == '__main__':
  print(moviesearch("异常生物见闻录"))