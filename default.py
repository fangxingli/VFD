# -*- coding: utf-8 -*-
import urllib,urllib2,re,os,xbmcplugin,xbmcgui,xbmc
import xbmcaddon

######################################################
# 音悦台MV
######################################################
# Version 1.4.1 2012-02-19 (cmeng)
# a. xbmcaddon.Addon() needs 1 parameter for Dharma
# b. remove extra " in Artist name listing
# c. addLink: name cannot contain "/" e.g. 12/02/25
######################################################

__addonid__       = "plugin.video.yinyuetai"
__settings__      = xbmcaddon.Addon(id=__addonid__)
__icon__          = xbmc.translatePath( __settings__.getAddonInfo('icon') )
__profile__       = xbmc.translatePath( __settings__.getAddonInfo('profile') )

def Root(ctl):
    j=0
    for i in ctl[None][2]:
        j+=1
        addDir(ctl[i][1],get_realurl(ctl[i][2]),i,'',j)
    
def SubTree(ctl,mode,lists):
    addDir('[COLOR FF00FFFF]'+'当前位置：'+ctl[mode][1]+'[/COLOR]',get_realurl(ctl[mode][2]),mode,'')
    j=0
    for i in lists:
        j+=1
        addDir(ctl[i][1],get_realurl(ctl[i][2]),i,'',j)

def RecommendMV(url,name,mode):
    addDir('[COLOR FF00FFFF]'+'当前位置：推荐MV'+'[/COLOR]',url,mode,'')
    link=get_content(url)
    if link == None: return
    link=re.sub(' ','',link)
    match=re.compile('<inputtype="radio"id="(.+?)"name=\'area\'onclick="javascript:document.location=\'(.+?)\'"value="(.+?)"').findall(link)
    j=0
    for id,url1,name1 in match:
        j+=1
        addDir(name1,get_realurl(url1),mode+1,'',j)

def ListRecommendMV(url,name,mode):
    link=get_content(url)
    if link == None: return
    match0=re.compile('<div class="page-nav">(.+?)</div>').findall(link)   
    curpos=re.sub('推荐','',name)        
    try:
        curpage=re.compile('<span>(.+?)</span>').findall(match0[0])
        addDir('[COLOR FF00FFFF]'+'当前位置：推荐MV>'+curpos+': 第'+curpage[0]+'页'+'[/COLOR]',url,mode,'')
    except:
        addDir('[COLOR FF00FFFF]'+'当前位置：推荐MV>'+curpos+'[/COLOR]',url,mode,'')
        pass
    try:
        matchs=re.compile('<div class="recommend_mv_list"><ul>(.+?)</ul></div>').findall(link)
        matchli=re.compile('<li>(.+?)</li>').findall(matchs[0])
        total=len(matchli)
        j=0
        for item in matchli:
            j+=1
            url1=re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)" title="(.+?)" alt="(.+?)"/>').findall(item)
            p_artist=re.compile('--<a href="(.+?)" title="(.+?)" class="link_people"').findall(item)
            name = url1[0][2]
            artist = p_artist[0][1]
            pic = get_Thumb(url1[0][1])
            vurl=get_flv_url(get_realurl(url1[0][0]))             
            if vurl == None: continue
            addLink(name,artist,vurl,pic,total,j)
    except:
        pass
    try:
        match1=re.compile('<a href="(.+?)">(.+?)</a>').findall(match0[0])
        for pageurl,pagenum in match1:
            if pagenum.isdigit():
                addDir('..第'+pagenum+'页',get_realurl(pageurl),mode,'')
            else:
               addDir('..'+pagenum,get_realurl(pageurl),mode,'')
    except:
        pass
    
def AllMV(url,name,mode):
    addDir('[COLOR FF00FFFF]'+'当前位置：全部MV'+'[/COLOR]',url,mode,'')
    link=get_content(url)
    if link == None: return
    match=re.compile('<li title="(.+?)"><a href="(.+?)"(.+?)>(.+?)</a></li>').findall(link)
    total=len(match)
    if total:
        j=0
        for title,url1,cur,name1 in match:
            j+=1
            addDir('全部MV>'+name1,get_realurl(url1),4,'',j)

def ListAllMV(url,name,mode):
    link=get_content(url)
    if link == None: return
    curpos1=re.compile('<a href="(.+?)" class="current">(.+?)</a>').findall(link)
    curpos2=re.compile('<li title="(.+?)"><a href="(.+?)" class="current">(.+?)</a></li>').findall(link)
    match0=re.compile('<div class="page-nav">(.+?)</div>').findall(link)
    try:
        curpage=re.compile('<span>(.+?)</span>').findall(match0[0])
        addDir('[COLOR FF00FFFF]'+'当前位置：'+curpos1[0][1]+'>'+curpos2[0][2]+': 第'+curpage[0]+'页'+'[/COLOR]',url,mode,'')
    except:
        addDir('[COLOR FF00FFFF]'+'当前位置：'+curpos1[0][1]+'>'+curpos2[0][2]+name+'[/COLOR]',url,mode,'')
        pass
    try:
        matchs=re.compile('<div class="mv_list"><ul>(.+?)</ul></div>').findall(link)
        matchli=re.compile('<div class="thumb">(.+?)</div></li>').findall(matchs[0])
        total=len(matchli)
        j=0
        for item in matchli:
            j+=1
            img=re.compile('<img src="(.+?)"').findall(item)
            title=re.compile('<div class="title"><a href="(.+?)" title="(.+?)" target="_blank"').findall(item)
            artist=re.compile('<div class="artis">--<a href="(.+?)" title="(.+?)" class="link_people"').findall(item)
            name = title[0][1]
            artist = artist[0][1]
            pic = get_Thumb(img[0])
            vurl=get_flv_url(get_realurl(title[0][0])) 
            if vurl == None: continue
            addLink(name,artist,vurl,pic,total,j)
    except:
        pass
    try:
        match1=re.compile('<a href="(.+?)">(.+?)</a>').findall(match0[0])
        for pageurl,pagenum in match1:
            if pagenum.isdigit():
                addDir('..第'+pagenum+'页',get_realurl(pageurl),mode,'')
            else:
                addDir('..'+pagenum,get_realurl(pageurl),mode,'')
    except:
        pass

def get_playlistpage(url,name,mode):
    link=get_content(url)
    if link == None: return
    match0=re.compile('<div class="page-nav">(.+?)</div>').findall(link)
    match=re.compile('<div class="thumb"><a href="(.+?)" target="_blank" title="(.+?)"><img src="(.+?)" alt="(.+?)"><span></span></a></div>').findall(link)
    curpos='当前位置：' + name
    if len(match0):
        curpage=re.compile('<span>(.+?)</span>').findall(match0[0])
        if len(curpage):
            curpos = curpos + ': 第' + curpage[0] +'页'
    addDir('[COLOR FF00FFFF]'+curpos+'[/COLOR]',url,mode,'')
    j=0
    for url1,title,img,title1 in match:
        j+=1
        addDir(title,get_realurl(url1),256,get_Thumb(img),j)
    if len(match0)>0:
        match1=re.compile('<a href="(.+?)" >(.+?)</a>').findall(match0[0])
        for pageurl,pagenum in match1:
            if pagenum.isdigit():
                addDir('..第'+pagenum+'页',get_realurl(pageurl),mode,'')
            else:
                addDir('..'+pagenum,get_realurl(pageurl),mode,'')
        match2=re.compile('<span class="separator">...</span>(.+?)</a><a href="(.+?)" class="nextpage">').findall(match0[0])
        for temp,nextpageurl in match2:
            addDir('..下一页',get_realurl(nextpageurl),mode,'')

def ShowPlayList(url,name,mode):
    link=get_content(url)
    if link == None: return
    pltitle=re.compile('<h2>(.+?)</h2>').findall(link)
    match0=re.compile('<div id="videoList" class="hidden">(.+?)</div><div class="subNav">').findall(link)
    if len(match0):
        match1=re.compile('<div>(.+?)</div>').findall(match0[0])
        total=len(match1)
        if len(match1):
            j=0
            for items in match1:
                j+=1
                match=re.compile('<span name="(.+?)">(.+?)</span>').findall(items)
                name = match[1][1]
                artist = match[3][1]
                pic = get_Thumb(match[4][1])
                vurl=get_flv_url(get_realurl('/video/'+match[0][1])) 
                if vurl == None: continue
                addLink(name,artist,vurl,pic,total,j)

def get_artistpage(url,name,mode,handle):
    link=get_content(url)
    if link == None: return
    match0=re.compile('<div class="page-nav">(.+?)</div>').findall(link)
    matchA=re.compile('<div class="letterCategory">(.+?)</div>').findall(link)
    curpos='当前位置：' + name
    if len(matchA):
        curletter=re.compile('<a href="(.+?)" class="current">(.+?)</a>').findall(matchA[0])
        if len(curletter):
            curpos = curpos + '>' + curletter[0][1]
    if len(match0):
        curpage=re.compile('<span>(.+?)</span>').findall(match0[0])
        if len(curletter):
            curpos = curpos + ': 第' + curpage[0] + '页'
    addDir('[COLOR FF00FFFF]'+curpos+'[/COLOR]',url,mode,'')
    match=re.compile('<span class="groupcover"(.+?)</li>').findall(link)
    if len(match):
        for i in range(0, len(match)):
            match1 = re.compile('fanid=.+?<a href="(.+?)"').search(match[i])
            p_url1 = match1.group(1)
            artistid = p_url1.split('/')[2]
            r_url = get_realurl('/fanclub/mv-all/'+artistid+'/toNew')
        
            match1 = re.compile('<img.+?src="(.+?)"/>').search(match[i])
            p_img = match1.group(1)          

            match1 = re.compile('<div class="info">.+?<a href="(.+?)"').search(match[i])
            p_url2 = match1.group(1)

            match1 = re.compile('class="song" title="(.+?)">').search(match[i])
            title = match1.group(1)
                    
            addDir(title,r_url,handle,get_Thumb(p_img),i+1)
    if len(matchA):
        matchB=re.compile('<a href="(.+?)" >(.+?)</a>').findall(matchA[0])
        for letterurl,letter in matchB:
            addDir(letter,get_realurl(letterurl),mode,'')
    if len(match0):
        match1=re.compile('<a href="(.+?)">(.+?)</a>').findall(match0[0])
        for pageurl,pagenum in match1:
            if pagenum.isdigit():
                addDir('..第'+pagenum+'页',get_realurl(pageurl),mode,'')
            else:
                addDir('..'+pagenum,get_realurl(pageurl),mode,'')
        match2=re.compile('<span class="separator">...</span>(.+?)</a><a href="(.+?)" class="nextpage">').findall(match0[0])
        for temp,nextpageurl in match2:
            addDir('..下一页',get_realurl(nextpageurl),mode,'')

def ShowArtistMV(url,name,mode):
    link=get_content(url)
    if link == None: return
    link=re.sub('&quot;','"',link)
    artist=re.compile('<h1>(.+?)</h1>').findall(link)
    match0=re.compile('<div class="page-nav">(.+?)</div>').findall(link)
    curpos='当前位置：歌手>'
    if len(artist):
        curpos=curpos+artist[0]
    if len(match0):
        curpage=re.compile('<span>(.+?)</span>').findall(match0[0])
        if len(curpage):
            curpos = curpos + ': 第' + curpage[0] + '页'
    addDir('[COLOR FF00FFFF]'+curpos+'[/COLOR]',url,mode,'')

    vlist=re.compile('<div class="mv_list"><ul>(.+?)</ul></div>').findall(link)
    match=re.compile('<div class="thumb"><a target="_blank" title="(.+?)" href="(.+?)"><img.+?src="(.+?)"').findall(vlist[0])    
    total=len(match)
    if len(match):
        j=0
        artist = artist[0]
        for name,url1,img in match:
            j+=1
            pic = get_Thumb(img)
            vurl=get_flv_url(get_realurl(url1)) 
            if vurl == None: continue
            addLink(name,artist,vurl,pic,total,j)            
    if len(match0):
        match1=re.compile('<a href="(.+?)">(.+?)</a>').findall(match0[0])
        if len(match1):
            for pageurl,pagenum in match1:
                if pagenum.isdigit():
                    addDir('..第'+pagenum+'页',get_realurl(pageurl),mode,'')
                else:
                    addDir('..'+pagenum,get_realurl(pageurl),mode,'')
                    
def ShowFocusMV(url,name,mode):
    curpos = '当前位置：'+name
    addDir('[COLOR FF00FFFF]'+curpos+'[/COLOR]', url, mode,'')
    link=get_content(url)
    if link == None: return
    matchs=re.compile('<div class="mv_list"><ul>(.+?)</ul></div>').findall(link)
    if len(matchs):
        matchli=re.compile('<div class="thumb">(.+?)</div></li>').findall(matchs[0])
        total=len(matchli)
        if total:
            j=0
            for item in matchli:
                j+=1
                img=re.compile('<img src="(.+?)"').findall(item)
                title=re.compile('<div class="title"><a href="(.+?)" title="(.+?)" target="_blank" class="song">').findall(item)
                p_artist=re.compile('--<a href="(.+?)" title="(.+?)" class="artist" target="_blank">').findall(item)
                name = title[0][1]                
                artist = p_artist[0][1]
                pic = get_Thumb(img[0])
                vurl=get_flv_url(get_realurl(title[0][0]))
                if vurl == None: continue
                addLink(name,artist,vurl,pic,total,j)

def get_flv_url(url):
    link=get_content('http://www.flvcd.com/parse.php?kw='+url)
    if link == None: return
    link=re.sub(" ","",link)
    match=re.compile('下载地址：<ahref="(.+?)"target="_blank"class="link"').findall(link)
    if len(match):
        return match[0]
    return
    
def get_realurl(url):
    return 'http://www.yinyuetai.com'+url

def get_content(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    try:
        response = urllib2.urlopen(req)
    except:
        return None
    httpdata=response.read()
    response.close()
    httpdata=re.sub('\r|\n|\t','',httpdata)
    match = re.compile('<meta.+?charset=["]*(.+?)"').findall(httpdata)
    if len(match):
        charset = match[0].lower()
        if (charset != 'utf-8') and (charset != 'utf8'):
            httpdata = unicode(httpdata, charset,'replace').encode('utf8')
    if len(httpdata) < 5: return None
    return httpdata

def get_Thumb(icon):
    if len(icon) < 2:
        return __icon__
    pic = __profile__ + icon.split('?')[0]
    if not os.path.isfile(pic):
        if not os.path.isdir(os.path.dirname(pic)):
            os.makedirs(os.path.dirname(pic))
        try:
            pic=urllib.urlretrieve(get_realurl(icon), pic)[filename]
        except:
            pass
    return pic
          
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
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

def addLink(name,artist,url,pic,total,sn):
#    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&artist="+urllib.quote_plus(artist)
    name=re.sub('/','-',name) #cannot contains "/" e.g. 12/02/18
    ok=True
    li=xbmcgui.ListItem(str(sn)+'. '+name+' 【'+artist+'】',iconImage=pic, thumbnailImage=pic)
    li.setInfo( type="Video", infoLabels={ "Title": name,"Artist": artist } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=li,totalItems=total)
    return ok

def addDir(name,url,mode,pic,sn=''):
    if sn != '': sn=str(sn)+". "
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    li=xbmcgui.ListItem(sn+name,'', pic, pic)
    li.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=li,isFolder=True)
    return ok

params=get_params()
url=None
name=None
mode=None
artist=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    artist=urllib.unquote_plus(params["artist"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass

ctl = {
            None : ('Root(ctl)','音悦台MV',(80,81,82,83,84,85,90,91,92,93,94,95,96)),
            1    : ('RecommendMV(url,name,mode)','推荐MV','/lookVideo'),
            2    : ('ListRecommendMV(url,name,mode)','推荐MV'),
            4    : ('ListAllMV(url,name,mode)','全部MV'),
            8    : ('SubTree(ctl,mode,(9,10,11,12))','热门评论悦单','/pl/playlist_hotComment'),
            9    : ('get_playlistpage(url,ctl[mode][1],mode)','24小时热门评论悦单','/pl/playlist_hotComment/today'),
            10   : ('get_playlistpage(url,ctl[mode][1],mode)','本周热门评论悦单','/pl/playlist_hotComment/week'),
            11   : ('get_playlistpage(url,ctl[mode][1],mode)','本月热门评论悦单','/pl/playlist_hotComment/month'),
            12   : ('get_playlistpage(url,ctl[mode][1],mode)','全部热门评论悦单','/pl/playlist_hotComment/all'),
            13   : ('SubTree(ctl,mode,(14,15,16,17))','热门收藏悦单','/pl/playlist_hotFavorite'),
            14   : ('get_playlistpage(url,ctl[mode][1],mode)','24小时热门收藏悦单','/pl/playlist_hotFavorite/today'),
            15   : ('get_playlistpage(url,ctl[mode][1],mode)','本周热门收藏悦单','/pl/playlist_hotFavorite/week'),
            16   : ('get_playlistpage(url,ctl[mode][1],mode)','本月热门收藏悦单','/pl/playlist_hotFavorite/month'),
            17   : ('get_playlistpage(url,ctl[mode][1],mode)','全部热门收藏悦单','/pl/playlist_hotFavorite/all'),
            18   : ('SubTree(ctl,mode,(19,20,21,22))','热门推荐悦单','/pl/playlist_hotRecommend'),
            19   : ('get_playlistpage(url,ctl[mode][1],mode)','24小时热门推荐悦单','/pl/playlist_hotRecommend/today'),
            20   : ('get_playlistpage(url,ctl[mode][1],mode)','本周热门推荐悦单','/pl/playlist_hotRecommend/week'),
            21   : ('get_playlistpage(url,ctl[mode][1],mode)','本月热门推荐悦单','/pl/playlist_hotRecommend/month'),
            22   : ('get_playlistpage(url,ctl[mode][1],mode)','全部热门推荐悦单','/pl/playlist_hotRecommend/all'),
            23   : ('SubTree(ctl,mode,(24,25,26,27))','热门播放悦单','/pl/playlist_hotView'),
            24   : ('get_playlistpage(url,ctl[mode][1],mode)','24小时热门播放悦单','/pl/playlist_hotView/today'),
            25   : ('get_playlistpage(url,ctl[mode][1],mode)','本周热门播放悦单','/pl/playlist_hotView/week'),
            26   : ('get_playlistpage(url,ctl[mode][1],mode)','本月热门播放悦单','/pl/playlist_hotView/month'),
            27   : ('get_playlistpage(url,ctl[mode][1],mode)','全部热门播放悦单','/pl/playlist_hotView/all'),
            
            31   : ('get_playlistpage(url,ctl[mode][1],mode)','最新推荐悦单','/pl/playlist_newRecommend'),
            32   : ('get_playlistpage(url,ctl[mode][1],mode)','最新收藏悦单','/pl/playlist_newFavorite'),
            33   : ('get_playlistpage(url,ctl[mode][1],mode)','最新评论悦单','/pl/playlist_newComment'),
            34   : ('get_playlistpage(url,ctl[mode][1],mode)','最新创建悦单','/pl/playlist_newCreate'),
            
            40   : ('get_artistpage(url,ctl[mode][1],mode,257)','全部歌手','/fanAll'),
            41   : ('get_artistpage(url,ctl[mode][1],mode,257)','港台男歌手','/fanAll?area=HT&property=Boy'),
            42   : ('get_artistpage(url,ctl[mode][1],mode,257)','港台女歌手','/fanAll?area=HT&property=Girl'),
            43   : ('get_artistpage(url,ctl[mode][1],mode,257)','港台乐队/组合','/fanAll?area=HT&property=Combo'),
            44   : ('get_artistpage(url,ctl[mode][1],mode,257)','内地男歌手','/fanAll?area=ML&property=Boy'),
            45   : ('get_artistpage(url,ctl[mode][1],mode,257)','内地女歌手','/fanAll?area=ML&property=Girl'),
            46   : ('get_artistpage(url,ctl[mode][1],mode,257)','内地乐队/组合','/fanAll?area=ML&property=Combo'),
            47   : ('get_artistpage(url,ctl[mode][1],mode,257)','欧美男歌手','/fanAll?area=US&property=Boy'),
            48   : ('get_artistpage(url,ctl[mode][1],mode,257)','欧美女歌手','/fanAll?area=US&property=Girl'),
            49   : ('get_artistpage(url,ctl[mode][1],mode,257)','欧美乐队/组合','/fanAll?area=US&property=Combo'),                   
            50   : ('get_artistpage(url,ctl[mode][1],mode,257)','韩语男歌手','/fanAll?area=KR&property=Boy'),
            51   : ('get_artistpage(url,ctl[mode][1],mode,257)','韩语女歌手','/fanAll?area=KR&property=Girl'),
            52   : ('get_artistpage(url,ctl[mode][1],mode,257)','韩语乐队/组合','/fanAll?area=KR&property=Combo'),
            53   : ('get_artistpage(url,ctl[mode][1],mode,257)','日语男歌手','/fanAll?area=JP&property=Boy'),
            54   : ('get_artistpage(url,ctl[mode][1],mode,257)','日语女歌手','/fanAll?area=JP&property=Girl'),
            55   : ('get_artistpage(url,ctl[mode][1],mode,257)','日语乐队/组合','/fanAll?area=JP&property=Combo'),
            
            61   : ('ListRecommendMV(url,name,mode)','全部推荐MV','/lookVideo-area/MV'),
            62   : ('ListRecommendMV(url,name,mode)','港台推荐MV','/lookVideo-area/HT'),
            63   : ('ListRecommendMV(url,name,mode)','内地推荐MV','/lookVideo-area/ML'),
            64   : ('ListRecommendMV(url,name,mode)','欧美推荐MV','/lookVideo-area/US'),
            65   : ('ListRecommendMV(url,name,mode)','韩语推荐MV','/lookVideo-area/KR'),           
            66   : ('ListRecommendMV(url,name,mode)','日语推荐MV','/lookVideo-area/JP'),           
            
            80   : ('ShowFocusMV(url,name,mode)','MV周榜','/index/MV'),
            81   : ('ShowFocusMV(url,name,mode)','港台周榜','/index-ht'),
            82   : ('ShowFocusMV(url,name,mode)','内地周榜','/index-ml'),
            83   : ('ShowFocusMV(url,name,mode)','欧美周榜','/index-us'),
            84   : ('ShowFocusMV(url,name,mode)','韩国周榜','/index-kr'),
            85   : ('ShowFocusMV(url,name,mode)','日本周榜','/index-jp'),
            
            90   : ('SubTree(ctl,mode,(61,62,63,64,65,66))','推荐MV','/lookVideo'),
            91   : ('AllMV(url,name,mode)','全部MV','/lookAllVideo'),
            92   : ('SubTree(ctl,mode,(31,32,33,34))','最新悦单','/pl/playlist_new'),
            93   : ('SubTree(ctl,mode,(8,13,18,23))','热门悦单','/pl/playlist_hot'),
            94   : ('get_playlistpage(url,ctl[mode][1],mode)','编辑推荐悦单','/pl/playlist_promo'),
            95   : ('get_playlistpage(url,ctl[mode][1],mode)','全部悦单','/pl/playlist_all'),
            96   : ('SubTree(ctl,mode,(40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55))','歌手','/fanAll'),
            
            256  : ('ShowPlayList(url,name,mode)','显示悦单'),
            257  : ('ShowArtistMV(url,name,mode)','显示歌手MV'),
      }
exec(ctl[mode][0])
#xbmcplugin.setPluginCategory(int(sys.argv[1]), ctl[mode][1])
xbmcplugin.endOfDirectory(int(sys.argv[1]))
