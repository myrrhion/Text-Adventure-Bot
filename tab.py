import discord

client = discord.Client()
class Glob:
	functions = {}
	running_games = {}


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
class Syntax(MutableMapping):
	def __init__(self,*args,**kwargs):
		self._storage = dict(*args,**kwargs)

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
