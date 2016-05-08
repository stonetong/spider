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
    #传入某页代码，返回本页段子列表
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败...."
            return None
        pattern = re.compile('<div.*?class="content".*?>(.*?)</div>',re.S)
        items = re.findall(pattern,pageCode)
        #用来存储每页的段子
        pageStories = []
        #遍历正则表达式匹配的信息
        for item in items:
            pageStories.append(item)
        return pageStories
    #加载并提取页面的内容，加入到列表中
    def loadPage(self):
        #如果当前未看的页数少于2页，则加载新一页
        if self.enable == True:
            if len(self.stories) < 2:
                #获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                #将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1
    #调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self,pageStories,page):
        #遍历一页的段子
        for story in pageStories:
            #等待用户输入
            user_input = raw_input()
            #每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            #如果输入Q则程序结束
            if user_input == 'Q':
                self.enable = False
                return
            print u'story: '
            print story
    #主函数
    def start(self):
        print u"loading...please press 'enter' to look through new ('Q' to quit)"
        #初始化变量为True，程序可以正常运行
        self.enable = True
        #先加载一页内容
        self.loadPage()
        #局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                #从全局list中获取一页的段子
                pageStories = self.stories[0]
                #当前读到的页数加一
                nowPage += 1
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页的段子
                self.getOneStory(pageStories,nowPage)
spider = QSBK()
spider.start()
