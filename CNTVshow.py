# -*- coding: utf-8 -*-
import urllib2,urllib,re,sys,os
import util

# 中国网络电视台点播(CNTV)
# Write by robinttt 2010.
# Update by taxigps 2011

# Plugin constants 
__addonname__ = "中国网络电视台点播(CNTV)"
__addonid__ = "plugin.video.cntv"
__addon__ = util.Addon(id=__addonid__)
__addonpath__ = __addon__.getAddonInfo('path')

argv = ['']*3
argv[0] = __addonid__
argv[1] = 0 
argv[2] =''

def encode(**args):
    return argv[0] + "?" + '&'.join([ "%s=%s"%(x,urllib.quote_plus(str(args[x]))) for x in args ])

def GetHttpData(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	try:
		response = urllib2.urlopen(req, timeout=10)
	except urllib2.URLError, e: 
		print e
		raise NetworkError, 'network error'	
	httpdata = response.read()
	response.close()
	match = re.compile('<meta http-equiv="Content-Type" content="text/html; charset=(.+?)" />').findall(httpdata)
	if len(match)>0:
		charset = match[0].lower()
		if (charset != 'utf-8') and (charset != 'utf8'):
			httpdata = unicode(httpdata, charset).encode('utf8')
	return httpdata

def getRootMenu():
	t = util.Menu()

	name = '爱西柚>专辑'
	category = 'plist'
	link=GetHttpData('http://xiyou.cntv.cn/'+category+'/index-hot-week.html')
	link=re.sub('\r','',link)
	link=re.sub('\n','',link)
	link=re.sub('\t','',link)
	li=util.MenuItem(name+'>全部')
	u = encode(mode=3, name=name+'>全部', category=category, id=0)
	t.addDirectoryItem(int(argv[1]),u,li,True)
	match=re.compile('<li><a href="/'+category+'/index-hot-week-([0-9]+).html"><span class="hotspan">(.+?)</span>').findall(link)
	for id,name1 in match:
		li=util.MenuItem(name+'>'+name1)
		#u=argv[0]+"?mode=3&name="+urllib.quote_plus(name+'>'+name1+'>全部')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)
		u = encode(mode=5, name=name+'>'+name1+'>全部>播放最多', category=category, id=id, type='', handler='-hot', page='1')
		t.addDirectoryItem(int(argv[1]),u,li,True)

	# Test
	decode(t.endOfDirectory(1))
	# end

	return t
"""
def XiyouC(name,category,id):
    li=util.MenuItem(name+'>今日')
    u=argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>今日')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus('-day')
    t.addDirectoryItem(int(argv[1]),u,li,True)
    li=util.MenuItem(name+'>本周')
    u=argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>本周')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus('-week')
    t.addDirectoryItem(int(argv[1]),u,li,True)
    li=util.MenuItem(name+'>本月')
    u=argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>本月')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus('-month')
    t.addDirectoryItem(int(argv[1]),u,li,True)
    li=util.MenuItem(name+'>全部')
    u=argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>全部')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus('')
    t.addDirectoryItem(int(argv[1]),u,li,True)

def XiyouD(name,category,id,type):
    li=util.MenuItem(name+'>播放最多')
    u=argv[0]+"?mode=5&name="+urllib.quote_plus(name+'>播放最多')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus(type)+"&handler="+urllib.quote_plus('-hot')+"&page="+urllib.quote_plus('1')
    t.addDirectoryItem(int(argv[1]),u,li,True)
    li=util.MenuItem(name+'>收藏最多')
    u=argv[0]+"?mode=5&name="+urllib.quote_plus(name+'>收藏最多')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus(type)+"&handler="+urllib.quote_plus('-fav')+"&page="+urllib.quote_plus('1')
    t.addDirectoryItem(int(argv[1]),u,li,True)
    if category=='video':
        li=util.MenuItem(name+'>评论最多')
        u=argv[0]+"?mode=5&name="+urllib.quote_plus(name+'>评论最多')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus(type)+"&handler="+urllib.quote_plus('-comment')+"&page="+urllib.quote_plus('1')
        t.addDirectoryItem(int(argv[1]),u,li,True)
        li=util.MenuItem(name+'>顶的最多')
        u=argv[0]+"?mode=5&name="+urllib.quote_plus(name+'>顶的最多')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus(type)+"&handler="+urllib.quote_plus('-dig')+"&page="+urllib.quote_plus('1')
        t.addDirectoryItem(int(argv[1]),u,li,True)
    li=util.MenuItem(name+'>最近更新')
    u=argv[0]+"?mode=5&name="+urllib.quote_plus(name+'>最近更新')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus(type)+"&handler="+urllib.quote_plus('-new')+"&page="+urllib.quote_plus('1')
    t.addDirectoryItem(int(argv[1]),u,li,True)
"""

def progList(name,category,handler,id,type,page):
	t = util.Menu()
	tmp='Ajax'+category+handler
	url='http://xiyou.cntv.cn/'+category+'/index'+handler+type+'-'+id+'-'+page+'.html'
	link=GetHttpData(url)
	link=re.sub('\r','',link)
	link=re.sub('\n','',link)
	link=re.sub('\t','',link)
	link=re.sub(' ','',link)

	li=util.MenuItem('当前位置：'+name+' 【第'+page+'页】')
	u=argv[0]+"?mode=20"
	t.addDirectoryItem(int(argv[1]),u,li,True)
	#获取当前列表
	if category=='video':
		match0=re.compile('<ulclass="video"><liclass="vimg"><atitle="(.+?)"href="(.+?)"target="_blank"><img.*?lazy-src="(.+?)"alt=".+?"></a><spanclass="vtime">(.+?)</span><spanid="(.+?)"').findall(link)
		for i in range(0,len(match0)):
			li=util.MenuItem(str(i+1)+'.'+match0[i][0],iconImage='',thumbnailImage=match0[i][2])
			u=argv[0]+"?mode=7&name="+urllib.quote_plus(match0[i][0])+"&id="+urllib.quote_plus(match0[i][4])+"&thumb="+urllib.quote_plus(match0[i][2])+"&duration="+urllib.quote_plus(match0[i][3])
			t.addDirectoryItem(int(argv[1]),u,li)
	else:
		match0=re.compile('<ulclass="video"><liclass="vimg"><atitle="(.+?)"href="(.+?)"target="_blank"><img.*?lazy-src="(.+?)"alt=".+?"></a>').findall(link)
		for i in range(0,len(match0)):
			li=util.MenuItem(str(i+1)+'.'+match0[i][0],iconImage='',thumbnailImage=match0[i][2])
			u=argv[0]+"?mode=6&name="+urllib.quote_plus(name+'>'+match0[i][0])+"&url="+urllib.quote_plus('http://xiyou.cntv.cn'+match0[i][1])
			t.addDirectoryItem(int(argv[1]),u,li,True)
	#获取其他页码
	match=re.compile('<divclass="page">(.+?)</div>').findall(link)
	if len(match)>0:
		match0=re.compile('<ahref="/'+category+'/index'+handler+type+'-'+id+'-([0-9]+).html"class="(.+?)">(.+?)</a>').findall(match[0])
		for i in range(0,len(match0)):
			if match0[i][1]=='fsize12' or match0[i][1]=='prev_page' or match0[i][1]=='next_page':
				li=util.MenuItem('..'+match0[i][2])
				u=argv[0]+"?mode=5&name="+urllib.quote_plus(name)+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus(type)+"&handler="+urllib.quote_plus(handler)+"&page="+urllib.quote_plus(match0[i][0])
				t.addDirectoryItem(int(argv[1]),u,li,True)
			elif match0[i][1]!='current_page':
				li=util.MenuItem('..第'+match0[i][2]+'页')
				u=argv[0]+"?mode=6&name="+urllib.quote_plus(name)+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus(type)+"&handler="+urllib.quote_plus(handler)+"&page="+urllib.quote_plus(match0[i][0])
				t.addDirectoryItem(int(argv[1]),u,li,True)

	# Test
	decode(t.endOfDirectory(1))	
	# end

	return t

def progList2(name,url):
	t = util.Menu()

	li=util.MenuItem('当前位置：'+name)
	u=argv[0]+"?mode=20"
	t.addDirectoryItem(int(argv[1]),u,li,True)
	link=GetHttpData(url)
	link=re.sub('\r','',link)
	link=re.sub('\n','',link)
	link=re.sub('\t','',link)
	link=re.sub(' ','',link)
	match=re.compile('<ulclass="video"><liclass="vimg"><ahref="(.+?)"title="(.+?)"><img.*?lazy-src="(.+?)"/></a><spanclass="vtime">(.+?)</span><spanclass="vadd"id="(.+?)"').findall(link)
	for i in range(0,len(match)):
		li=util.MenuItem(str(i+1)+'.'+match[i][1],iconImage='',thumbnailImage=match[i][2])
		li.bindMedia( util.Media() )
		u=argv[0]+"?mode=7&name="+urllib.quote_plus(match[i][1])+"&id="+urllib.quote_plus(match[i][4])+"&thumb="+urllib.quote_plus(match[i][2])+"&duration="+urllib.quote_plus(match[i][3])
		t.addDirectoryItem(int(argv[1]),u,li)

	# Test
	decode(t.endOfDirectory(1))
	# end

	return t

def PlayVideo(name,id,thumb,duration):
	media = util.Media()
	playlist = util.PlayList(1)
	playlist.clear()

	media.setMediaInfo('Title', name)
	url='http://xiyou.cntv.cn/interface/index?videoId='+id
	link=GetHttpData(url)
	match=re.compile('"videoFilePath":"(.+?)#').findall(link)
	path=match[0].replace('\\','')+'_001.mp4'
	#li=util.MenuItem(name, iconImage='', thumbnailImage=thumb)
	#li.setInfo(type="Video",infoLabels={"Title":name,"Duration":duration})
	#util.Player().play(path, li)
	playlist.add(path)
	# Test
	util.Player().play(path)
	# end

	media.setPlayList(playlist)
	return media

def get_params(code):
    parts = code.split('?')
    argv[0], argv[1] = parts[0] , ' 0 '
    if len(parts) > 1:
        argv[2] = parts[1]

    param=[]
    paramstring=argv[2]
    if len(paramstring)>=2:
        params=argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
                
    return param

def decode(code):
	params=get_params(code)

	mode=None
	name=None
	url=None
	category=None
	id=None
	type=None
	handler=None
	page=None
	thumb=None
	director=None
	studio=None
	plot=None
	duration=None

	try:
		url=urllib.unquote_plus(params["url"])
	except:
		pass
	try:
		name=urllib.unquote_plus(params["name"])
	except:
		pass
	try:
		mode=int(params["mode"])
	except:
		pass
	try:
		category=urllib.unquote_plus(params["category"])
	except:
		pass
	try:
		id=urllib.unquote_plus(params["id"])
	except:
		pass
	try:
		type=urllib.unquote_plus(params["type"])
	except:
		pass
	try:
		handler=urllib.unquote_plus(params["handler"])
	except:
		pass
	try:
		page=urllib.unquote_plus(params["page"])
	except:
		pass
	try:
		director=urllib.unquote_plus(params["director"])
	except:
		pass
	try:
		studio=urllib.unquote_plus(params["studio"])
	except:
		pass
	try:
		plot=urllib.unquote_plus(params["plot"])
	except:
		pass
	try:
		thumb=urllib.unquote_plus(params["thumb"])
	except:
		pass
	try:
		duration=urllib.unquote_plus(params["duration"])
	except:
		pass


	if mode==None:
		name=''
		return getRootMenu()
	elif mode==5:
		return progList(name,category,handler,id,type,page)
	elif mode==6:
		return progList2(name,url)
	elif mode==7:
		return PlayVideo(name,id,thumb,duration)

# Test
if __name__ == '__main__':
	decode(__addonid__)
# end
