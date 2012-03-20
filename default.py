# -*- coding: utf-8 -*-
import urllib2, urllib, re, string, os, gzip, StringIO
import io
#from util import LevelTree
import util as xbmc
import util as xbmcgui
import util as xbmcplugin
import util as xbmcaddon

# PPTV IPAD专区视频(ipad.pptv.com) by wow1122(wht9000@gmail.com), 2011

# Plugin constants 
__addonname__ = "PPTV IPAD专区视频(ipad.pptv.com)"
__addonid__ = "plugin.video.ipadpptv"
__addon__ = xbmcaddon.Addon(id=__addonid__)
__addonicon__ = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )

#UserAgent = 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10'
UserAgent = 'Mozilla/5.0(iPad; U; CPU OS 4_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F191 Safari/6533.18.5'
TOP_TREE=[['新上线','new'], ['电影', 'movie'], ['电视剧','tv'], ['动漫','cartoon'], ['综艺','show'], ['资讯','info'], ['体育','sport'] ,['游戏','game']]
argv = ['']*3
argv[0] = __addonid__
argv[1] = 0
argv[2] =''

def GetHttpData(url):
	print "GetHttpData %s " % url
	req = urllib2.Request(url)
	req.add_header('User-Agent', UserAgent)
	response = urllib2.urlopen(req)
	httpdata = response.read()
	if response.headers.get('content-encoding', None) == 'gzip':
		httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
	response.close()
	match = re.compile('<meta http-equiv="[Cc]ontent-[Tt]ype" content="text/html; charset=(.+?)"').findall(httpdata)
	if len(match)<=0:
		match = re.compile('meta charset="(.+?)"').findall(httpdata)
	if len(match)>0:
		charset = match[0].lower()
		if (charset != 'utf-8') and (charset != 'utf8'):
			httpdata = unicode(httpdata, charset).encode('utf8')
	return httpdata
    
def searchDict(dlist,idx):
	for i in range(0,len(dlist)):
		if dlist[i][0] == idx:
			return dlist[i][1]
	return ''
    
def getList(listpage):
	catlist = re.compile('<a href="(.+?).htm" title="(.+?)"', re.DOTALL).findall(listpage)
	return catlist 

''' 合作商填写 '''
def rootList():
	t = xbmcgui.LevelList()
	
	for i,j in TOP_TREE:
		li=xbmcgui.ListItem(i)
		u=argv[0]+"?mode=1&name="+urllib.quote_plus(i)+"&type="+urllib.quote_plus(j)+"&cat="+urllib.quote_plus('')+"&page="+urllib.quote_plus('1')
		t.addDirectoryItem(argv[1], u, li, True)
	# For Test
	feed(t.endOfDirectory(1))
	# end
	return t
    
def progList(name,type,cat,page):
	t = xbmcgui.LevelList()
	if cat.find('_')==-1:
		url = 'http://ipad.pptv.com/'+type+'_p'+page+'.htm'
	else:
		url = 'http://ipad.pptv.com/'+cat+'_p'+page+'.htm'
	link = GetHttpData(url)
	print "progList %s " % url
	match = re.compile('<dt>类型：</dt>(.+?)</dl>', re.DOTALL).findall(link)
	if len(match):
		listpage = match[0]
	else:
		listpage = ''
	catlist=getList(listpage)
	if cat.find('_')==-1:
		catstr='全部'
	else:
		clist=cat.split('_')
		if len(clist)==2:
			catstr = searchDict(catlist,cat)
		else:
			print cat[:-6]
			catstr = searchDict(catlist,cat[:-6])
			match = re.compile('<dt>全部子分类：</dt>(.+?)</dd>',re.DOTALL).findall(link)
			if match:
				match1 = re.compile('class="now">(.+?)</a>').findall(match[0])
				catstr = catstr+'-'+match1[0]
                
	match = re.compile('<li>(.+?)</li>', re.DOTALL).findall(link)
	totalItems = len(match)           

	#li = xbmcgui.ListItem('类型[COLOR FFFF0000]【' + catstr + '】[/COLOR] （按此选择）')
	#u = argv[0] + "?mode=5&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&cat="+urllib.quote_plus(cat)+"&page="+urllib.quote_plus(listpage)
	#t.addDirectoryItem(int(argv[1]), u, li, True, totalItems)

	for i in range(0,len(match)):
		match1 = re.compile('<a href="(.+?)" title="(.+?)" class="img"><img src="(.+?)" width=', re.DOTALL).findall(match[i])
		for p_id,p_name,p_thumb in match1:
			li = xbmcgui.ListItem(p_name, iconImage = p_thumb, thumbnailImage = p_thumb)
			u = argv[0]+"?mode=2&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus('http://ipad.pptv.com/'+p_id)+"&thumb="+urllib.quote_plus(p_thumb)
			t.addDirectoryItem(int(argv[1]), u, li, True, totalItems)

	match = re.compile('<nav class="pageNum c_b">(.+?)</nav>', re.DOTALL).findall(link)
	match1= re.compile('<a class="" href=".+?">(.+?)</a>', re.DOTALL).findall(match[0])
	if len(match1):
		totalpages=match1[len(match1)-2]
	else:
		totalpages=1
	currpage=int(page)
	if currpage > 1:
		li = xbmcgui.ListItem('上一页')
		u = argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&cat="+urllib.quote_plus(cat)+"&page="+urllib.quote_plus(str(currpage-1))
		t.addDirectoryItem(int(argv[1]), u, li, True, totalItems)
	if currpage < totalpages:
		li = xbmcgui.ListItem('下一页')
		u = argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&cat="+urllib.quote_plus(cat)+"&page="+urllib.quote_plus(str(currpage+1))
		t.addDirectoryItem(int(argv[1]), u, li, True, totalItems)
	t.setContent(int(argv[1]), 'movies')
	# Note: This may take some time
	xbmc.ImageCache('/home/lifangxing/imgs', [ i.getURLImage() for i in t.getItems() ]).start()
	print '**********************' + xbmc.ImageCache.path
	# For Test
	feed(t.endOfDirectory(1))
	# end
	return t

def ListA(name,url,thumb):
	print 'List A **************** ' + url
	link = GetHttpData(url)
	match = re.compile('var PlayList = \["(.+?)"\];').findall(link)   
	vid=match[0]
	print vid
	if len(vid)==32:
		PlayVideo(name,vid,thumb)
	else:
		ListB(name,url,thumb)
    
def ListB(name,url,thumb):
	t = xbmcgui.LevelList()
	print 'List B **************** ' + url
	link = GetHttpData(url)
	match = re.compile('var PlayList = \["(.+?)"\];').findall(link)  
	vid=match[0]
	vidlist=vid.split('","')
	match= re.compile('<a href="#" onclick=.+?>(.+?)</a>').findall(link) 
	for i in range(len(vidlist)):
		#print match[i]
		li = xbmcgui.ListItem(match[i], iconImage = '', thumbnailImage = thumb)
		u = argv[0]+"?mode=10&name="+urllib.quote_plus(match[i])+"&url="+urllib.quote_plus(vidlist[i])+"&thumb="+urllib.quote_plus(thumb)
		t.addDirectoryItem(int(argv[1]), u, li, False, len(vidlist))
	t.setContent(int(argv[1]), 'movies')
	t.endOfDirectory(int(argv[1]))
    
def PlayVideo(name,url,thumb):
	link = GetHttpData('http://ipad.pptv.com/api/ipad/list.js?cb=load.cbs.cb_1&md5='+url)
	print 'http://ipad.pptv.com/api/ipad/list.js?cb=load.cbs.cb_1&md5='+url
	print "PlayVideo link %s " % link
	match = re.compile('"m3u":"(.+?)","').findall(link)   
	url=match[0].replace('\\', '')
	print url
	host=url.replace('http://','')
	host='http://'+host.split('/')[0]+'/'
	#print host
	link = GetHttpData(url)
	#print link
	#EXTINF:10,
	match = re.compile('(/.+?.ts)').findall(link)    
	for i in range(0,len(match)):
		#listitem = xbmcgui.ListItem(name, thumbnailImage = __addonicon__)
		#listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(match))+" 节"})
		fileurl = match[i]
		if fileurl.find('/') == 0:
			fileurl = fileurl[1:len(fileurl)]
		fileurl = fileurl.replace('_0_10.','_0_0.')
		print 'File url: !!!!!!!!!!!!!!-> '+ host+fileurl
		os.system('mplayer '+host+fileurl)
		return host+fileurl

def performChanges(name,type,page,cat):
    catlist = getList(page)
    change = False
    dialog = xbmcgui.Dialog()
    if len(catlist)>0:
        list = [x[1] for x in catlist]
        sel = dialog.select('类型', list)
        if sel != -1:
            cat = catlist[sel][0]
            change = True
            if cat.find('_')!=-1:
                link = GetHttpData('http://ipad.pptv.com/'+cat+'_p1.htm')
                match = re.compile('<dt>全部子分类：</dt>(.+?)</dd>', re.DOTALL).findall(link)
                if match:
                    catlist = re.compile('<a href="(.+?).htm" title="(.+?)"').findall(match[0])
                    if len(catlist)>0:
                        list = [x[1] for x in catlist]
                        dialog = xbmcgui.Dialog()
                        sel = dialog.select('子分类', list)
                        if sel != -1:
                            if catlist[sel][1]!='全部':
                                cat = catlist[sel][0]
    if change:
        progList(name,type,cat,'1')
    
''' 合作商填写 '''
def get_params(code):
    parts = code.split('?')
    argv[0], argv[1] = parts[0] , ' 0 '
    if len(parts) > 1:
        argv[2] = parts[1]

    param = []
    paramstring = argv[2]
    if len(paramstring) >= 2:
        params = argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param

''' 合作商填写, 显示模块调用 '''
def feed(code):
	params = get_params(code)
	mode = None
	name = None
	url = ''
	thumb = None
	type = ''
	cat = ''
	page = ''
	try:
		thumb = urllib.unquote_plus(params["thumb"])
	except:
		pass
	try:
		url = urllib.unquote_plus(params["url"])
	except:
		pass
	try:
		type = urllib.unquote_plus(params["type"])
	except:
		pass
	try:
		cat = urllib.unquote_plus(params["cat"])
	except:
		pass
	try:
		page = urllib.unquote_plus(params["page"])
	except:
		pass
	try:
		name = urllib.unquote_plus(params["name"])
	except:
		pass
	try:
		mode = int(params["mode"])
	except:
		pass

	if mode != None:
		print 'params mode %d' % mode

	if mode == None:
		return rootList()
	elif mode == 1:
		return progList(name,type,cat,page)
	elif mode == 2:
		return ListA(name,url,thumb)
	elif mode == 5:
		return performChanges(name,type,page,cat)
	elif mode == 10:
		return PlayVideo(name,url,thumb)

# For test
if __name__ == '__main__':
	feed("plugin.video.ipadpptv")
# end
