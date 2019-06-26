import discord

client = discord.Client()
class Glob:
	functions = {}
	running_games = {}
	def clean(string):
		out = string
		out = out.replace('$','$dollar')
		out = out.replace('[','$lbracket')
		out = out.replace(']','$rbracket')
		return out
	def readable(string):
		out = string
		out = out.replace('$lbracket','[')
		out = out.replace('$rbracket',']')
		out = out.replace('$dollar','$')
		return out

class Game:
	def __init__(self,adventure,private=false):
		self.private = private
		#TODO: Load variable for adventure


	def player_join(self, player):
		#TODO: Player joins

class Player:
	def __init__(self,pID,sroom,inventory=[],flags=[]):
		self.player = pid
		self.game = adventure
		self.inv = inventory
		self.cur_room = sroom
		self.pflags = flags
class Room:
	def __init__(self,bigobj):
		self.rid = bigobj["rid"]
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
			if any(phrase.startswith(kw) for kw in key.split('|')):
				words = self._storage[key]
				for elm in words:
					if elm.meets_requirement():
						return elm[phrase.replace(key,'',1).strip()]
		return None
class Word():
	def __init__(self, bigobj):
		self.prereq = Prereq(bigobj["prereq"] if "prereq" in bigobj else [])
		self.flave_text = bigobj["fltext"]
		self.words = Syntax(bigobj["commands"])
		self.cons = bigobj['execute']
		self.onfail = bigobj['onfail'] if 'onfail' in bigobj else "[onfaildefault]"



# A bit of my own api since I like to mix actual bot with client
def command(acname=None):
	def wrap(func):
		name = acname if acname else func.__name__
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



token = open(login.token).readline()
client.run(token)
