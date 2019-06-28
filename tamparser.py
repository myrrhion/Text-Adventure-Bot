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

@_getter()
def iteminroom(self, value):
	return value in self.get_room().items

@_getter()
def hasitem(self, value):
	return value in self.inv


@_getter(acname="gflag")
def gflag(self,value):
	return value in self.pflags

@_setter(acname="gotoroom")
def gotoroom(self,value):
	self.cur_room = value
@_setter()
def quitgame(self,value):
	self.game.end()
@_setter()
def setpflag(self,value):
	self.pflags.add(value)

@_setter()
def pickup(self,value):
	self.inv.add(value)
	self.get_room().items.discard(value)
	
@_setter()
def addtoinv(self,value):
	self.inv.add(value)

@_setter()
def removefrominv(self,value):
	self.inv.discard(value)

@_setter()
def drop(self,value):
	self.inv.discard(value)
	self.get_room().items.add(value)
	
@_setter()
def addtoroom(self,value):
	self.get_room().add(value)

@_setter()
def removefromroom(self,value):
	self.get_room().items.discard(value)


@_setter()
def delpflag(self,value):
	self.pflags.discard(value)

@_setter()
def setgflag(self,value):
	self.game._flags.add(value)

@_setter()
def delgflag(self,value):
	self.game._flags.discard(value)

def getter(self,key,value):
	return Glob.getter[key](self,value)

def setter(self,key,value):
	return Glob.setter[key](self,value)
