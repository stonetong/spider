#!/usr/bin/env python
#-*- coding:UTF-8 -*-

import urllib2
import re

url = 'http://www.qiushibaike.com'
user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
headers = {
            'User-Agent':user_agent
}
request = urllib2.Request(url,headers=headers)
response = urllib2.urlopen(request)
content = response.read().decode('UTF-8')
pattern = re.compile('<div.*?class="content".*?>(.*?)</div>',re.S)
items = re.findall(pattern,content)

for item in items:
    print item
