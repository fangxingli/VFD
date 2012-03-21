#!/usr/bin/env python
# -*- coding: utf-8 -*-

__applicationName__ = 'util'
__doc__ = """
util 是一个介于H3显示模块和数据处理模块中间的框架模块，
用来标准化显示模块和数据处理模块交互接口，方便抽象数据
类型，两个模块都需要import util
"""

import io, re, os
import urllib2
from xml.dom import minidom
class Media(object):
	"""
	视频类，处理于视频信息相关信息，包括导演，演员，视频播放地址等
	
	一般由数据获取方创建并填充数据，由视频显示方从中取得所需数据
	"""

	"""
	@var infos holds the infomations of the media, ie. Score, Director, Actors, Area ...
	@var playlist holds the PlayList object witch standing by Playing address(es)
	@var URLs holds the Playing urls which actually belong PlayList object
	"""
	def __init__(self, label='', label2='', iconImage='', thumbnailImage='', path=''):
		#object.__init__(self)
		self.infos={'Score':'', 'Director':'', 'Actors':'', 'Area':'', 'Type':'', 'Year':'', 'Duration':'', 'Introduction':''}
		self.playlist = None
		self.URLs = []

	def setMediaInfo(self, name='', value=''):
		"""
		x.setMediaInfo('Director', 'Steven, King') -> None

		修改或增加视频信息
		"""
		self.infos[name] = value

	def setPlayList(self, l):
		"""
		x.setPlayList(playlist) -> None

		设置于视频相关的播放列表对象
		"""
		self.playlist = l
		self.URLs = l.getURLs()

	def getMediaInfos(self):
		"""
		x.getMediaInfos() -> dict

		返回视频信息字典
		"""
		return self.infos
	
	def isMenu(self):
		"""
		x.isMenu() -> bool

		是否为Menu对象，类似于isinstance(x, Menu)
		"""
		return False
	
	def getURLs(self):
		"""
		x.getURLs() -> list

		返回播放地址数组
		"""
		return self.URLs

	# For Test
	def printMediaInfo(self):
		""" DBG """
		print '---------------------Begin print Media infomation ----------------------'
		for k,v in self.infos.iteritems():
			if isinstance(v, list):
				print k + '<=======>',
				for i in v:
					print i,
				print ''
			else:
				print k + '<=======>' + str(v)

	def __getattr__(self, func):
		"""
		x.__getattr__('Actors') <==> x.getActors() 
		"""
		if func[3:] not in self.infos or func.find('get') != 0:
			raise NotImplementedError, '%s not implements' % (func)
		else:
			return lambda : self.infos[func[3:]]

class MenuItem(object):
	"""
	目录项类，表示树形控件或者平铺控件中的一个可选择对象
	包括和处理与此对象相关信息	
	"""

	"""
	@var label holds the major title
	@var label2 holds the minor title(useless)
	@var iconImage holds the iconImage URL(useless)
	@var thumbnailImage hold the thumbnailImage URL
	@var path useless
	"""
	def __init__(self, label='', label2='', iconImage='', thumbnailImage='', path=''):
		self.label = label
		self.label2 = label2
		self.iconImage = iconImage
		self.thumbnailImage = thumbnailImage
		self.path = path
		self.media = None

	def __getattr__(self, func):
		"""
		x.__getattr__('getActors') <==> x.getActors() <==> x.media.getActors()
		
		raise Exception if self.media is None
		"""
		if self.media is not None:
			return getattr(self.media, func)
		raise Exception, 'self.media is None'
	
	def setInfo(self, type, infoLabels):
		""" Uesless """
		pass
	
	def bindMedia(self, media=None):
		"""
		x.bindMedia(media) -> None
	
		使用此方法绑定具体影片，之后可将本对象当作Media对象来获取影片信息
		"""
		self.media = media	

	def getName(self):
		"""
		x.getName() -> string
		
		返回item title, 如果绑定了Media对象，则是影片名
		"""
		return self.label	

	def getPictureURL(self):
		"""
		x.getPictureURL() -> string

		返回与此项项关的展示图片(海报)的网络地址
		"""
		return self.thumbnailImage

	def getPictureName(self):
		"""
		x.getPictureName() -> string
		
		返回展示图片(海报)文件名
		"""
		return self.thumbnailImage.split('/')[-1]

class Categorization(object):
	"""
	筛选分类类，对于某一个大类----比如'电影'----进行
	筛选，比如类型为‘动作'，地区为'大陆'，上映年代为'2011'

	这些信息存放的数据结构类似于
		{
			('年代','year'):{'1999':'_1999','2000':'_2000'},
		   	('类型','cat'):{'动作':'_action','爱情':'_love','恐怖':'_horribel'},
			('地区','area'):{'大陆':'_mainland','台湾':'_Taiwan','香港':'_Hongkong'}
		}
	以第二行为例：('类型','cat'):{'动作':'_action','爱情':'_love','恐怖':'_horribel'}
		前面的tuple中的元素0是用来显示在屏幕的，后面接的'cat'为一个key，之后的dict每一项
		的key为'类型'下面的子选项，当选中'动作'后，将'_action'作为value,与之前的'cat'组成
		dict中的一项{'cat':'_action'}
	"""
	def __init__(self):
		object.__init__(self)
		self.cate_table = {}
		self.cate_code = None

	def __iter__(self):
		"""
		for i in cate:
			i ==  ('年代','year')
			cate[i] == {'1999':'_1999','2000':'_2000'}
			...

		可以这样迭代此对象 for i in cate:
		"""
		return iter(self.cate_table)

	''' Methods below are used by tv '''
	def addCategorization(self, cate_name, cate_name_key, cate_map = {}):
		"""
		x.addCategorization(cate_name, cate_name_key, cate_map) -> None
		@param cate_name 	 : string - 筛选类型名，如'类型'
		@param cate_name_key : string - 类型键值，如'year'
		@param cate_map 	 : dict(optional) - 筛选类型下的子选项字典,可选
		"""
		if len(cate_map) != 0:
			self.cate_table[(cate_name, cate_name_key)] = cate_map

	def getCate(self, cate_name_or_key):
		"""
		x.getCate('类型') -> dict  or  x.getCate('cat') -> dict
	
		返回筛选类型名对应的dict
		"""
		for i in self.cate_table.keys():
			if cate_name_or_key in i:
				return self.cate_table[i]
		raise IndexError, '%s not exists in cate table' %(cate_name_or_key)

	def getCateSize(self):
		"""
		x.getCateSize() -> int

		返回筛选类型种类数目
		"""
		return len(self.cate_table)

	def getGivenCateSize(self, cate_name_or_key):
		"""
		x.getGivenCateSize('类型') -> int

		返回特定筛选类型子选项长度
		"""
		for i in self.cate_table:
			if cate_name_or_key in i:
				return len(self.cate_table[i])
		raise IndexError, '%s not exists in cate table' %(cate_name_or_key )

	''' Set init code for categorising '''
	def setCateCode(self, **args):
		self.cate_code = args
            
	def updateCateCode(self, update_code):
		self.cate_code.update(update_cate)
		return self.cate_code

	''' For Test '''
	def printTable(self):
		""" GDB """
		for k,v in self.cate_table.iteritems():
			print k[0] +'('+ k[1] + ')' + '===>\t'
			for i,j in v.iteritems():
				print '\t\t' + i + '--->' + j

''' Most of the methods are invoked by clutter '''
class Menu(object):
	"""
	目录列表类，作为包含MenuItem ,Categorization的容器
	"""
	def __init__(self):
		self.params = []
		self.items = []
		self.page_items = {}
		self.cate = None

	def __getitem__(self, index):
		"""
		x.__getitem__(i) <==> x[i]

		使用下标i迭代所包含的MenuItem对象
		"""
		if index < len(self.items):
			return self.items[index]
		raise IndexError, "Index %d does not exists " % (index)

	def isMenu(self):
		"""
		x.isMenu() -> bool

		是否为Menu对象，类似于isinstance(x, Menu)
		"""
		return True

	''' For Categorization '''
	def getCategorization(self):
		"""
		x.getCategorization() -> Categorization对象

		如果不为None, 则返回筛选分类类
		"""
		return self.cate

	def enableCategorization(self, cate):
		"""
		x.enableCategorization( Categorization对象 ) -> None

		如果有筛选分类, 设置完筛选相关信息后，用来开启筛选分类
		"""
		self.cate = cate
	''' End Categorization '''

	def getMenuNames(self):
		"""
		x.getMenuNames() -> list
		
		返回所有MenuItem title 列表
		"""
		return [ x.getName() for x in self.items ]

	def getMenuSize(self):
		"""
		x.getMenuSize() -> int

		返回MenuItem数目
		"""
		return len(self.items)

	def addDirectoryItem(self, handle, url, listitem, isFolder=True, totalItems=0):
		"""
		Fix me 向XBMC兼容性
		x.addDirectoryItem(...) -> None
		"""
		self.items.append(listitem)	
		self.params.append(url)

	def addPageItem(self, page_code, item):
		"""
		x.addPageItem(page_code, MenuItem对象) -> None

		如果有上一页或者下一页
		"""
		self.page_items[item.getName()] = page_code

	def getPageItems(self):
		"""
		x.getPageItems() -> dict
		
		返回分页信息字典
		"""
		return self.page_items

	def getItems(self):
		"""
		x.getItems() -> list
		
		返回所有MenuItems对象
		"""
		return self.items

	''' Invoke by clutter  '''
	def selectItem(self, name='', index = -1):
		if index in range(len(self.params)):
			return self.params[index]
		''' Loop the page items '''
		if name in self.page_items:
			return self.page_items[name]
		''' Loop the directory items '''
		for i in range(len(self.items)):
			print self.items[i].getName() + ' <=> ' + str(name)
			if self.items[i].getName() == name:
				return self.params[i]
		raise IndexError, "Item %s does not exists" % str(name)

	''' For Test '''
	def endOfDirectory(self, handle, succeeded=True, updateListing=True, cacheToDisc=True):
		""" GDB """
		for i in range(len(self.items)):
			print '[%2d] %s' %(i+1, self.items[i].getName())
		f = io.open('/dev/stdin', 'r')
		print 'Select item: '
		getin = f.readline()	
		if getin.strip() == 'q':
			exit(0)
		elif getin.strip() == 'n':
			return self.selectItem('下一页')
		elif getin.strip() == 'p':
			return self.selectItem('上一页')
		elif getin.strip() == 's':
			return self.enableCategorization()
		else:
			getin = int(getin) - 1
		print getin
		f.close()
		for i in range(self.getMenuSize()):
			print '[%d] %s' % (i+1, self.items[i].getName())
			print self.params[i]
			print '%s' % (self.items[i].getPictureURL())
			print '**********************************'
		return self.selectItem(self.items[getin].getName())

	def setContent(self, handle, content):
		pass	

class Addon(object):
	def __init__(self, id):
		self.__id = id
		self.cfg_path = os.path.join(os.getcwd() + '/' + self.__id + '/resources/settings.xml')

	def getAddonInfo(self, id):
		return self.__id	

	def getSetting(self,id):
		f = open(self.cfg_path, 'r')
		dom = minidom.parse(self.cfg_path)
		root = dom.documentElement
		for i in root.getElementsByTagName('setting'): 
			if i.getAttribute('id') == id:
				return i.getAttribute('default').encode('utf8')
		f.close()

	def setSetting(self, id, value):
		f = open(self.cfg_path, 'rwb')
		dom = minidom.parse(f)
		root = dom.documentElement
		for i in root.getElementsByTagName('setting'):
			if i.getAttribute('id') == id:
				i.setAttribute('default', value.decode('utf8'))
		open(self.cfg_path,'w').write(dom.toxml().encode('utf8'))
		f.close()

# For Test
class Player(object):
	''' The play URL is here, which can be played in mplayer'''
	__current_play_url=''
	def __init__(self):
		pass
	
	def play(self, item='', listitem=None, windowed=True):
		if isinstance(item, str):
			if listitem is not None:
				os.system('mplayer "%s"' %(listitem.getURL()))
			else:
				os.system('mplayer "%s"' %(item))
		else:	
			os.system('mplayer "%s"' %(item.getURLs()[0]))


class PlayList(object):
	def __init__(self, playlist):
		self.urls=[]
		self.listitems=[]

	def __str__(self):
		return self.urls	
	
	def getURLs(self):
		return self.urls

	def clear(self):
		pass
		
	def add(self, url, listitem=None, index=1):
		self.urls.append(url)
		self.listitems.append(listitem)
	
class Dialog(object):
	dialog_list=[]
	heading=''
	def __init__(self):
		pass
	
	def select(self, heading, list):
		self.heading = heading	
		print '======> '+ heading + ' <======\n'
		for i in range(len(list)):
			print '[' + str(i+1) + '] ' + list[i]
		f = io.open('/dev/stdin','r')
		print 'Select item: '
		getin = f.readline().strip()
		if getin == 'q':
			exit(0)
		getin = int(getin) - 1	
		f.close()
		if getin >= len(list):
			return -1
		else:
			return getin
		
def translatePath(path):
	pass	

def GetHttpData(url, UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'):
    print '------------------------------> ' + url 
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
            httpdata = httpdata.decode(charset, 'ignore').encode('utf8', 'ignore')
    return httpdata
