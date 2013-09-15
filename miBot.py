#!/usr/bin/env python
#encoding=utf-8
import time, sys, os
import re, json
import threading
import urllib, urllib2, cookielib
import webbrowser, StringIO, gzip

class miBot(object):
    
    def __init__(self, username=None, 
            password=None, serveraddr="http://www.xiaomi.com",
            cookiefile="config/xiaomi.cookie"):
        self.__username = username
        self.__password = password
        self.__serveraddr = serveraddr
        self.__cookiefile = cookiefile
        self.__cookie = cookielib.MozillaCookieJar(self.__cookiefile)
        self.__header = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding":"gzip,deflate,sdch",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Cache-Control":"max-age=0",
                "Connection":"keep-alive",
                "Content-Length":"",
                "Content-Type":"",
                "Host":"",
                "Origin":"",
                "Referer":"",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36"}

        try:
        #加载已存在的cookie，尝试此cookie是否还有效
            self.__cookie.load(ignore_discard=True, ignore_expires=True)
            print 'cookie exited'
        except Exception:
        #加载失败，说明从未登录过，需登录并创建一个cookie文件
            print '登录中...'
            self.__LoginSaveCookie(self.__username, self.__password)
            print 'exit'

    def __LoginSaveCookie(self, username, password):
        '''登录并保存本地cookie'''
        self.__loginheader = self.__header
        self.__loginheader["Content-Length"] = "184"
        self.__loginheader["Content-Type"] = "application/x-www-form-urlencoded"
        self.__loginheader["Host"] = "account.xiaomi.com"
        self.__loginheader["Origin"] = "https://account.xiaomi.com"
        self.__loginheader["Referer"] = "https://account.xiaomi.com/pass/serviceLogin"
        self.__loginseverurl = "https://account.xiaomi.com"
        self.__loginposturl = self.__loginseverurl + "/pass/serviceLoginAuth2"
        tmpdata = {"passToken":"", "user":username, 'pwd':password, "callback":"https://account.xiaomi.com", "sid":"passport", "qs":"%3Fsid%3Dpassport", "hidden":"", "_sign":"KKkRvCpZoDC+gLdeyOsdMhwV0Xg="}
        tmpdata = urllib.urlencode(tmpdata)
        tmpopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookie))
        tmpreq = urllib2.Request(self.__loginposturl, tmpdata, self.__loginheader)
        response = tmpopener.open(tmpreq, tmpdata)
        # print response.info().get('Set-Cookie')
        self.__cookie.save(self.__cookiefile, ignore_discard=True,ignore_expires=True)

    def preBuy(self):#红米
        self.__buyaddr = "http://t.hd.xiaomi.com/?_a=20130910&_op=book"
        tmpopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookie))
        response  = tmpopener.open(self.__buyaddr)#Get method
        if response.info().get('Content-Encoding') == 'gzip':#解码
            buf = StringIO.StringIO(response.read())
            gzip_f = gzip.GzipFile(fileobj=buf)
            content = gzip_f.read()
        else:
            content = response.read()
        f = open("./xiaomi.html", "w")
        f.write(content)
        f.close()
        path = os.path.abspath("./xiaomi.html")
        webbrowser.open_new_tab("file://"+path)

if __name__ == '__main__':
    username = ""
    password = ""
    if not os.path.exists('config/xiaomi.cookie'):
        print "输入用户名..."
        username = raw_input('> ')
        print "输入密码..."
        password = raw_input('> ')
    mibot = miBot(username=username, password=password)
    mibot.preBuy()