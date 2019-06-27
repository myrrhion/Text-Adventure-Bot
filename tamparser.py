class Glob:
	getter = {}
	setter = {}

def _getter(acname=None):
	def wrap(func):
		name = acname if acname else func.__name__
		Glob.getter[name] = func
		return func
	return wrap

def _setter(acname=None):
	def wrap(func):
		name = acname if acname else func.__name__
		Glob.setter[name] = func
		return func
	return wrap



@_getter(acname="pflag")
def pflag(self, value):
	return value in self.pflags

@_getter(acname="gflag")
def gflag(self,value):
	return value in self.pflags

@_setter(acname="gotoroom")
def gotoroom(self,value):
	self._visited.add(self.cur_room)
	self.cur_room = value

def getter(self,key,value):
	return Glob.getter[key](self,value)

def setter(self,key,value):
	return Glob.setter[key](self,value)
