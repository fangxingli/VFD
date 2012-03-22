# -*- coding: utf-8 -*-
import urllib2, urllib, re, string, os, gzip, StringIO
import util
from util import GetHttpData

############################################################
# 腾讯视频(v.qq.com) by wow1122(wht9000@gmail.com), 2011
############################################################
# Version 1.0.5 (2012-01-29)
# - Update xml video list access parameters for MV
# - Cleanup progList() & change player for type > '3' 

# Plugin constants 
__addonname__ = "腾讯视频(v.qq.com)"
__addonid__ = "plugin.video.tencent"
__addon__ = util.Addon(id=__addonid__)
__addonicon__ = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )

UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
argv = ['']*3
argv[0] = __addonid__
argv[1] = 0 
argv[2] =''

ORDER_LIST = [['按更新','0'], ['按热度','1'], ['按评分','2']]
ORDER_DICT = dict(ORDER_LIST)

MOVIE_TYPE_LIST = {}
MOVIE_AREA_LIST = {}
MOVIE_YEAR_LIST = {}
MOVIE_TYPE_LIST['1'] = [['全部类型','-1'],['动作','0'],['冒险','1'],['喜剧','3'],['爱情','2'],['动画','16'],['战争','5'],['恐怖','6'],['犯罪','7'],['悬疑','8'],['惊悚','9'],['武侠','10'],['科幻','4'],['音乐','19'],['奇幻','17'],['家庭','18'],['剧情','15'],['伦理','14'],['记录','22'],['历史','13'],]
MOVIE_AREA_LIST['1'] = [['全部地区','-1'],['内地','0'],['港台','1'],['日韩','4'],['欧美','5'],['其他','9999'],]
MOVIE_YEAR_LIST['1'] = [['全部年份','-1'],['2011年','2011'],['2010年','2010'],['2009年','2009'],['2008年','2008'],['2007年','2007'],['2006年','2006'],['2005年','2005'],['2004年','2004'],['2003年','2003'],['2002年','2002'],['2001年','2001'],['其他','9999'],]
MOVIE_TYPE_LIST['2'] = [['全部类型','-1'],['偶像','1'],['喜剧','2'],['爱情','3'],['都市','4'],['古装','5'],['武侠','6'],['历史','7'],['警匪','8'],['家庭','9'],['神话','10'],['剧情','11'],['悬疑','12'],['战争','13'],['军事','14'],['犯罪','15'],['情景','16'],['TVB','17'],]
MOVIE_AREA_LIST['2'] = [['全部地区','-1'],['内地','0'],['香港','1'],['台湾','4'],['韩国','5'],['其他','9999'],]
MOVIE_YEAR_LIST['2'] = [['全部年份','-1'],['2011年','2011'],['2010年','2010'],['2009年','2009'],['2008年','2008'],['2007年','2007'],['2006年','2006'],['其他','9999'],]
MOVIE_TYPE_LIST['3'] = [['全部类型','-1'],['流行','1'],['摇滚','0'],['R&B','2'],['电子','3'],['爵士','4'],['说唱','5'],]
MOVIE_AREA_LIST['3'] = [['全部地区','-1'],['港台','0'],['内地','1'],['日韩','2'],['欧美','3'],['其他','4'],]
MOVIE_YEAR_LIST['3'] = [['全部年份','-1'],['2011年','2011'],['2010年','2010'],['2009年','2009'],['2008年','2008'],['2007年','2007'],]

def getRootMenu():
    t = util.Menu()

    li=util.MenuItem('电影')
    u=argv[0]+"?mode=1&name="+urllib.quote_plus('电影')+"&type="+urllib.quote_plus('2')+"&cat="+urllib.quote_plus('-1')+"&area="+urllib.quote_plus('-1')+"&year="+urllib.quote_plus('-1')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('0')
    t.addDirectoryItem(int(argv[1]),u,li,True)
    li=util.MenuItem('电视剧')
    u=argv[0]+"?mode=1&name="+urllib.quote_plus('电视剧')+"&type="+urllib.quote_plus('3')+"&cat="+urllib.quote_plus('-1')+"&area="+urllib.quote_plus('-1')+"&year="+urllib.quote_plus('-1')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('0')
    t.addDirectoryItem(int(argv[1]),u,li,True)
    li=util.MenuItem('音乐')
    u=argv[0]+"?mode=1&name="+urllib.quote_plus('音乐')+"&type="+urllib.quote_plus('4')+"&cat="+urllib.quote_plus('-1')+"&area="+urllib.quote_plus('-1')+"&year="+urllib.quote_plus('-1')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('0')
    t.addDirectoryItem(int(argv[1]),u,li,True)
    li=util.MenuItem('娱乐')
    u=argv[0]+"?mode=1&name="+urllib.quote_plus('娱乐')+"&type="+urllib.quote_plus('6')+"&cat="+urllib.quote_plus('-1')+"&area="+urllib.quote_plus('-1')+"&year="+urllib.quote_plus('-1')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('0')
    t.addDirectoryItem(int(argv[1]),u,li,True)
    li=util.MenuItem('体育')
    u=argv[0]+"?mode=1&name="+urllib.quote_plus('体育')+"&type="+urllib.quote_plus('5')+"&cat="+urllib.quote_plus('-1')+"&area="+urllib.quote_plus('-1')+"&year="+urllib.quote_plus('-1')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('0')
    t.addDirectoryItem(int(argv[1]),u,li,True)
    li=util.MenuItem('新闻')
    u=argv[0]+"?mode=1&name="+urllib.quote_plus('新闻')+"&type="+urllib.quote_plus('7')+"&cat="+urllib.quote_plus('-1')+"&area="+urllib.quote_plus('-1')+"&year="+urllib.quote_plus('-1')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('0')
    t.addDirectoryItem(int(argv[1]),u,li,True)
    li=util.MenuItem('财经')
    u=argv[0]+"?mode=1&name="+urllib.quote_plus('财经')+"&type="+urllib.quote_plus('8')+"&cat="+urllib.quote_plus('-1')+"&area="+urllib.quote_plus('-1')+"&year="+urllib.quote_plus('-1')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('0')
    t.addDirectoryItem(int(argv[1]),u,li,True)

    # For Test
    #decode(t.endOfDirectory(int(argv[1])))
    # end
    return t
    
def searchDict(dlist,idx):
    for i in range(0,len(dlist)):
        if dlist[i][1] == idx:
            return dlist[i][0]
    return ''

def progList(name,type,page,cat,area,year,order):
	t = util.Menu()
	baseurl='http://sns.video.qq.com/fcgi-bin/txv_lib?'
	if page:
		currpage = int(page)
	else:
		currpage = 0
	url = baseurl + 'mi_mtype='+type+'&mi_type='+cat+ '&mi_area=' +area+ '&mi_year=' + year + '&mi_sort=1&mi_show_type=0&mi_pagenum=' +str(currpage) +'&mi_pagesize=30&otype=xml&mi_online=1&mi_index_type=0'
	if type=='4': url+='&mi_platform=1' 
	link = GetHttpData(url)
	if link == None:
		return None
	match = re.compile('<total>(.+?)</total>', re.DOTALL).findall(link)
	alltotalItems=match[0]
	if int(alltotalItems)%30 > 0:
		totalpages=int(alltotalItems)/30+1
	else:
		totalpages=int(alltotalItems)/30
	match = re.compile('(<movies>.+?</movies>)', re.DOTALL).findall(link)
	totalItems = len(match)
	if currpage > 1: totalItems = totalItems + 1
	if currpage < totalpages: totalItems = totalItems + 1
	if type in ['2','3','4']:
		if cat == '-1':
			catstr = '全部类型'
		else:
			if type=='2':catstr = searchDict(MOVIE_TYPE_LIST['1'],cat)
			elif type=='3':catstr = searchDict(MOVIE_TYPE_LIST['2'],cat)
			elif type=='4':catstr = searchDict(MOVIE_TYPE_LIST['3'],cat)
		if area == '-1':
			areastr = '全部地区'
		else:
			if type=='2':areastr = searchDict(MOVIE_AREA_LIST['1'],area)
			elif type=='3':areastr = searchDict(MOVIE_AREA_LIST['2'],area)
			elif type=='4':areastr = searchDict(MOVIE_AREA_LIST['3'],area)
		if year == '-1':
			yearstr = '全部年份'
		else:
			if type=='2':yearstr = searchDict(MOVIE_YEAR_LIST['1'],year)
			elif type=='3':yearstr = searchDict(MOVIE_YEAR_LIST['2'],year)
			elif type=='4':yearstr = searchDict(MOVIE_YEAR_LIST['3'],year)
		orderstr=searchDict(ORDER_LIST,order)
		# Test
		#li = util.MenuItem('类型[COLOR FFFF0000]【' + catstr + '】[/COLOR] 地区[COLOR FFFF0000]【' + areastr + '】[/COLOR] 年份[COLOR FFFF0000]【' + yearstr + '】[/COLOR] 排序[COLOR FFFF0000]【' + orderstr + '】[/COLOR]（按此选择）')
		#u = argv[0] + "?mode=5&name="+urllib.quote_plus(name)+"&type="+type+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(page)
		#t.addDirectoryItem(int(argv[1]), u, li, True, totalItems)
		# end

	for i in range(0,len(match)):
		matchp = re.compile('<pic_url>(.+?)</pic_url>').search(match[i])
		if matchp: p_thumb = matchp.group(1)
		else: p_thumb = ""
		matchp = re.compile('<title>(.+?)</title>').search(match[i])
		p_name = matchp.group(1)
		match1 = re.compile('<cover_id>(.+?)</cover_id>').search(match[i])

		isDir=False
		if type=='4': #音乐
			p_id = match1.group(1)
			match1 = re.compile('<actor>(.+?)</actor>').search(match[i])
			if match1 != None:
				p_actor =match1.group(1)
				p_actor1=p_actor.split(';')[1]
			else:
				p_actor1 = '暂无'
			li = util.MenuItem(p_actor1+'-'+p_name, iconImage = '', thumbnailImage = p_thumb)
			u = argv[0]+"?mode=3&name="+urllib.quote_plus(p_actor1+'-'+p_name)+"&url="+urllib.quote_plus(p_id)+"&thumb="+urllib.quote_plus(p_thumb)
		else:
			li = util.MenuItem(p_name, iconImage = '', thumbnailImage = p_thumb)
			p_id = match1.group(1)[0]+'/'+match1.group(1)+'.html'
			p_url = 'http://v.qq.com/cover/'+ p_id
			if type=='2': #电影
				u = argv[0]+"?mode=10&name="+urllib.quote_plus(p_name)+"&type=2&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)
			elif type=='3': #电视剧
				isDir=True
				u = argv[0]+"?mode=2&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)
			else:  # Others
				p_id = match1.group(1) 
				u = argv[0]+"?mode=3&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_id)+"&thumb="+urllib.quote_plus(p_thumb)
	   
		#li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
		t.addDirectoryItem(int(argv[1]), u, li, isDir, totalItems)

	order='1'
	cat='-1'
	area='-1'
	year='-1'
	if currpage >= 1:
		li = util.MenuItem('上一页')
		u = argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&baseurl="+urllib.quote_plus(baseurl)+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(currpage-1))
		t.addPageItem(u, li)
	if currpage < totalpages:
		li = util.MenuItem('下一页')
		u = argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&baseurl="+urllib.quote_plus(baseurl)+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(currpage+1))
		t.addPageItem(u, li)
	t.setContent(int(argv[1]), 'movies')
	# For Test
	#decode(t.endOfDirectory(int(argv[1])))
	# end
	return t

def listA(name,url,thumb):
    t = util.Menu()
    print name
    print url
    link = GetHttpData(url)
    if link == None:
        return None
    #media = util.Media()
    #电视剧
    # get TV Media Info
    media = showMediaInfo(link)
    if link.find('sv=""') > 0 :
        match = re.compile('</i><a target="_self".+?id="(.+?)"  title="(.+?)"', re.DOTALL).findall(link)
        totalItems=len(match)
        for p_url,p_name  in match:
            li = util.MenuItem(p_name, iconImage = '', thumbnailImage = thumb)
            li.bindMedia(media)
            u = argv[0] + "?mode=10&name="+urllib.quote_plus(p_name)+"&type=3&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(thumb)
            t.addDirectoryItem(int(argv[1]), u, li, False, totalItems)
    else:
        match = re.compile('</i><a target="_self".+?title="(.+?)".+?sv="(.+?)"', re.DOTALL).findall(link)
        totalItems=len(match)
        for p_name,p_url  in match:
            li = util.MenuItem(p_name, iconImage = '', thumbnailImage = thumb)
            li.bindMedia(media)
            u = argv[0] + "?mode=10&name="+urllib.quote_plus(p_name)+"&type=3&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(thumb)
            t.addDirectoryItem(int(argv[1]), u, li, False, totalItems)
    t.setContent(int(argv[1]), 'movies')
	# For Test
    #media.printMediaInfo()
    #decode(t.endOfDirectory(int(argv[1])))
	#end
    return t
    
def PlayVideo(name,type,url,thumb):
    # get Movie Media Info
    media = util.Media()
    print name
    print '------------------------------------------------>' + url
    if type=='2':
        # 电影
        t = util.Menu()
        link = GetHttpData(url)
        if link == None:
            return None

        match = re.compile('vid:"(.+?)"').findall(link)   
        vid=match[0]

        showMediaInfo(link, media)
        # Test
        #media.printMediaInfo()
        # end
        li = util.MenuItem(name, iconImage = '', thumbnailImage = thumb)
        li.bindMedia(media)
        u = argv[0] + "?mode=10&name="+urllib.quote_plus(name)+"&type=3&url="+vid+"&thumb="+urllib.quote_plus(thumb)
        t.addDirectoryItem(int(argv[1]), u, li, False)

		# Test
        #decode(t.endOfDirectory(1))
        return t

    elif type=='3':
        # 电视剧
        vidlist=url.split('|')
       
    print vidlist
    if len(vidlist)>0:
        playlist=util.PlayList(1)
        playlist.clear()
        for i in range(len(vidlist)):
            listitem = util.MenuItem(name, thumbnailImage = thumb)
            listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(vidlist))+" 节"})
            print vidlist[i]
            p_url = 'http://vv.video.qq.com/geturl?otype=xml&platform=1&format=2&&vid='+vidlist[i]
            link = GetHttpData(p_url)
            if link == None:
                return None
            match = re.compile('<url>(.+?)</url>').findall(link)
            if match:
                playlist.add(match[0], listitem)
            else:
                match =re.compile('<msg>(.+?)</msg>').findall(link)
                if match==None: match[0]=""
                msg = '节目暂时不提供观看: ' + match[0]
                dialog = util.Dialog()
                ok = dialog.ok(__addonname__, msg)
        media.setPlayList(playlist)
        # Test
        #media.printMediaInfo()
        #util.Player().play(playlist)
        # end
    else:
        dialog = util.Dialog()
        ok = dialog.ok(__addonname__, '无法播放：未匹配到视频文件，请稍侯再试.')

    return media

def PlayMv(name,url,thumb):
    print name
    print url
    mv = util.Media()
    li = util.MenuItem(name, thumbnailImage = thumb)
    playlist = util.PlayList(1)
    link = GetHttpData('http://vv.video.qq.com/geturl?otype=xml&platform=1&format=2&&vid='+url)
    if link == None:
        return None
    match = re.compile('<url>(.+?)</url>').findall(link)
    if match:
        playlist.add(match[0])
        # Test
        #util.Player().play(match[0])
        # end
    else:
        dialog = util.Dialog()
        ok = dialog.ok(__addonname__, '无法播放：未匹配到视频文件，请稍侯再试.')
    mv.setPlayList(playlist)
    li.bindMedia(mv)

    return li

def showMediaInfo(data, item=None):
	if item == None:
		item = util.Media()
	try:
		match = re.compile('<div class="mod_info">.*?<h3>(.+?)</h3>.*?<p class=".*?">(.+?)</p>.*?<ul class=".*?">(.*?)</ul>.*?<div class=".*?">(.*?)</div>', re.DOTALL).findall(data)
		item.setMediaInfo( 'Name', re.compile('<a href=".*?">(.*?)</a>', re.DOTALL).findall(match[0][0])[0] )
		lis = re.compile('<li.*?>(.*?)</li>', re.DOTALL).findall(match[0][2])
		
		for i in lis:
			if i.find('导演') != -1:
				item.setMediaInfo( 'Director', ','.join(re.compile('<a.*?>(.*?)</a>', re.DOTALL).findall(i)) )
			elif i.find('主演') != -1:
				item.setMediaInfo( 'Actors', ','.join(re.compile('<a.*?>(.*?)</a>', re.DOTALL).findall(i)) )
			elif i.find('地区') != -1:
				item.setMediaInfo( 'Area', ','.join(re.compile('<a.*?>(.*?)</a>', re.DOTALL).findall(i)) )
			elif i.find('类型') != -1:
				item.setMediaInfo( 'Type', ','.join(re.compile('<a.*?>(.*?)</a>', re.DOTALL).findall(i)) )
			elif i.find('年份') != -1:
				item.setMediaInfo( 'Year', ','.join(re.compile('<a.*?>(.*?)</a>', re.DOTALL).findall(i)) )
			elif i.find('时长') != -1:
				item.setMediaInfo( 'Duration', ','.join(re.compile('([0-9]+)', re.DOTALL).findall(i)) )
		intro_data = re.compile('<p class="mod_cont">(.*?)</p>', re.DOTALL).findall(match[0][3])
		item.setMediaInfo( 'Introduction', intro_data[0].replace('<br/>','') + '...')
	except:
		pass
	return item
        
def performChanges(name,type,page,cat,area,year,order):
    change = False
    dialog = util.Dialog()
    if type=='2':
       list = [x[0] for x in MOVIE_TYPE_LIST['1']]
    elif type=='3':
       list = [x[0] for x in MOVIE_TYPE_LIST['2']]   
    elif type=='4':
       list = [x[0] for x in MOVIE_TYPE_LIST['3']] 
    sel = dialog.select('类型', list)
    if sel != -1:
        if type=='2':
           cat = MOVIE_TYPE_LIST['1'][sel][1]
        elif type=='3':
           cat = MOVIE_TYPE_LIST['2'][sel][1]  
        elif type=='4':
           cat = MOVIE_TYPE_LIST['3'][sel][1] 
        change = True
    if type=='2':
        list = [x[0] for x in MOVIE_AREA_LIST['1']]
    elif type=='3':
        list = [x[0] for x in MOVIE_AREA_LIST['2']]        
    elif type=='4':
        list = [x[0] for x in MOVIE_AREA_LIST['3']]   
    sel = dialog.select('地区', list)
    if sel != -1:
        if type=='2':
           area = MOVIE_AREA_LIST['1'][sel][1]
        elif type=='3':
           area = MOVIE_AREA_LIST['2'][sel][1]        
        elif type=='4':
           area = MOVIE_AREA_LIST['3'][sel][1]  
        change = True
    if type=='2':
        list = [x[0] for x in MOVIE_YEAR_LIST['1']]
    elif type=='3':
        list = [x[0] for x in MOVIE_YEAR_LIST['2']]        
    elif type=='4':
        list = [x[0] for x in MOVIE_YEAR_LIST['3']]
    sel = dialog.select('地区', list)
    if sel != -1:
        if type=='2':
           year = MOVIE_YEAR_LIST['1'][sel][1]
        elif type=='3':
           year = MOVIE_YEAR_LIST['2'][sel][1]        
        elif type=='4':
           year = MOVIE_YEAR_LIST['3'][sel][1]  
        change = True
    list = [x[0] for x in ORDER_LIST]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        order = ORDER_LIST[sel][1]
        change = True

    if change:
        return progList(name,type,'0',cat,area,year,order)

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
	type = ''
	cat = ''
	area = ''
	year = ''
	order = None
	page = '1'
	url = ''
	thumb = None
	res = 0

	try:
		type = urllib.unquote_plus(params["type"])
	except:
		pass
	try:
		res = int(params["res"])
	except:
		pass
	try:
		thumb = urllib.unquote_plus(params["thumb"])
	except:
		pass
	try:
		baseurl = urllib.unquote_plus(params["baseurl"])
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
		return progList(name,type,page,cat,area,year,order)
	elif mode == 2:
		return listA(name,url,thumb)
	elif mode == 3:
		return PlayMv(name,url,thumb)
		
	elif mode == 5:
		return performChanges(name,type,page,cat,area,year,order)
	elif mode == 6:
		return SearchVideo(name,type,url,thumb)
	elif mode == 10:
		return PlayVideo(name,type,url,thumb)

# Test
#if __name__ == '__main__':
#	decode('plugin.video.tencent')
# end
