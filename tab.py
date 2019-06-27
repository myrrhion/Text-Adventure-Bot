import discord
from collections.abc import Mapping
import tamparser
import json

client = discord.Client()
class Glob:
	functions = {}
	running_games = {}
	deffail = "I don't understand"
	defget = "You took {0}"
def clean(string):
	out = string
	out = out.replace('$','$dollar')
	out = out.replace('{','$lbracket')
	out = out.replace('}','$rbracket')
	return out
def readable(string):
	out = string
	out = out.replace('$lbracket','{')
	out = out.replace('$rbracket','}')
	out = out.replace('$dollar','$')
	return out


class C(str):
	def __new__(cls, value, meta):
		obj = str.__new__(cls, value)
		obj.meta = meta
		return obj
	def strip(obj):
		out = C(str(obj).strip(),obj.meta)
		return out
	def replace(obj,i,j,n=0):
		return C(str(obj).replace(i,j,n if n else -1),obj.meta)

class Game:
	def __init__(self,adventure,private=False):
		self.private = private
		self.rooms = {}
		for key in adventure["rooms"]:
			self.rooms[key] = Room(adventure["rooms"][key])
		self.default_commands = Syntax(adventure["default_commands"])
		self._onfail = adventure["deffailmsg"] if "deffailmsg" in adventure else Glob.deffail
		#TODO: Load variable for adventure
	#formats the return string in accordance to what the file says
	def common_format(string,rest):
		return string.format(*rest.split(" "),left=rest,onfaildefault=self._onfail)

	def player_join(self, player):
		#TODO: Player joins
		pass

class Player:
	def __init__(self,pid,adventure,sroom,inventory=[],flags=[]):
		self.player = pid
		self.game = adventure
		self.inv = inventory
		self.cur_room = sroom
		self.pflags = flags
		self._visited =set()
	def getParse(self,key,value):
		return tamparser.getter(self,key,value)
	def setParse(self,key,value):
		return tamparser.getter(self,key,value)
	def update(self):
		self.game.get_room(self.cur_room)
	def do(self, text):
		self.game.get_room(self.cur_room)[C(text,self)]
	def message(self,text):
		client.get_user(self.player).send_message(text)

class Room:
	def __init__(self,bigobj):
		self.sDesc = bigobj["sDesc"]
		self.lDesc = bigobj["lDesc"]
		self.items = bigobj["items"] if "items" in bigobj else []
		self.commands = Syntax(bigobj["commands"])
		self.exits = bigobj["exits"]

class Syntax(Mapping):
	def __init__(self,*args,**kwargs):
		temp_storage = dict(*args,**kwargs)
		self._storage = {}
		for key in temp_storage:
			branches = []
			for w in temp_storage[key]:
				branches.append(Word(w))
			self._storage[key] = branches

	def __len__(self):
		return len(self._storage)

	def __iter__(self):
		return iter(self._storage)

	def __getitem__(self, phrase):
		for key in self._storage:
			for kw in key.split('|'):
				if phrase.startswith(kw):
					words = self._storage[key]
					for elm in words:
						if elm.meets_requirement(phrase.meta):
							return elm[phrase.replace(kw,'',1).strip()]
		return None
class Word():
	def __init__(self, bigobj):
		self._prereq = [a.split("|") for a in bigobj["prereq"]] if "prereq" in bigobj else []
		self.flave_text = bigobj["fltext"]
		self._words = Syntax(bigobj["commands"])
		self._cons = [a.split("|") for a in bigobj['execute']] if 'execute' in bigobj else []
		self.onfail = bigobj['onfail'] if 'onfail' in bigobj else "{onfaildefault}"
		self._forceend = 'forcepass' in bigobj
	def meets_requirement(self, meta):
		if len(self._prereq) is 0:
			return True
		return all(meta.getParse(con[0],con[1]) for con in self._prereq)
	def execute(self, meta):
		for c in self.con:
			meta.setParse(c[0],c[1])
		
	def __getitem__(self, phrase):
		if len(phrase)>0 and not self._forceend:
			for key in self._words:
				for kw in key.split('|'):
					if phrase.startswith(kw):
						out = self._words[key][phrase.replace(kw,'',1).strip()]
						if out:
							return out
			#If it's not found, return fail
			return self.onfail

		else:
			self.execute(phrase.meta)
			return meta.game.commonformat(self.flave_text,phrase)
			
			
# A bit of my own api since I like to mix actual bot with client
def command(acname=None):
	def wrap(func):
		name = acname if acname else func.__name__
		print(name)
		Glob.functions["!"+name+" "] = func
		return func
	return wrap



@client.event
async def on_ready():
	print('Connected!')
	print('Username: ' + client.user.name)
	print('ID: ' + str(client.user.id))

@client.event
async def on_message(message):
	#this is where the magic happens
	for cname in Glob.functions:
		if message.content.startswith(cname):
			cont = message.content
			cont = cont.replace(cname,'')
			cont = cont.strip()
			await Glob.functions[cname](message, cont)

@command()
async def hi(msg, cont):
	await msg.channel.send("Hello {}".format(msg.author.nick if msg.author.nick else msg.author.name))


c = C("   Nyehehehe  ","what")
ctwo = c.replace(" ",'')
print(ctwo)
print(ctwo.meta)
p = Player(1,2,3)
p.getParse("pflag",4)
token = open("login.token").readline().strip()
client.run(token)
