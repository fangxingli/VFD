#!/usr/bin/env python
# -*- coding: utf-8 -*-

__applicationName__ = "MediaPlugin"
__doc__="""
MediaPlugin 负责接收界面Dbus请求，根据请求调用各插件模块，处理后发送Dbus
消息给界面，
"""
import dbus, dbus.service, gobject
from dbus.mainloop.glib import DBusGMainLoop
import cPickle
import util

class MediaPluginController(object):
	"""
	MediaPluginController 根据获得的消息体解析后，调用具体插件模块执行后返回
	返回的对象以消息体模式发送到界面进程
	"""
	def __init__(self):
		self.plugins_allowed = ['pptv', 'youkutv', 'sohutv', 'qqtv']
		self.plugin_state = None
		self.include = None
	
	def update(self, observed):
		"""
		
		msg_recv == {'command':'setPlugin', 'params':'qqtv', 'type':'Tree'} or 
			   		{'command':'SelectItem', 'params':'电影', 'type':'Tree', 'pluginObject':obj} or
			   		{'command':'getRootMenu', 'type':'Tree'} or
			   		{'command':'stop'} or

		msg_send == {'pluginObject':obj, 'type':'Tree'}
		"""
		msg_recv = cPickle.loads(observed.data)
		print '消息体: %s' % str(msg_recv)
		if msg_recv['command'] == 'setPlugin':
			try:
				if msg_recv['params'] not in self.plugins_allowed:
					raise KeyError, '%s plugin invalid yet' % msg_recv['params']
				self.include = __import__(msg_recv['params'], fromlist=["*"])
			except Exception, e:
				print e
		elif msg_recv['command'] == 'SelectItem':
			try:
				# FIXME: exception process
				self.plugin_state = self.include.decode( self.plugin_state.selectItem(msg_recv['params']) )
				print '>>>>>>>开始发消息 SelectItem'
				msg_send = { 'pluginObject':self.plugin_state, 'type':msg_recv['type'] }		
				observed.tnMessmageSend( observed.from_module_name, 0, cPickle.dumps(msg_send) )
				print '<<<<<<<结束发消息 SelectItem'
			except Exception, e:
				print e
		elif msg_recv['command'] == 'getRootMenu':
			print 'Begin getRootMenu'
			try:
				self.plugin_state = self.include.getRootMenu()
				print '>>>>>>>开始发消息 getRootMenu'
				msg_send = { 'pluginObject':self.plugin_state, 'type':msg_recv['type'] }		
				observed.tnMessmageSend( observed.from_module_name, 0, cPickle.dumps(msg_send) )
				print '>>>>>>>结束发消息 getRootMenu'
			except Exception, e:
				print e
			print 'After getRootMenu'
		elif msg_recv['command'] == 'stop':
			exit(0)
		print '更新结束'

class MediaPluginDBus(dbus.service.Object):
	"""
	Media Plugin Dbus通信处理类
	这里的消息传输使用的是类似IPC模式
	"""
	
	def __init__(self, bus_name, session):
		dbus.service.Object.__init__(self, bus_name, '/com/routon')
		self.bus_name = bus_name
		self.session = session
		self.my_module_name = 'MediaPlugin'
		self.from_module_name = None
		self.data = None
		self.code = None
		self.observer = None
		self.my_proxy = {}

	def get_proxy(self, module):
		module_name = "com.routon."+module
		if module_name in self.my_proxy:
			return self.my_proxy[module_name]
		path = self.session.get_object(module_name, '/com/routon', follow_name_owner_changes=True)
		interface = dbus.Interface(path, dbus_interface='com.routon')
		self.my_proxy[module_name] = interface
		return interface

	@dbus.service.method(dbus_interface='com.routon', in_signature='suay', out_signature='i', byte_arrays=True, utf8_strings=True)
	def TnMessage(self, module, code, data):
		"""
		回调方法, 默认的方法名
		"""
		self.from_module_name = module
		self.code = code
		self.data = data
		# 消息接收完毕，通知controller 开始处理数据	
		print '消息接收完毕，通知controller 开始处理数据'
		self.notify()
		return 0

	def notify(self):
		"""
		消息接收后，通知控制器更新状态
		"""
		self.observer.update(self)

	def attach(self, observer):
		"""
		绑定控制器	
		"""
		self.observer = observer

	def tnMessmageSend(self, module, code, data):
		"""
		消息发送
		@param module: 消息接收模块名 (testdbus)
		@param code  : Useless
		@param data  : 消息体
		"""
		def handle_dbus_reply(x):
			pass
		def handle_dbus_error(x):
			pass
		try:
			proxy = self.get_proxy(module)	
			return proxy.TnMessage(self.my_module_name, code, dbus.ByteArray(data),
					reply_handler=handle_dbus_reply, error_handler=handle_dbus_error)
		except dbus.exceptions.DBusException, e:
			print e

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
