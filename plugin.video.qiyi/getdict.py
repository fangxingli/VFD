# -*- coding: utf-8 -*-
import urllib2, urllib, re, string, sys, os

CHANNEL_LIST = [['电影','1'], ['电视剧','2'], ['纪录片','3'], ['动漫','4'], ['音乐','5'], ['综艺','6'], ['娱乐','7'], ['旅游','9']]
CHANNEL_DICT = dict(CHANNEL_LIST)
ORDER_LIST = [['关注','5'], ['最新','2'], ['热播','3'], ['好评','4']]
ORDER_DICT = dict(ORDER_LIST)

def GetHttpData(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    httpdata = re.sub("\s", "", httpdata)
    return httpdata

# 从电影页面获取电影类型列表（MOVIE_TYPE_LIST）和地区列表（MOVIE_AREA_LIST）
MOVIE_TYPE_LIST = {}
MOVIE_AREA_LIST = {}
for channel, id in CHANNEL_LIST:
    print channel.decode('utf8').encode('gb2312')
    link = GetHttpData('http://list.qiyi.com/www/' + id + '/------------2-1-1----.html')
    if id == '5':
        match1 = re.compile('<dtdata-value="[0-9]">按流派</dt>(.*?)</dd>').findall(link)
    else:
        match1 = re.compile('<dtdata-value="[0-9]">按类型</dt>(.*?)</dd>').findall(link)
    if id == '3' or id == '9':
        match = re.compile('href="http://list.qiyi.com/www/' + id + '/([0-9]*)------------2-1-1----.html">(.*?)</a>').findall(match1[0])
    elif id == '5':
        match = re.compile('href="http://list.qiyi.com/www/' + id + '/---([0-9]*)---------2-1-1----.html">(.*?)</a>').findall(match1[0])
    else:
        match = re.compile('href="http://list.qiyi.com/www/' + id + '/-([0-9]*)-----------2-1-1----.html">(.*?)</a>').findall(match1[0])
    tmp = "MOVIE_TYPE_LIST['"+id+"'] = ["
    for a, b in match:
        tmp = tmp + "['" + b.decode('utf8').encode('gb2312') + "','" + a + "'],"
    tmp = tmp + ']'
    print tmp 
    #MOVIE_TYPE_LIST[id] = [[x[1],x[0]] for x in match]
    match1 = re.compile('<dtdata-value="[0-9]">按地区</dt>(.*?)</dd>').findall(link)
    tmp = "MOVIE_AREA_LIST['"+id+"'] = ["
    if len(match1) > 0:
        if id == '7':
            match = re.compile('href="http://list.qiyi.com/www/' + id + '/--([0-9]*)----------2-1-1----.html">(.*?)</a>').findall(match1[0])
        elif id == '9':
            match = re.compile('href="http://list.qiyi.com/www/' + id + '/-([0-9]*)-----------2-1-1----.html">(.*?)</a>').findall(match1[0])
        else:
            match = re.compile('href="http://list.qiyi.com/www/' + id + '/([0-9]*)------------2-1-1----.html">(.*?)</a>').findall(match1[0])
        for a, b in match:
            tmp = tmp + "['" + b.decode('utf8').encode('gb2312') + "','" + a + "'],"
    tmp = tmp + ']'
    print tmp 
    #MOVIE_AREA_LIST[id] = [[x[1],x[0]] for x in match]
