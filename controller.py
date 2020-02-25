import gevent
import threading
import re
import json
import novel.nv1 as nv1
import anime.am1 as am1
import manhua.mh1 as mh1
import manhua.mh2 as mh2
import movie.mv1 as mv1
from gevent import socket
NovelSearchBookTask = "NovelSearchBookTask"
NovelSearchBookMoreTask = "NovelSearchBookMoreTask"
NovelSearchBookDetailTask = "NovelSearchBookDetailTask"
NovelSearchBookContentTask = "NovelSearchBookContentTask"
NovelPoprecommendationTask="NovelPoprecommendationTask"#热门推荐
NovelrecommendnovelsTask="NovelrecommendnovelsTask"
NovelbookfriendrecommedTask = "NovelbookfriendrecommedTask";
NovelmostpopularnovelTask = "NovelmostpopularnovelTask";
NovelgetsortTask="NovelgetsortTask"
AnimSearchTask = "AnimSearchTask";
AnimSearchDetailTask = "AnimSearchDetailTask";
AnimSearchContentTask = "AnimSearchContentTask";
ManhuaSearchTask = "ManhuaSearchTask";
ManhuaSearchlinkTask = "ManhuaSearchlinkTask";
ManhuaSearchContentlinkTask = "ManhuaSearchContentlinkTask"
ManhuaSortContentlinkTask = "ManhuaSortContentlinkTask"
MovieSearchTask="MovieSearchTask"
MovieDetailTask="MovieDetailTask"
MoviePlayerTask="MoviePlayerTask"


def gorun(clientsocket):
    try:
        thread = ServerThreading(clientsocket)
        thread.start()
        pass
    except Exception as identifier:
        print(identifier)
        pass


def main():
    serversocker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 40001
    serversocker.bind((host, port))
    serversocker.listen(100)
    myaddr = serversocker.getsockname()
    print("服务器地址:%s" % str(myaddr))
    while True:
        clientsocket, addr = serversocker.accept()
        print("连接地址:%s" % str(addr))
        gevent.spawn(gorun, clientsocket)
        pass
    serversocker.close()
    pass


class ServerThreading(threading.Thread):

    def __init__(self, clientsocket, recvsize=1024 * 1024, encoding="utf-8"):
        threading.Thread.__init__(self)
        self._socket = clientsocket
        self._recvsize = recvsize
        self._encoding = encoding
        pass

    def resolvemsg(self, msg):
        try:
            if msg == None: return
            st = re.findall('[^@!]+', msg)
            task = st[0]
            art = st[1]
            facen = st[2]
            facen=int(facen)
            print(facen)
            if task == NovelSearchBookTask:
                if facen == 1:
                    rest = nv1.getnv(art)
            if task == NovelSearchBookMoreTask:
                if facen == 1:
                    rest = nv1.getmore(art)
            if task == NovelSearchBookDetailTask:
                if facen == 1:
                    rest = nv1.getdetail(art)
            if task == NovelSearchBookContentTask:
                if facen == 1:
                    rest = nv1.getcontent(art)
            if task == NovelPoprecommendationTask:
                if facen == 1:
                    rest = nv1.getrecommend(art)
            if task == NovelrecommendnovelsTask:
                if facen == 1:
                    rest = nv1.gethot(art)
            if task == NovelbookfriendrecommedTask:
                if facen == 1:
                    rest = nv1.readerrecom(art)
            if task ==NovelmostpopularnovelTask:
                if facen == 1:
                    rest = nv1.readerlove(art)

            if task==NovelgetsortTask:
                if facen == 1:
                    rest = nv1.getsort(art)

            if task == AnimSearchTask:
                if facen == 1:
                    rest = am1.getanime(art)
            if task == AnimSearchDetailTask:
                if facen == 1:
                    rest = am1.geturl(art)
            if task == AnimSearchContentTask:
                if facen == 1:
                    rest = am1.getview(art)

            if task == ManhuaSearchTask:
                if facen == 1:
                    rest = mh1.searchmanhua(art)
                if facen == 2:
                    rest = mh2.searchmanhua(art)
                if facen == 3:
                    rest = mh3.searchmanhua(art)
            if task == ManhuaSearchlinkTask:
                if facen == 1:
                    rest = mh1.manhuadetail(art)
                if facen == 2:
                    rest = mh2.manhuadetail(art)
                if facen == 3:
                    rest = mh3.manhuadetail(art)
            if task == ManhuaSearchContentlinkTask:
                if facen == 1:
                    rest = mh1.manhuacontent(art)
                if facen == 2:
                    rest = mh2.manhuacontent(art)
                if facen == 3:
                    rest = mh3.manhuacontent(art)
            if task == ManhuaSortContentlinkTask:
                if facen == 1:
                    rest = mh1.manhuasort(art)
                if facen == 2:
                    rest = mh2.manhuasort(art)
                if facen == 3:
                    rest = mh3.manhuasort(art)

            if task == MovieSearchTask:
                if facen == 1:
                    rest = mv1.moviesearch(art)
            if task == MovieDetailTask:
                if facen == 1:
                    rest = mv1.moviedetail(art)
            if task == MoviePlayerTask:
                if facen == 1:
                    rest = mv1.movieplayer(art)
            return rest
        except:
            return ''

    def run(self):
        print("线程开始")
        try:
            msg = ''
            arg = ''
            while True:
                # 读取recvsize个字节
                rec = self._socket.recv(self._recvsize)
                # 解码
                msg += rec.decode(self._encoding)
                # 文本接受是否完毕，因为python socket不能自己判断接收数据是否完毕，
                # 所以需要自定义协议标志数据接受完毕
                if msg.strip().endswith('over'):
                    arg = msg[:-4]
                    print(arg)
                    break
            msgs = self.resolvemsg(arg)
            ms = {}
            if len(msgs) == 0:
                ms['code'] = 0
                ms['message'] = '失败'
            else:
                ms['code'] = 1
                ms['message'] = '成功'
            ms['list'] = msgs
            presendmsg = json.dumps(ms, ensure_ascii=False)
            print(presendmsg)
            send=presendmsg.encode('utf-8')
            self._socket.send(send)
        except Exception as identifier:
            self._socket.send("500".encode(self._encoding))
            print(identifier)
            pass
        finally:
            self._socket.close()
        print("任务结束")


if __name__ == "__main__":
    main()
