# -*- coding: utf-8 -*-
import urllib2,urllib,re,sys,os
import util

# 中国网络电视台点播(CNTV)
# Write by robinttt 2010.
# Update by taxigps 2011

# Plugin constants 
__addonname__ = "中国网络电视台点播(CNTV)"
__addonid__ = "plugin.video.cntv"
__addon__ = xbmcaddon.Addon(id=__addonid__)
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

def getRootMenu(name,url):
	t = util.Menu()

	name = '爱布谷>频道查询'
	url = 'http://bugu.cntv.cn/channel/index.shtml'
	
	link=GetHttpData(url)
	link=re.sub('\r','',link)
	link=re.sub('\n','',link)
	link=re.sub('\t','',link)
	match=re.compile('<p class="edh"(.+?)id="(.+?)">(.+?)</p>').findall(link)
	for i in range(0,len(match)):
		name1=re.sub('<a(.+?)>','',match[i][2])
		name1=re.sub('</a>','',name1)
		li=util.MenuItem(name+'>'+name1)
		u=argv[0]+"?mode=10&name="+urllib.quote_plus(name+'>'+name1)+"&url="+urllib.quote_plus(url)+"&id="+urllib.quote_plus('<p class="edh"'+match[i][0]+'id="'+match[i][1]+'">'+match[i][2]+'</p>')
		t.addDirectoryItem(int(argv[1]),u,li,True)

	# Test
	decode(t.endOfDirectory(1))
	# end

	return t

def progList(name,url,id):
	t = util.Menu()

	link=GetHttpData(url)
	link=re.sub('\r','',link)
	link=re.sub('\n','',link)
	link=re.sub('\t','',link)
	match=re.compile(id+'(.+?)</table>').findall(link)
	match0=re.compile('href="(.+?)" target="_blank" class="cyan">(.+?)</a>').findall(match[0])
	for url1,name1 in match0:
		li=util.MenuItem(name+'>'+name1)
		u=argv[0]+"?mode=11&name="+urllib.quote_plus(name+'>'+name1)+"&url="+urllib.quote_plus(url1)
		t.addDirectoryItem(int(argv[1]),u,li,True)

	# Test
	decode(t.endOfDirectory(1))
	# end

	return t

def progList2(name,url):
	t = util.Menu()

	li=util.MenuItem('当前位置：'+name)
	u=argv[0]+"?mode=20&name="+urllib.quote_plus(name)
	t.addDirectoryItem(int(argv[1]),u,li,True)
	link=GetHttpData(url)
	match=re.compile('var brief="(.+?)";').findall(link)
	plot=match[0]
	match=re.compile("new title_array\('(.+?)','(.+?)','(.+?)','(.+?)'").findall(link)
	for i in range(0,len(match)):
		li=util.MenuItem(str(i+1)+'. '+match[i][0]+'  (时长:'+match[i][2]+')',iconImage='',thumbnailImage=match[i][1])
		li.bindMedia( util.Media() )
		u=argv[0]+"?mode=12&name="+urllib.quote_plus(match[i][0])+"&url="+urllib.quote_plus(match[i][3])+"&plot="+urllib.quote_plus(plot)+"&thumb="+urllib.quote_plus(match[i][1])
		t.addDirectoryItem(int(argv[1]),u,li)

	# Test
	decode(t.endOfDirectory(1))
	# end

	return t

def PlayVideo(name,url,thumb,plot):
	media = util.Media()

	playlist=util.PlayList(1)
	playlist.clear()
	link=GetHttpData(url)
	match=re.compile('\("videoCenterId","(.+?)"\)').findall(link)
	url='http://vdd.player.cntv.cn/index.php?pid='+match[0]
	link=GetHttpData(url)
	match=re.compile('"chapters":\[(.+?)\]').findall(link)
	match0=re.compile('"url":"(.+?)"').findall(match[0])
	for i in range(0,len(match0)):
		#listitem=util.MenuItem(name,iconImage='',thumbnailImage=thumb)
		#listitem.setInfo(type="Video",infoLabels={"Title":name,"plot":plot})
		#playlist.add(match0[i].replace('\\',''), listitem)
		playlist.add(match0[i].replace('\\',''))

	# Test
	util.Player().play(playlist)
	# end

	media.setMediaInfo('Title', name)
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
	params=get_params()

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
	elif mode==10:
		return progList(name,url,id)
	elif mode==11:
		return progList2(name,url)
	elif mode==12:
		return PlayVideo(name,url,plot,thumb)
