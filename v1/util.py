# -*- coding: utf-8 -*-
import io, re, string, sys, os
import urllib2
from xml.dom import minidom

# qq_default.py "plugin://plugin.video.tencent/" "0"

''' Most of the methods are invoked by clutter '''
class Media(object):
	def __init__(self, label='', label2='', iconImage='', thumbnailImage='', path=''):
		#object.__init__(self)
		self.infos={'Score':'', 'Director':'', 'Actors':'', 'Area':'', 'Type':'', 'Year':'', 'Duration':'', 'Introduction':''}
		self.playlist = None
		self.URLs = []

	def setMediaInfo(self, name, value):
		self.infos[name] = value

	def setPlayList(self, l):
		self.playlist = l
		self.URLs = l.getURLs()

	def getMediaInfos(self):
		return self.infos
	
	def isMenu(self):
		return False
	
	def getURLs(self):
		return self.URLs

	# For Test
	def printMediaInfo(self):
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
		if func[3:] not in self.infos or func.find('get') != 0:
			raise NotImplementedError, '%s not implements' % (func)
		else:
			return lambda : self.infos[func[3:]]

class MenuItem(object):
	def __init__(self, label='', label2='', iconImage='', thumbnailImage='', path=''):
		self.label = label
		self.label2 = label2
		self.iconImage = iconImage
		self.thumbnailImage = thumbnailImage
		self.path = path
		self.media = None

	def __getattr__(self, func):
		if self.media is not None:
			return getattr(self.media, func)
		raise Exception, 'self.media is None'
	
	def setInfo(self, type, infoLabels):
		pass
	
	def bindMedia(self, media=None):
		self.media = media	

	def getName(self):
		return self.label	

	def getPictureURL(self):
		return self.thumbnailImage

	def getPictureName(self):
		return self.thumbnailImage.split('/')[-1]

class Categorization(object):
	def __init__(self):
		object.__init__(self)
		self.cate_table = {}
		''' cate_table struct seems like this
		{
			'年代':{'1999':'_1999','2000':'_2000'},
		   	'类型':{'动作':'_action','爱情':'_love','恐怖':'_horribel'},
			'地区':{'大陆':'_mainland','台湾':'_Taiwan','香港':'_Hongkong'}
		}
		'''

	def addCategorization(self, cate_name, cate_map = {}):
		self.cate_table[cate_name] = cate_map

	def updateCategorization(self, cate_name, cate_map):
		self.addCategorization(cate_name, cate_map)

	def getCate(self, cate_name):
		if cate_name in self.cate_table:
			return self.cate_table[cate_name]
		raise IndexError, '%s not exists in cate table' %(cate_name)

	def getCateSize(self):
		return len(self.cate_table)

	def getGivenCateSize(self, cate_name):
		if cate_name in self.cate_table:
			return len(self.cate_table[cate_name])
		raise IndexError, '%s not exists in cate table' %(cate_name)

	''' For Test '''
	def printTable(self):
		for k,v in self.cate_table.iteritems():
			print k + '===>\t'
			for i,j in v.iteritems():
				print '\t\t' + i + '--->' + j

''' Most of the methods are invoked by clutter '''
class Menu(object):
	def __init__(self):
		self.params = []
		self.items = []
		self.page_items = {}
		self.cate_code = None

	def __getitem__(self, index):
		if index < len(self.items):
			return self.items[index]
		raise IndexError, "Index %d does not exists " % (index)

	def isMenu(self):
		return True

	''' For Categorization '''
	def hasCategorization(self):
		return self.cate_code is not None

	def setCateCode(self, code):
		self.cate_code = code

	def enableCategorization(self):
		return cate_code
	''' End Categorization '''

	def getMenuNames(self):
		return [ x.getName() for x in self.items ]

	def getMenuSize(self):
		return len(self.items)

	def addDirectoryItem(self, handle, url, listitem, isFolder=True, totalItems=0):
		self.items.append(listitem)	
		self.params.append(url)

	def addPageItem(self, params, item):
		self.page_items[item.getName()] = params

	def getItems(self):
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
			print self.items[i].getName() + ' <=> ' + name
			if self.items[i].getName() == name:
				return self.params[i]
		raise IndexError, "Item %s does not exists" % (name)

	''' For Test '''
	def endOfDirectory(self, handle, succeeded=True, updateListing=True, cacheToDisc=True):
		for i in range(len(self.items)):
			print '[%2d] %s' %(i+1, self.items[i].getName())
		f = io.open('/dev/stdin', 'r')
		print 'Select item: '
		getin = f.readline()	
		if getin.strip() == 'q':
			exit(0)
		elif getin.strip() == 's':
			return self.cate_code			
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
		dom = minidom.parse(self.cfg_path)
		root = dom.documentElement
		for i in root.getElementsByTagName('setting'): 
			if i.getAttribute('id') == id:
				return i.getAttribute('default').encode('utf8')

	def setSetting(self, id, value):
		dom = minidom.parse(self.cfg_path)
		root = dom.documentElement
		for i in root.getElementsByTagName('settings'):
			if i.getAttribute('id') == id:
				i.setAttribute('default', value)

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
