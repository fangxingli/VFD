# -*- coding: utf-8 -*-
import urllib2, urllib, re, string, os
import util

# QIYI.COM(奇艺视频) by taxigps, 2011

# Plugin constants 
__addonname__ = "奇艺视频"
__addonid__ = "plugin.video.qiyi"
__addon__ = util.Addon(id=__addonid__)
argv = ['']*3
argv[0] = __addonid__
argv[1] = 0
argv[2] =''

CHANNEL_LIST = [['电影','1'], ['电视剧','2'], ['纪录片','3'], ['动漫','4'], ['音乐','5'], ['综艺','6'], ['娱乐','7'], ['旅游','9']]
CHANNEL_DICT = dict(CHANNEL_LIST)
ORDER_LIST = [['关注','5'], ['最新','2'], ['热播','3'], ['好评','4']]
ORDER_DICT = dict(ORDER_LIST)
PAYTYPE_LIST = [['全部',''], ['免费','0'], ['会员免费','1'], ['付费','2']]
PAYTYPE_DICT = dict(PAYTYPE_LIST)

MOVIE_TYPE_LIST = {}
MOVIE_AREA_LIST = {}
MOVIE_TYPE_LIST['1'] = [['全部',''],['爱情','6'],['战争','7'],['喜剧','8'],['动作','11'],['动画','12'],['悲剧','13'],['灾难','14'],['剧情','127'],['惊悚','128'],['青春','130'],['传记','132'],['恐怖','10'],['魔幻','129'],['科幻','9'],['枪战','131'],['艺术片','133'],]
MOVIE_AREA_LIST['1'] = [['全部',''],['华语','1'],['美国','2'],['欧洲','3'],['韩国','4'],['日本','308'],]
MOVIE_TYPE_LIST['2'] = [['全部',''],['言情','20'],['历史','21'],['战争','22'],['谍战','290'],['武侠','23'],['古装','24'],['传记','25'],['现代','26'],['年代','27'],['都市','28'],['农村','29'],['偶像','30'],['刑侦','31'],['悬疑','32'],['情景','33'],['伦理','35'],['生活','136'],['宫廷','139'],['励志','147'],['革命','142'],['主旋律','137'],['名著','143'],['儿童','36'],['喜剧','135'],['商战','140'],['神话','145'],['罪案','149'],['科幻','34'],['穿越','148'],['青少','144'],['反腐','146'],['戏说','141'],]
MOVIE_AREA_LIST['2'] = [['全部',''],['内地','15'],['港台','16'],['韩国','17'],['美剧','18'],['其他','19'],]
MOVIE_TYPE_LIST['3'] = [['全部',''],['社会','71'],['军事','72'],['探索','73'],['自然','76'],['历史','74'],['人物','70'],['文化','77'],['地理','75'],['旅游','310'],['奇艺','162'],['典藏','79'],['其他','78'],]
MOVIE_AREA_LIST['3'] = []
MOVIE_TYPE_LIST['4'] = [['全部',''],['动作','41'],['亲子','316'],['热血','42'],['冒险','48'],['古代','45'],['未来','46'],['竞技','49'],['体育','50'],['搞笑','51'],['言情','52'],['校园','53'],['都市','54'],['魔幻','55'],['科幻','56'],['励志','297'],['剧情','59'],['悬疑','60'],['宠物','61'],['LOLI','62'],['益智','298'],['童话','299'],['真人','300'],['神话','301'],]
MOVIE_AREA_LIST['4'] = [['全部',''],['大陆','37'],['日本','38'],['美国','39'],['其他','40'],]
MOVIE_TYPE_LIST['5'] = [['全部',''],['流行','222'],['摇滚','224'],['民谣','223'],['Hip-Hop/说唱','227'],['Disco/Club','231'],['爵士/蓝调','228'],['另类','226'],['朋克','234'],['暗潮/哥特','232'],['金属','235'],['独立','237'],['电子','233'],['古典','236'],['民族音乐','238'],['世界音乐','239'],]
MOVIE_AREA_LIST['5'] = [['全部',''],['内地','221'],['港台','220'],['日韩','218'],]
MOVIE_TYPE_LIST['6'] = [['全部',''],['播报','155'],['访谈','156'],['搞笑','157'],['游戏','158'],['选秀','159'],['时尚','160'],['杂谈','161'],['情感','163'],['盛会','292'],['曲艺','293'],]
MOVIE_AREA_LIST['6'] = [['全部',''],['内地','151'],['港台','152'],]
MOVIE_TYPE_LIST['7'] = [['全部',''],['新闻','189'],['访谈','190'],['专题','191'],['宣传片','192'],['花絮','193'],['MV','194'],['独家','169'],['热点','170'],['原创','171'],['电影','172'],['电视','173'],['明星','174'],['八卦','175'],['选秀','176'],['情感','177'],['时尚','178'],['游戏','179'],['搞笑','180'],['音乐','181'],['颁奖','182'],['活动','183'],]
MOVIE_AREA_LIST['7'] = [['全部',''],['内地','184'],['港台','185'],['日韩','186'],['海外','187'],['其它','188'],]
MOVIE_TYPE_LIST['9'] = [['全部',''],['风光','354'],['饮食','355'],['出行','638'],['住宿','356'],]
MOVIE_AREA_LIST['9'] = [['全部',''],['安徽','599'],['北京','576'],['河南','607'],['湖南','611'],['江苏','595'],['辽宁','589'],['西藏','625'],['埃及','567'],['澳大利亚','559'],['法国','520'],['马尔代夫','460'],['日本','426'],['新西兰','380'],['意大利','371'],]

def GetHttpData(url):
	try:
		print "GetHttpData %s " % url 
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req, timeout=10)
		httpdata = response.read()
		response.close()
		httpdata = re.sub("\s", "", httpdata)
		return httpdata
	except urllib2.URLError, e:
		raise NetworkError, 'network error'
		return None

def encode(**args):
    return argv[0] + "?" + '&'.join([ "%s=%s"%(x,urllib.quote_plus(str(args[x]))) for x in args ])

def urlExists(url):
    try:
        resp = urllib2.urlopen(url, timeout=3)
        result = True
        resp.close()
    except urllib2.URLError, e:
        #print e
        result = False
    return result

def getPlayURL(html):
    match1 = re.compile('pid:"(.+?)",//').findall(html)
    if len(match1) > 0:
        pid = match1[0]
        match1 = re.compile('ptype:"(.+?)",//').findall(html)
        ptype = match1[0]
        match1 = re.compile('videoId:"(.+?)",//').findall(html)
        videoId = match1[0]
        url = 'http://cache.video.qiyi.com/v/' + videoId + '/' + pid + '/' + ptype + '/'
    else:
        url = ''
    return url

def searchDict(dlist,id,idx):
    for i in range(0,len(dlist[id])):
        if dlist[id][i][0] == idx:
            return dlist[id][i][1]
    return ''

def getRootMenu():
	t = util.Menu()

	for i in CHANNEL_LIST:
		li=util.MenuItem(i[0])
		u = encode(mode=4, channel=i[0])
		t.addDirectoryItem(int(argv[1]),u,li,True)

	# Test
	#decode(t.endOfDirectory(int(argv[1])))
	# end
	return t

def progList():
	t = util.Menu()
	c1 = ''
	c2 = ''
	c3 = ''
	c4 = ''
	page = __addon__.getSetting('page')
	currpage = int(page)
	channel = __addon__.getSetting('channel')
	print '----------------> ' + str(channel)
	id = CHANNEL_DICT[channel]
	movie_area = __addon__.getSetting('movie_area')
	if id == '7':
		c3 = searchDict(MOVIE_AREA_LIST,id,movie_area)
	elif id == '9':
		c2 = searchDict(MOVIE_AREA_LIST,id,movie_area)
	elif id != '3':
		c1 = searchDict(MOVIE_AREA_LIST,id,movie_area)
	movie_type = __addon__.getSetting('movie_type')
	if id == '3' or id == '9':
		c1 = searchDict(MOVIE_TYPE_LIST,id,movie_type)
	elif id == '5':
		c4 = searchDict(MOVIE_TYPE_LIST,id,movie_type)
	else:
		c2 = searchDict(MOVIE_TYPE_LIST,id,movie_type)
	order = __addon__.getSetting('order')
	paytype = '免费'
	print "progList order = %s" % order
	print "progList paytype = %s" % paytype
	c13 = ORDER_DICT[order]
	cpaytype = PAYTYPE_DICT[paytype]
	url = 'http://list.qiyi.com/www/' + id + '/' + c1 + '-' + c2 + '-' + c3 + '-' + c4 + '-------' + cpaytype + '--' + c13 + '-1-' + page + '----.html'
	link = GetHttpData(url)
	match1 = re.compile('data-key="([0-9]+)"').findall(link)
	if len(match1) == 0:
		totalpages = 1
	else:
		totalpages = int(match1[len(match1) - 1])
	if id in ['5','7','9']:
		match = re.compile('<li><ahref="(.+?)"class="(.*?)"><.+?src="(.+?)"title="(.+?)"alt="').findall(link)
	else:
		match = re.compile('<li><ahref="(.+?)"class="(.*?)"><.+?src="(.+?)"title="(.+?)"alt=".+?<spanid="fenshu"class="fRed"><strong>(.+?)</strong>(.*?)</span><spanclass="fBlack"></span>（(.*?)评）</p></li>').findall(link)
	totalItems = len(match) + 2
	if currpage > 1: totalItems = totalItems + 1
	if currpage < totalpages: totalItems = totalItems + 1

	'''
	节目分类
	li = util.MenuItem('节目分类[COLOR FF00FF00]【' + channel + '】[/COLOR]（按此选择）')
	u = argv[0] + "?mode=4"
	t.addDirectoryItem(int(argv[1]), u, li, True, totalItems)
	'''

	'''
	筛选分类
	li = util.MenuItem('类型[COLOR FFFF0000]【' + movie_type + '】[/COLOR] 地区[COLOR FFFF0000]【' + movie_area + '】[/COLOR] 排序[COLOR FFFF0000]【' + order + '】[/COLOR]（按此选择）')
	u = argv[0] + "?mode=5"
	t.addDirectoryItem(int(argv[1]), u, li, True, totalItems)
	'''

	for i in range(0,len(match)):
		p_url = match[i][0]
		p_name = match[i][3]
		if match[i][1].find('chaoqing_pic') != -1:
			p_name = p_name + '(超清)'
		p_thumb = match[i][2]
		if id in ['5','7','9']:
			p_rating = 0
			p_votes = ''
		else:
			p_rating = float(match[i][4] + match[i][5])
			p_votes = match[i][6]
		li = util.MenuItem(p_name, iconImage = '', thumbnailImage = p_thumb)
		u = encode(mode=6, name=p_name, url=p_url, thumb=p_thumb)
		t.addDirectoryItem(int(argv[1]), u, li, False, totalItems)

	if currpage > 1:
		#li = util.MenuItem('上一页（第'+page+'页/共'+str(totalpages)+'页）')
		li = util.MenuItem('上一页')
		u = encode(mode=1, page=str(currpage-1))
		t.addPageItem(u, li)
	if currpage < totalpages:
		#li = util.MenuItem('下一页（第'+page+'页/共'+str(totalpages)+'页）')
		li = util.MenuItem('下一页')
		u = encode(mode=1, page=str(currpage+1))
		print '==========================> ' + str(page)
		t.addPageItem(u, li)
	t.setContent(int(argv[1]), 'movies')

	# Test
	#decode(t.endOfDirectory(int(argv[1])))
	# end
	return t

def fakeProgList(p_name, url, p_thumb):
	link = GetHttpData(url)
	v_url = getPlayURL(link)
	if v_url != '':
		t = util.Menu()
		# 能够获取播放页面，为单个视频
		match1 = re.compile('上映年份：<ahref=".*?">([0-9]*)').findall(link)
		if len(match1) == 0:
			match1 = re.compile('出品年份：<!--.*?-->([0-9]*)').findall(link)
		if len(match1) == 0:
			p_year = 0
		else:
			p_year = int(match1[0])
		match1 = re.compile('导演：<ahref=".*?">(.*?)</a>').findall(link)
		if len(match1) == 0:
			p_director = ''
		else:
			p_director = match1[0]
		p_cast = re.compile('class="f14">(.*?)</a>饰演<spanclass="f14">(.*?)</span>').findall(link)
		match1 = re.compile('<pid="desc1".*?>(.*?)</p>').findall(link)
		if len(match1) == 0:
			p_plot = ''
		else:
			p_plot = match1[0]
		li = util.MenuItem(p_name, iconImage = '', thumbnailImage = p_thumb)
		li.bindMedia(util.Media())
		u = encode(mode=2, name=p_name, url=v_url, thumb=p_thumb)
		t.addDirectoryItem(int(argv[1]), u, li, False)

		# Test
		#decode(t.endOfDirectory(int(argv[1])))
		# end
		return t
	else:
		# 无法获取播放页面，为剧集
		match1 = re.compile('年份：<ahref=".*?">([0-9]*)').findall(link)
		if len(match1) == 0:
			match1 = re.compile('出品年份：([0-9]*)').findall(link)
		if len(match1) == 0:
			p_year = 0
		else:
			p_year = int(match1[0])
		match1 = re.compile('导演：<ahref=".*?">(.*?)</a>').findall(link)
		if len(match1) == 0:
			p_director = ''
		else:
			p_director = match1[0]
		p_cast = re.compile('class="f14">(.*?)</a>饰演<spanclass="f14">(.*?)</span>').findall(link)
		match1 = re.compile('<pclass="zhuanjiP2">(.*?)</p>').findall(link)
		if len(match1) == 0:
			p_plot = ''
		else:
			p_plot = match1[0]
		return seriesList(url, p_name, p_thumb)
		'''
		li = util.MenuItem(p_name, iconImage = '', thumbnailImage = p_thumb)
		u = encode(mode=3, name=p_name, url=url, thumb=p_thumb)
		li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Cast":p_cast, "Plot":p_plot, "Year":p_year, "Rating":p_rating, "Votes":p_votes})
		t.addDirectoryItem(int(argv[1]), u, li, True, totalItems)
		'''

def seriesList(url, name, thumb):
	t = util.Menu()
	link = GetHttpData(url)
	match1 = re.compile('年份：<ahref=".*?">([0-9]*)').findall(link)
	if len(match1) == 0:
		match1 = re.compile('出品年份：([0-9]*)').findall(link)
	if len(match1) == 0:
		p_year = 0
	else:
		p_year = int(match1[0])
	match1 = re.compile('导演：<ahref=".*?">(.*?)</a>').findall(link)
	if len(match1) == 0:
		p_director = ''
	else:
		p_director = match1[0]
	p_cast = re.compile('class="f14">(.*?)</a>饰演<spanclass="f14">(.*?)</span>').findall(link)
	#    match1 = re.compile('<divid="j-album-[^>]*>(.*?)</div>').findall(link)
	match1 = re.compile('<divid="j-album-[0-9]+[^>]*>(.*?)</div>').findall(link)
	album = ''
	for url1 in match1:
		album = album + GetHttpData('http://www.qiyi.com' + url1)
	match2 = re.compile('<divid="j-desc-[0-9]+[^>]*>(.*?)</div>').findall(link)
	desc = ''
	for url1 in match2:
		desc = desc + GetHttpData('http://www.qiyi.com' + url1)
	#    match = re.compile('<li><ahref="(.+?)"class="imgBg1"><.+?src="(.+?)"title="(.+?)".*?"').findall(album)
	match = re.compile('<li><ahref="(.+?)"class="a_bar"><.+?data-lazy="(.+?)"title="(.+?)"').findall(album)
	totalItems = len(match)
	if totalItems==0:
		match1 = re.compile('"tvPictureUrl":"(.+?)","producers').findall(link)
		p_thumb=match1[0]
		match = re.compile('<ahref="(.+?)">(.+?)</a>').findall(album)
		totalItems = len(match) 
		for p_url,p_name in match:
			match1 = re.compile('<ahref="' + p_url + '">' + p_name + '</a></span><pstyle=.*?>(.*?)</p>').findall(desc)
			if len(match1) > 0:
				p_plot = match1[0].replace('&nbsp;','')
			else:
				p_plot = ''
			p_name =  name + '(' + p_name + ')'
			li = util.MenuItem(p_name, iconImage = '', thumbnailImage = p_thumb)
			li.bindMedia(util.Media())
			li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Cast":p_cast, "Plot":p_plot, "Year":p_year})
			u = argv[0] + "?mode=2&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)+ "&thumb=" + urllib.quote_plus(p_thumb)
			t.addDirectoryItem(int(argv[1]), u, li, False, totalItems)
	else:
		for p_url, p_thumb, p_name in match:
	#            match1 = re.compile('<ahref="' + p_url + '">' + p_name + '</a></span><pstyle=.*?>(.*?)</p>').findall(desc)
			match1 = re.compile('<ahref="' + p_url + '">' + p_name + '</a></dt><dd>(.*?)</dd>').findall(desc)
			if len(match1) > 0:
				p_plot = match1[0].replace('&nbsp;','')
			else:
				p_plot = ''
			li = util.MenuItem(p_name, iconImage = '', thumbnailImage = p_thumb)
			li.bindMedia(util.Media())
			li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Cast":p_cast, "Plot":p_plot, "Year":p_year})
			u = argv[0] + "?mode=2&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)+ "&thumb=" + urllib.quote_plus(p_thumb)
			t.addDirectoryItem(int(argv[1]), u, li, False, totalItems)
	t.setContent(int(argv[1]), 'episodes')

	# Test
	#decode(t.endOfDirectory(int(argv[1])))
	# end
	return t

def PlayVideo(url,name,thumb):
	media = util.Media()
	if url.find('http://cache.video.qiyi.com/v/') == -1:
		link = GetHttpData(url)
		url = getPlayURL(link)
	link = GetHttpData(url)
	match=re.compile('<file>http://data.video.qiyi.com/videos/([^/]+?)/(.+?)</file>').findall(link)
	playlist=util.PlayList(1)
	playlist.clear()
	listitem = util.MenuItem(name, thumbnailImage = thumb)
	media.setMediaInfo('Title', name)
	#listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(1)+"/"+str(len(match))+" 节"})
	if urlExists('http://qiyi.soooner.com/videos2/'+match[0][0]+'/'+match[0][1]):
		baseurl = 'http://qiyi.soooner.com/videos2/'
	else:
		baseurl = 'http://qiyi.soooner.com/videos/'
	playlist.add(baseurl+match[0][0]+'/'+match[0][1], listitem = listitem)
	for i in range(1,len(match)):
		listitem=util.MenuItem(name, thumbnailImage = thumb)
		#listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(match))+" 节"})
		playlist.add(baseurl+match[i][0]+'/'+match[i][1], listitem = listitem)
	media.setPlayList(playlist)
	# Test
	#util.Player().play(playlist)
	# end

	return media

def performChannel(channel):
	'''
	dialog = util.Dialog()
	list = [x[0] for x in CHANNEL_LIST]
	sel = dialog.select('节目分类', list)
	'''
	__addon__.setSetting(id="channel", value=channel)
	__addon__.setSetting(id="movie_type", value='全部')
	__addon__.setSetting(id="movie_area", value='全部')
	__addon__.setSetting(id="order", value='最新')
	__addon__.setSetting(id="page", value="1")
	if __addon__.getSetting('remember_dir') == "true":
		return progList()

def performChanges():
    change = False
    channel = __addon__.getSetting('channel')
    id = CHANNEL_DICT[channel]
    dialog = util.Dialog()
    list = [x[0] for x in MOVIE_TYPE_LIST[id]]
    sel = dialog.select('类型', list)
    if sel != -1:
        __addon__.setSetting(id="movie_type", value=list[sel])
        __addon__.setSetting(id="page", value="1")
        change = True

    if id != '3':
        list = [x[0] for x in MOVIE_AREA_LIST[id]]
        sel = dialog.select('地区', list)
        if sel != -1:
            __addon__.setSetting(id="movie_area", value=list[sel])
            __addon__.setSetting(id="page", value="1")
            change = True

    list = [x[0] for x in ORDER_LIST]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        __addon__.setSetting(id="order", value=list[sel])
        __addon__.setSetting(id="page", value="1")
        change = True

    if change:
        if __addon__.getSetting('remember_dir') == "true":
            return progList()

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

def decode(code):
	params = get_params(code)
	mode = None
	name = None
	url = None
	thumb = None
	page = None
	channel = None

	try:
		page = urllib.unquote_plus(params["page"])
	except:
		pass
	try:
		thumb = urllib.unquote_plus(params["thumb"])
	except:
		pass
	try:
		url = urllib.unquote_plus(params["url"])
	except:
		pass
	try:
		name = urllib.unquote_plus(params["name"])
	except:
		pass
	try:
		channel = urllib.unquote_plus(params["channel"])
	except:
		pass
	try:
		mode = int(params["mode"])
	except:
		pass

	if mode == None:
		print 'run mode = None'
	else:
		print 'run mode = %d' % mode

	if mode == None:
		return getRootMenu()
	elif mode == 1:
		__addon__.setSetting(id="page", value=page)
		if __addon__.getSetting('remember_dir') == "true":
			return progList()
	elif mode == 2:
		return PlayVideo(url, name, thumb)
	elif mode == 3:
		return seriesList(url, name, thumb)
	elif mode == 4:
		return performChannel(channel)
	elif mode == 5:
		return performChanges()
	elif mode == 6:
		return fakeProgList(name, url, thumb)

# Test
#if __name__ == '__main__':
#	decode(__addonid__)
# end
