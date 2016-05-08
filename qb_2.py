#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time

class QSBK:
    #初始化方法，定义变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64)'
        self.headers = {'User-Agent':self.user_agent }
        #存放段子的变量，每个元素是每一页的全部段子
        self.stories = []
        self.enable = False
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url,headers = self.headers)
            response = urllib2.urlopen(request)
            #将页面转化为UTF-8编码
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"连接糗事百科失败,错误原因",e.reason
                return None

    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败...."
            return None
        pattern = re.compile('<div.*?class="content".*?>(.*?)</div>',re.S)
        items = re.findall(pattern,pageCode)

        pageStories = []

        for item in items:
            pageStories.append(item)
        return pageStories

    def loadPage(self):

        if self.enable == True:
            if len(self.stories) < 2:

                pageStories = self.getPageItems(self.pageIndex)

                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    def getOneStory(self,pageStories,page):

        for story in pageStories:

            user_input = raw_input()

            self.loadPage()

            if user_input == 'Q':
                self.enable = False
                return
            print u'story: '
            print story[0],story[1],story[2],

    def start(self):
        print u"loading...please press 'enter' to look through new ('Q' to quit)"

        self.enable = True

        self.loadPage()

        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:

                pageStories = self.stories[0]

                nowPage += 1

                del self.stories[0]

                self.getOneStory(pageStories,nowPage)
spider = QSBK()
spider.start()
