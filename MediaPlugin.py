# -*- coding: utf-8 -*-

__applicationName__ = "MediaPlugin"
__doc__="""
MediaPluginController 界面对各个插件数据获取请求由此处理并返回
"""
import dbus, dbus.service, gobject
from dbus.mainloop.glib import DBusGMainLoop
import cPickle
import util

class MediaPluginController(object):
	def __init__(self):
		self.plugins = ['pptv', 'youkutv', 'sohutv', 'qqtv']
		self.plugin_state = None
	
	def update(self, observed):
		"""
		msg == {'command':'setPlugin', params:'qqtv'} or 
			   {'command':'delPlugin', params:'qqtv'} or
			   {'command':'SelectItem', params:'电影'} or
			   {'command':'getRootMenu'} or
		"""
		msg = cPickle.loads(observed.data)
		if msg['command'] == 'setPlugin':
			try:
				observed.include = __import__(msg['params'], fromlist=["*"])
			except Exception, e:
				print e
				raise e
		elif msg['command'] == 'SelectItem':
			try:
				# FIXME: exception process
				self.plugin_state = observed.include.decode( self.plugin_state.selectItem(msg['params']) )
			except Exception, e:
				pass
			observed.tnMessmageSend( 'testdbus', 0, cPickle.dumps(self.plugin_state) )
		elif msg['command'] == 'getRootMenu':
			try:
				print 'getRootMenu'
				self.plugin_state = observed.include.getRootMenu()
			except Exception, e:
				pass	
			print 'Begin send'
			observed.tnMessmageSend( 'testdbus', 0, cPickle.dumps(self.plugin_state) )
			print 'after send'
		elif msg['command'] == 'delPlugin':
			del msg['params']

class MediaPluginDBus(dbus.service.Object):
	"""
	Media Plugin Dbus通信处理类
	"""
	
	def __init__(self, bus_name, session):
		dbus.service.Object.__init__(self, object_path='/com/routon', bus_name=bus_name)
		self.bus_name = bus_name
		self.session = session
		self.my_module_name = 'MediaPlugin'
		self.from_module_name = None
		self.data = None
		self.code = None
		self.observer = None

	def get_proxy(self, module):
		module_name = "com.routon."+module
		if module_name in self.my_proxy:
			return self.my_proxy[module_name]
		path = self.my_bus.get_object(module_name, '/com/routon', follow_name_owner_changes=True)
		interface = dbus.Interface(path, dbus_interface='com.routon')
		self.my_proxy[module_name] = interface
		return interface

	@dbus.service.method(dbus_interface='com.routon', in_signature='suay', out_signature='i', byte_arrays=True, utf8_strings=True)
	def tnMessage(self, module, code, data):
		"""
		回调方法, 默认的方法名
		"""
		self.from_module_name = module
		self.code = code
		self.data = data
		# 消息接收完毕，通知controller 开始处理数据	
		print '消息接收完毕，通知controller 开始处理数据'
		self.notify()

	def notify(self,):
		self.observer.update(self)

	def attach(self,observer):
		self.observer = observer

	def tnMessmageSend(self, module, code, data):
		"""
		消息发送
		@param module: 消息接收模块名 (testdbus)
		@param data  : 消息体
		"""
		try:
			proxy = self.get_proxy(module)	
			return proxy.TnMessage(self.my_module_name, code, dbus.ByteArray(data),
					reply_handler=handle_dbus_reply, error_handler=handle_dbus_error)
		except dbus.exceptions.DBusException, e:
			print e
			raise e

if __name__ == '__main__':
	""" Init MediaPluginDBus and Controller"""
	DBusGMainLoop(set_as_default=True)
	session = dbus.SessionBus()
	bus_name = dbus.service.BusName('com.routon.' + 'MediaPlugin', bus = session)
	mpc_bus = MediaPluginDBus(bus_name, session)	
	mpc = MediaPluginController()
	mpc_bus.attach(mpc)
	""" Dbus MainLoop """	
	mainloop = gobject.MainLoop()	
	print 'MediaPluginDBus mainloop begin'
	""" loop end """
	mainloop.run()
