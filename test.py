class TestFrame(object):
	def __init__(self):
		self.m = ['lifangxing', 'chenjiawo', 'adfa','asdf','1','2','3']

	def save(self, **args):
		self.m = args
 
t = TestFrame()
t.save(mode=4, name='name', id='id', cat='cat')
for i in t.m:
	print i,t.m[i]
print t.m
#TestFrame().iteritems()
