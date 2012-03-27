# -*- coding: utf-8 -*-
import urllib2, urllib, re, string, sys, os, gzip, StringIO
import util
from util import GetHttpData

# 优酷视频(YouKu) by taxigps, 2011

# Plugin constants 
__addonname__ = "优酷视频(YouKu)"
__addonid__ = "plugin.video.youku"
__addon__ = util.Addon(id=__addonid__)
__addonicon__ = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )

UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
ORDER_LIST = [['1','历史最多播放'], ['6','本周最多播放'], ['7','今日最多播放'], ['3','最新上映'], ['9','最近上映'], ['5','最多评论'], ['11','用户好评']]
ORDER_LIST2 = [['1','最新发布'], ['2','最多播放'], ['3','最热话题'], ['8','最具争议'], ['4','最多收藏'], ['5','最广传播'], ['6','用户推荐']]
YEAR_LIST2 = [['1','今日'], ['2','本周'], ['3','本月'], ['4','历史']]
RES_LIST = ['normal', 'high', 'super']
argv = ['']*3
argv[0] = __addonid__
argv[1] = 0
argv[2] =''

def encode(**args):
	return argv[0] + "?" + '&'.join([ "%s=%s"%(x,urllib.quote_plus(str(args[x]))) for x in args ])

def searchDict(dlist,idx):
    for i in range(0,len(dlist)):
        if dlist[i][0] == idx:
            return dlist[i][1]
    return ''

def getList(listpage):
    match0 = re.compile('<label>类型:</label>(.+?)</ul>', re.DOTALL).search(listpage)
    catlist = re.compile('<li.+?>([^<]+)(?:</a>|</span>)</li>').findall(match0.group(1))
    match0 = re.compile('<label>地区:</label>(.+?)</ul>', re.DOTALL).search(listpage)
    arealist = re.compile('<li.+?>([^<]+)(?:</a>|</span>)</li>').findall(match0.group(1))
    match0 = re.compile('<label>上映:</label>(.+?)</ul>', re.DOTALL).search(listpage)
    yearlist = re.compile('<li.+?>([^<]+)(?:</a>|</span>)</li>').findall(match0.group(1))
    return catlist,arealist,yearlist

def getList2(listpage, cat):
    match0 = re.compile('<label>类型:</label>(.+?)</ul>', re.DOTALL).search(listpage)
    if match0:
        catlist = re.compile('<li><a href="/v_showlist/[^g]*g([0-9]+)[^\.]*.html"[^>]*>(.+?)</a></li>').findall(match0.group(1))
        match1 = re.compile('<li class="current"><span>(.+?)</span>').search(match0.group(1))
        if match1:
            catlist.append([cat,match1.group(1)])
    else:
        catlist = []
    return catlist

def getRootMenu():
    t = util.Menu()
    link = GetHttpData('http://www.youku.com/v/')
    if link == None:
        return None
    match0 = re.compile('<div class="left">(.+?)<!--left end-->', re.DOTALL).search(link)
    match = re.compile('<li><a href="/([^/]+)/([^\.]+)\.html"[^>]+>(.+?)</a></li>').findall(match0.group(1))
    totalItems = len(match)
    for path, id, name in match:
        if path == 'v_olist':
            u = encode(mode=1, name=name, id=id, cat='不限', area='不限', year='不限', order='7')
        else:
            u = encode(mode=11, name=name, id=id, cat='0', year='1',order='2')
        li = util.MenuItem(name)
        t.addDirectoryItem(int(argv[1]),u,li,True,totalItems)
	# Test
    #decode(t.endOfDirectory(int(argv[1])))
	# end
    return t

def progList(name,id,page,cat,area,year,order):
	t = util.Menu()
	if cat == '不限':
		catstr = ''
	else:
		catstr = cat
	if area == '不限':
		areastr = ''
	else:
		areastr = area
	if year == '不限':
		yearstr = ''
	elif year.find('年代')>0:
		yearstr = '19' + year[0:2]
	else:
		yearstr = year
	url = 'http://www.youku.com/v_olist/'+id+'_a_'+areastr+'_s__g_'+catstr+'_r_'+yearstr+'_o_'+order
	if page:
		url = url + '_p_' + page
		currpage = int(page)
	else:
		currpage = 1
	url += '.html'
	link = GetHttpData(url)
	if link == None:
		return None
	match = re.compile('<ul class="pages">(.+?)</ul>', re.DOTALL).findall(link)
	if len(match):
		match1 = re.compile('<li.+?>([0-9]+)(</a>|</span>)</li>', re.DOTALL).findall(match[0])
		totalpages = int(match1[len(match1)-1][0])
	else:
		totalpages = 1
	match = re.compile('<div class="filter" id="filter">(.+?)<!--filter end-->', re.DOTALL).findall(link)
	if len(match):
		listpage = match[0]
	else:
		listpage = ''
	match = re.compile('<ul class="p">(.+?)</ul>', re.DOTALL).findall(link)
	totalItems = len(match) + 1
	if currpage > 1: totalItems = totalItems + 1
	if currpage < totalpages: totalItems = totalItems + 1
	if cat == '不限':
		catstr = '全部类型'
	else:
		catstr = cat
	if area == '不限':
		areastr = '全部地区'
	else:
		areastr = area
	if year == '不限':
		yearstr = '全部年份'
	else:
		yearstr = year
	# Test
	#li = util.MenuItem(name+'（第'+str(currpage)+'/'+str(totalpages)+'页）【[COLOR FFFF0000]' + catstr + '[/COLOR]/[COLOR FF00FF00]' + areastr + '[/COLOR]/[COLOR FFFFFF00]' + yearstr + '[/COLOR]/[COLOR FF00FFFF]' + searchDict(ORDER_LIST,order) + '[/COLOR]】（按此选择）')
	#u = encode(mode=4, name=name, id=id, cat=cat, area=area, year=year, order=order, page=listpage)
	try:
		cate = getCategorization(listpage)
		cate.setCateCode(mode=4, name=name, id=id, cat=cat, area=area, year=year, order=order, page=listpage)
		t.enableCategorization(cate)
	except Exception, e:
		t.enableCategorization(None)
	# end
	for i in range(0,len(match)):
		match1 = re.compile('/id_(.+?).html"').search(match[i])   
		p_id = match1.group(1)
		match1 = re.compile('<li class="p_thumb"><img src="(.+?)"').search(match[i])
		p_thumb = match1.group(1)
		match1 = re.compile('<li class="p_title"><a [^>]+>(.+?)</a>').search(match[i])
		p_name = match1.group(1)
		match1 = re.compile('<li class="p_status"><span class="status">(.+?)</span>').search(match[i])
		if match1:
			p_name1 = p_name + '（' + match1.group(1) + '）'
		else:
			p_name1 = p_name
		if match[i].find('<span class="ico__SD"')>0:
			p_name1 += '[超清]'
			p_res = 2
		elif match[i].find('<span class="ico__HD"')>0:
			p_name1 += '[高清]'
			p_res = 1
		else:
			p_res = 0
		if match[i].find('<li class="p_ischarge">')>0:
			p_name1 += '[付费节目]'
			# skim non-free
			continue
		print id
		if id in ('c_96','c_95'):
			mode = 2
			isdir = False
		else:
			mode = 3
			isdir = True
		li = util.MenuItem(p_name1, iconImage = '', thumbnailImage = p_thumb)
		#li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
		u = encode(mode=str(mode), name=p_name, id=p_id, thumb=(p_thumb), res=p_res)
		t.addDirectoryItem(int(argv[1]), u, li, isdir, totalItems)

	if currpage > 1:
		li = util.MenuItem('上一页')
		u = encode(mode=1, name=name, id=id,cat=cat, area=area, year=year,order=order,page=str(currpage-1))
		t.addPageItem(u, li)
	if currpage < totalpages:
		li = util.MenuItem('下一页')
		u = encode(mode=1, name=name, id=id,cat=cat, area=area, year=year,order=order,page=str(currpage+1))
		t.addPageItem(u, li)
	t.setContent(int(argv[1]), 'movies')
	# Test
	#decode(t.endOfDirectory(int(argv[1])))
	# end
	return t

def showMediaInfo(data, item=None):
	if item == None:
		item = util.Media()
	try:
		match = re.compile('节目信息(.*?)收藏', re.DOTALL).findall(data)	
		lis = re.compile('<li.*?>(.*?)</li>', re.DOTALL).findall(match[0])
		title_and_year = re.compile('<a.*?>(.*?)</a>.*?<span class="pub">\((.*?)\)</span>', re.DOTALL).findall(lis[0])
		item.setMediaInfo( 'Name', title_and_year[0][0])
		item.setMediaInfo( 'Year', title_and_year[0][1])
		for i in lis:
			if i.find('导演:') != -1: 
				item.setMediaInfo( 'Director', ','.join(re.compile('<a.*?>(.*?)</a>', re.DOTALL).findall(i)) )
			elif i.find('主演:') != -1: 
				item.setMediaInfo( 'Actors', ','.join(re.compile('<a.*?>(.*?)</a>', re.DOTALL).findall(i)) )
			elif i.find('show_info_short') != -1:
				item.setMediaInfo( 'Introduction', ','.join(re.compile('id="show_info_short">(.*?)</span>', re.DOTALL).findall(i)) )
			elif i.find('rating') != -1:
				item.setMediaInfo( 'Score', ','.join(re.compile('<em class="num">(.*?)</em>', re.DOTALL).findall(i)) )
			elif i.find('地区:') != -1: 
				item.setMediaInfo( 'Area', ','.join(re.compile('<a.*?>(.*?)</a>', re.DOTALL).findall(i)) )
			elif i.find('类型:') != -1: 
				item.setMediaInfo( 'Type', ','.join(re.compile('<a.*?>(.*?)</a>', re.DOTALL).findall(i)) )
	except:
		pass
	return item

''' 这是为了在选择列表里的某一视频后在增加一级信息展示而包装了一级ProgList, 由getMovie 调用 '''
def fakeProgList(name, url, thumb, res):
	t = util.Menu()
	li = util.MenuItem(name)
	# mode:10 is PlayVideo
	link = GetHttpData(url)
	if link == None:
		return None
	li.bindMedia( showMediaInfo(link) )
	u = encode(mode=10, name=name, url=url, thumb=thumb, res=str(res))
	t.addDirectoryItem(int(argv[1]), u, li)
	# Test
	#print li.printMediaInfo()
	#decode(t.endOfDirectory(int(argv[1])))
	# end
	return t

def getMovie(name,id,thumb,res):
    if len(id)==21:
        link = GetHttpData('http://www.youku.com/show_page/id_' + id + '.html')
        if link == None:
            return None
		
        match = re.compile('<div class="showbanner">.+?href="(http://v.youku.com/v_show/id_.+?.html)"', re.DOTALL).search(link)
        if match:
            return fakeProgList(name, match.group(1), thumb, res)
            #PlayVideo(name, match.group(1), thumb, res)
    else:
        return fakeProgList(name, 'http://v.youku.com/v_show/id_'+id+'.html', thumb, res)
        #PlayVideo(name, 'http://v.youku.com/v_show/id_'+id+'.html', thumb, res)

def seriesList(name,id,thumb,page):
    t = util.Menu()
    url = "http://www.youku.com/show_eplist/showid_"+id+"_type_pic_from_ajax_page_"+page+".html"
    print url
    currpage = int(page)
    link = GetHttpData(url)
    if link == None:
        return None
    match = re.compile('<ul class="pages">(.+?)</ul>', re.DOTALL).findall(link)
    if len(match):
        match1 = re.compile('<li.+?>([0-9]+)(</a>|</span>)</li>', re.DOTALL).findall(match[0])
        totalpages = int(match1[len(match1)-1][0])
    else:
        totalpages = 1
    match = re.compile('<ul class="v">(.+?)</ul>', re.DOTALL).findall(link)
    totalItems = len(match) + 1
    if currpage > 1: totalItems = totalItems + 1
    if currpage < totalpages: totalItems = totalItems + 1

    # Test
    #li = util.MenuItem("当前节目："+name+'（第'+str(currpage)+'/'+str(totalpages)+'页）')
    #u=argv[0]+"?mode=40&name="+urllib.quote_plus(name)
    #t.addDirectoryItem(int(argv[1]), u, li, True, totalItems)
    # end
    media = None
    for i in range(0,len(match)):
        match1 = re.compile('<li class="v_link"><a .*?href="(http://v.youku.com/v_show/id_.+?.html)"').search(match[i])
        if match1:
            p_url = match1.group(1)
            ''' Media Infomation get in here , and make sure run here once'''
            if media is None:
                link = GetHttpData(p_url)
                if link == None:
                    return None
                media = showMediaInfo(link, media)
        else:
            continue
        match1 = re.compile('<li class="v_thumb"><img src="(.+?)"').search(match[i])
        p_thumb = match1.group(1)
        match1 = re.compile('<li class="v_title">[\s]*<a [^>]+>(.+?)</a>').search(match[i])
        p_name = match1.group(1)
        if match[i].find('<span class="ico__SD"')>0:
            p_name += '[超清]'
            p_res = 2
        elif match[i].find('<span class="ico__HD"')>0:
            p_name += '[高清]'
            p_res = 1
        else:
            p_res = 0
        li = util.MenuItem(p_name, iconImage = '', thumbnailImage = p_thumb)
        li.bindMedia(media)
        u = encode(mode=10, name=p_name, url=p_url, thum=p_thumb, res=str(p_res))
        t.addDirectoryItem(int(argv[1]), u, li, False, totalItems)

    if currpage > 1:
        li = util.MenuItem('上一页')
        u = encode(mode=3, name=name, id=id, thumb=thumb, page=str(currpage-1))
        t.addPageItem(u, li)
    if currpage < totalpages:
        li = util.MenuItem('下一页')
        u = encode(mode=3, name=name, id=id, thumb=thumb, page=str(currpage+1))
        t.addPageItem(u, li)
    t.setContent(int(argv[1]), 'movies')
	# Test
    #t[1].printMediaInfo()
    #decode(t.endOfDirectory(int(argv[1])))
	# end
    return t

def progList2(name,id,page,cat,year,order):
    t = util.Menu()

    url = 'http://www.youku.com/v_showlist/t'+order+'d'+year+id+'g'+cat
    if page:
        url += 'p' + page
        currpage = int(page)
    else:
        currpage = 1
    url += '.html'
    link = GetHttpData(url)
    if link == None:
        return None	
    match = re.compile('<ul class="pages">(.+?)</ul>', re.DOTALL).findall(link)
    if len(match):
        match1 = re.compile('<li.+?>([0-9]+)(</a>|</span>)</li>', re.DOTALL).findall(match[0])
        totalpages = int(match1[len(match1)-1][0])
    else:
        totalpages = 1
    match = re.compile('<div class="filter" id="filter">(.+?)<!--filter end-->', re.DOTALL).findall(link)
    if len(match):
        listpage = match[0]
    else:
        listpage = ''
    catlist = getList2(listpage, cat)
    match = re.compile('<ul class="v">(.+?)</ul>', re.DOTALL).findall(link)
    totalItems = len(match) + 1
    if currpage > 1: totalItems = totalItems + 1
    if currpage < totalpages: totalItems = totalItems + 1
    if cat == '0':
        catstr = '全部类型'
    else:
        catstr = searchDict(catlist,cat)
    # Test
    try:
        cate = getCategorization2(listpage, cat)
        cate.setCateCode(mode=12, name=name, id=id, cat=cat, year=year, order=order, page=listpage)
        t.enableCategorization(cate)
    except Exception,e:
        t.enableCategorization(None);
    # end
    for i in range(0,len(match)):
        match1 = re.compile('<li class="v_link"><a href="(http://v.youku.com/v_show/id_.+?.html)"').search(match[i])
        p_url = match1.group(1)
        match1 = re.compile('<li class="v_thumb"><img src="(.+?)"').search(match[i])
        p_thumb = match1.group(1)
        match1 = re.compile('<li class="v_title"><a [^>]+>(.+?)</a>').search(match[i])
        p_name = match1.group(1).replace('&quot;','"')
        if match[i].find('<span class="ico__SD"')>0:
            p_name += '[超清]'
            p_res = 2
        elif match[i].find('<span class="ico__HD"')>0:
            p_name += '[高清]'
            p_res = 1
        else:
            p_res = 0
        li = util.MenuItem(p_name, iconImage = '', thumbnailImage = p_thumb)
        u = encode(mode=10, name=p_name, url=p_url, thumb=p_thumb, res=p_res)
        t.addDirectoryItem(int(argv[1]), u, li, False, totalItems)

    if currpage > 1:
        li = util.MenuItem('上一页')
        u = encode(mode=11, name=name, id=id, cat=cat, year=year, order=order, page=str(currpage-1))
        t.addPageItem(u, li)
    if currpage < totalpages:
        li = util.MenuItem('下一页')
        u = encode(mode=11, name=name, id=id, cat=cat, year=year, order=order, page=str(currpage+1))
        t.addPageItem(u, li)
    t.setContent(int(argv[1]), 'movies')
	# Test
    #decode(t.endOfDirectory(int(argv[1])))
	# end
    return t

def PlayVideo(name,url,thumb,res):
	media = util.Media()
	res_limit = int(__addon__.getSetting('movie_res'))
	if res > res_limit:
		res = res_limit
	link = GetHttpData("http://www.flvcd.com/parse.php?kw="+url+"&format="+RES_LIST[res])
	if link == None:
		return None
	match = re.compile('"(http://f.youku.com/player/getFlvPath/.+?)" target="_blank"').findall(link)
	if len(match)>0:
		playlist=util.PlayList(1)
		playlist.clear()
		for i in range(0,len(match)):
			listitem = util.MenuItem(name, thumbnailImage = __addonicon__)
			listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(match))+" 节"})
			playlist.add(match[i], listitem)
		# Test
		#util.Player().play(playlist)
		# end
		media.setPlayList(playlist)
	else:
		if link.find('该视频为加密视频')>0:
			dialog = util.Dialog()
			ok = dialog.ok(__addonname__, '无法播放：该视频为加密视频')
		elif link.find('解析失败，请确认视频是否被删除')>0:
			dialog = util.Dialog()
			ok = dialog.ok(__addonname__, '无法播放：该视频或为收费节目')

	return media

def getCategorization(listpage):
	cate = util.Categorization()
	catlist,arealist,yearlist = getList(listpage)
	
	cate.addCategorization('类型', 'cat', dict([ (x,x) for x in catlist ]))
	cate.addCategorization('地区', 'area', dict([ (x,x) for x in arealist ]))
	cate.addCategorization('年份', 'year', dict([ (x,x) for x in yearlist ]))
	tmp = list(ORDER_LIST)
	for i in tmp:
		i.reverse()
	cate.addCategorization('排序方式', 'order', dict(tmp))
	return cate

def performChanges(name,id,listpage,cat,area,year,order):
    catlist,arealist,yearlist = getList(listpage)
    change = False
    dialog = util.Dialog()
    if len(catlist)>0:
        sel = dialog.select('类型', catlist)
        if sel != -1:
            cat = catlist[sel]
            change = True
    if len(arealist)>0:
        sel = dialog.select('地区', arealist)
        if sel != -1:
            area = arealist[sel]
            change = True
    if len(yearlist)>0:
        sel = dialog.select('年份', yearlist)
        if sel != -1:
            year = yearlist[sel]
            change = True

    lst = [x[1] for x in ORDER_LIST]
    sel = dialog.select('排序方式', lst)
    if sel != -1:
        order = ORDER_LIST[sel][0]
        change = True

    if change:
        return progList(name,id,'1',cat,area,year,order)

def getCategorization2(listpage, cat):
	cate = util.Categorization()
	catlist = getList2(listpage, cat)
	
	cate.addCategorization('类型', 'cat', dict([ (x,x) for x in catlist ]))
	tmp = list(ORDER_LIST2)
	for i in tmp:
		i.reverse()
	cate.addCategorization('排序方式', 'order', dict(tmp))

	tmp = list(YEAR_LIST2)
	for i in tmp:
		i.reverse()
	cate.addCategorization('统计周期', 'year', dict(tmp))
	return cate

def performChanges2(name,id,listpage,cat,year,order):
    catlist = getList2(listpage, cat)
    change = False
    dialog = util.Dialog()
    if len(catlist)>0:
        lst = [x[1] for x in catlist]
        sel = dialog.select('类型', lst)
        if sel != -1:
            cat = catlist[sel][0]
            change = True
    lst = [x[1] for x in ORDER_LIST2]
    sel = dialog.select('排序方式', lst)
    if sel != -1:
        order = ORDER_LIST2[sel][0]
        change = True
    lst = [x[1] for x in YEAR_LIST2]
    sel = dialog.select('统计周期', lst)
    if sel != -1:
        year = YEAR_LIST2[sel][0]
        change = True

    if change:
        return progList2(name,id,'1',cat,year,order)

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
	id = None
	cat = None
	area = None
	year = None
	order = None
	page = '1'
	url = None
	thumb = None
	res = 0

	try:
		res = int(params["res"])
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
		page = urllib.unquote_plus(params["page"])
	except:
		pass
	try:
		order = urllib.unquote_plus(params["order"])
	except:
		pass
	try:
		year = urllib.unquote_plus(params["year"])
	except:
		pass
	try:
		area = urllib.unquote_plus(params["area"])
	except:
		pass
	try:
		cat = urllib.unquote_plus(params["cat"])
	except:
		pass
	try:
		id = urllib.unquote_plus(params["id"])
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

	if mode == None:
		return getRootMenu()
	elif mode == 1:
		return progList(name,id,page,cat,area,year,order)
	elif mode == 2:
		return getMovie(name,id,thumb,res)
	elif mode == 3:
		return seriesList(name,id,thumb,page)
	elif mode == 4:
		return performChanges(name,id,page,cat,area,year,order)
	elif mode == 10:
		return PlayVideo(name,url,thumb,res)
	elif mode == 11:
		return progList2(name,id,page,cat,year,order)
	elif mode == 12:
		return performChanges2(name,id,page,cat,year,order)
	elif mode == 99:
		return fakeProgList(mode, name, url, thumb, res)
# Test
#if __name__ == '__main__':
#	decode('__addonid__')
# end
