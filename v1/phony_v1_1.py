import io, re, string, sys, os
import urllib2
import threading

# qq_default.py "plugin://plugin.video.tencent/" "0"

IMG_PATH = '/workspace/python-movie/src/imgs'

#class ImageCache(threading.Thread):
class ImageCache:
	path=''
	urls=[]
	def __init__(self, path='/hdisk/backup/cache/Images', imgs=[]):
		#threading.Thread.__init__(self)
		ImageCache.path = path
		self.checkPathValid()
		self.imgs = imgs

	def start(self):
		self.run()

	def run(self):
		self.dislocalize()
		self.localize()

	def checkPathValid(self):
		if not os.path.exists(self.getPath()):
			raise IOError, '    Path %s does not exists' % (self.getPath())

	def localize(self):
		self.checkPathValid()
		print 'The length of imgs is ' + str(len(self.imgs))
		for i in self.imgs:
			try:
				if i != '':
					print i + '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
					req = urllib2.Request(i)
					response = urllib2.urlopen(req)
					data = response.read()
					ImageCache.urls.append(self.getPath()+i[i.rfind('/'):])
	#				print ImageCache.urls[-1]
					f = io.open(ImageCache.urls[-1], 'wb')
					f.write(data)
					f.close()
				else:
					print i+ '------------------------------'
			except:
				continue

	def dislocalize(self):
		self.checkPathValid()
		for i in ImageCache.urls:
			if i != '':
				try:
					os.remove(i)
				except:
					pass
		ImageCache.urls=[]

	def getPath(self):
		return ImageCache.path

	def setPath(self, path):
		ImageCache.path = path

class ListItem:
	def __init__(self, label='', label2='', iconImage='', thumbnailImage='', path=''):
		self.label = label
		self.label2 = label2
		self.iconImage = iconImage
		self.thumbnailImage = thumbnailImage
		self.path = path
	def setInfo(self, type, infoLabels):
		pass
	def getURLImage(self):
		return self.iconImage
	def getLocalImage(self):
		return ImageCache.path + self.iconImage[self.iconImage.rfind('/'):]
	def getLabel(self):
		return self.label
	def __str__(self):
		return self.label

class LevelTree:
	def __init__(self):
		self.links=[]
		self.seqs=[]
		self.seq=0
		self.items = []

	def __getitem__(self, index):
		if index < self.seq:
			return self.items[index]
		raise IndexError, "Index %d does not exsits" % (index)

	def __len__(self):
		return self.seq

	def addDirectoryItem(self, handle, url, listitem, isFolder=True, totalItems=0):
		self.items.append(listitem)	
		self.links.append(url)
		self.seq += 1
		self.seqs.append(self.seq)
	
	def getItems(self):
		return self.items

	def selectItem(self, name=''):
		for i in range(len(self.items)):
			print self.items[i].getLabel() + ' <=> ' + name
			if self.items[i].getLabel() == name:
				return self.links[i].split('?')[0] , ' 0 ', self.links[i].split('?')[1]

		raise IndexError, "Item %s does not exsits" % (name)

	''' For Test '''
	def endOfDirectory(self, handle, succeeded=True, updateListing=True, cacheToDisc=True):
		for i in range(len(self.items)):
			print '[%2d] %s' %(self.seqs[i], self.items[i])
		f = io.open('/dev/stdin', 'r')
		print 'Select item: '
		getin = int(f.readline()) - 1	
		print getin
		f.close()
		for i in range(self.seq):
			print '[%d] %s' % (i+1, self.items[i])
			print self.links[i]
			print '**********************************'
		#print 'python %s "%s" "%s" "%s"' %(sys.path[0]+'/pptv_default.py', links[getin].split('?')[0] ,' 0 ' ,links[getin].split('?')[1])
		#os.system('python %s "%s" "%s" "%s"' %(sys.path[0]+'/pptv_default.py', links[getin].split('?')[0] ,' 0 ' ,links[getin].split('?')[1]))
		return self.selectItem(self.items[getin].getLabel())
		#return self.links[getin].split('?')[0] , ' 0 ', self.links[getin].split('?')[1]

	def setContent(self, handle, content):
		pass	

class Addon:
	__id=''
	def __init__(self, id):
		self.__id = id

	def getAddonInfo(self, id):
		return self.__id	

	def getSetting(self,id):
		return 1

class Player:
	''' The play URL is here, which can be played in mplayer'''
	__current_play_url=''
	def __init__(self):
		pass
	
	def play(self, item='', listitem=None, windowed=True):
		self.__current_play_url = str(item)
		os.system('mplayer "%s"' %(self.__current_play_url))


class PlayList:
	__url=''
	__listitem=None
	def __init__(self, playlist):
		pass

	def __str__(self):
		return self.__url	
	
	def clear(self):
		pass
		
	def add(self, url, listitem=None, index=1):
		self.__url = url
		self.__listitem = listitem
class Dialog:
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
		getin = int(f.readline()) - 1
		f.close()
		if getin >= len(list):
			return -1
		else:
			return getin
		
def translatePath(path):
	pass	
