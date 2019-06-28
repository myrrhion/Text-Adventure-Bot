import discord
from collections.abc import Mapping
import tamparser
import json
import os
import asyncio

client = discord.Client()
class Glob:
	functions = {}
	running_games = {}
	session = 0
	active_players = {}
	deffail = "I don't understand"
	defget = "You took {0}"
	def newsession():
		Glob.session += 1
		return Glob.session
	compass = [{"n":"n","e":"e","s":"s","w":"w"},{"n":"north","e":"east","s":"south","w":"west"}]

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
	def replace(obj,i,j,n=-1):
		out = C(str(obj).replace(i,j,n),obj.meta)
		return out

class Game:
	def __init__(self,adventure,player,private=False):
		self.private = private
		self.rooms = adventure.get("rooms")
		self.default_commands = adventure.get("default_commands",[])
		self._onfail = adventure.get("deffailmsg",Glob.deffail)
		self._flags = adventure.get("flags",set())
		self.items = adventure.get("items",[])
		self.config = adventure.get("config",[])
		self._stdget = adventure.get("stdget",[])
		self.players = []
		#TODO: Load variable for adventure
	#formats the return string in accordance to what the file says
	def common_format(self,string,rest):
		return string.format(*rest.split(" "),left=rest,onfaildefault=self._onfail)

	async def player_join(self, player):
		if player in Glob.active_players:
			return None
		p = Player(player,self,**self.config["player"][str(len(self.players))])
		self.players.append(p)
		Glob.active_players[player] = p
		await p.update()
	def get_room(self,index):
		return self.rooms[index]
	def __getitem__(self, text):
		out = self.rooms[text.meta.cur_room][text]
		if not out or not out.meta:
			snd = self.default_commands[text]
			out = snd if snd and out and not out.meta else out
		if not out or not out.meta:
			snd = self._stdget[text]
			out = snd if snd and not (out and not out.meta) else out
		if not out:
			out = self.common_format("{onfaildefault}",text)
		return out
	def get_items(self, lst):
		return [r for r in self.items if r["id"] in lst ]
	def end(self):
		for p in self.players:
			del Glob.active_players[p.id]
		del Glob.running_games[Glob.running_games.index(self)]

class Player:
	def __init__(self,pid,adventure,sroom="start",inventory=[],flags=[]):
		self.player = pid
		self.game = adventure
		self.inv = set(inventory)
		self.cur_room = sroom
		self.pflags = set(flags)
		self._visited =set()
	def __eq__(self,other):
		return self.player is other.player
	def __getattr__(self, name):
		print(str(name))
		msg = ""
		if str(name) == "inventory":
			msg = "You are carrying"
			anitems = ["an "+f["sdesc"] if any(f["sdesc"].startswith(v) for v in "aeiou") else "a "+f["sdesc"] for f in self.game.get_items(self.inv)]
			if len(anitems)>2:
				msg +=" "+", ".join(anitems[:-2])
			if len(anitems)>1:
				msg += "{} and".format(anitems[-2])
			if len(anitems)>0:
				msg += " "+anitems[-1]+"."
			else:
				msg +=" nothing."
		return msg
	def getParse(self,key,value):
		return tamparser.getter(self,key,value)
	def setParse(self,key,value):
		return tamparser.setter(self,key,value)
	async def update(self):
		msg = ""
		r = self.game.get_room(self.cur_room)
		msg += r.sDesc if self.cur_room in self._visited else r.lDesc
		if r.items:
			msg +='\n'
			msg += "On the ground you see"
			anitems = ["an "+f["sdesc"] if any(f["sdesc"].startswith(v) for v in "aeiou") else "a "+f["sdesc"] for f in self.game.get_items(r.items)]
			if len(anitems)>2:
				msg +=" "+", ".join(anitems[:-2])
			if len(anitems)>1:
				msg += "{} and".format(anitems[-2])
			msg += " "+anitems[-1]+"."
		if r.exits:
			msg +='\n'
			msg += "Visible exit{} {}".format("","is" if len(r.exits) is 1 else "s","are")
			anitems = r.exits
			if len(anitems)>2:
				msg +=" "+", ".join(anitems[:-2])
			if len(anitems)>1:
				msg += "{} and".format(anitems[-2])
			msg += " "+anitems[-1]+"."
		self._visited.add(self.cur_room)
		await self.message(msg)

	def do(self, text):
		out = self.game[C(text,self)]
		return out
	async def message(self,text):
		await client.get_user(self.player).send(text)
	def get_room(self):
		return self.game.get_room(self.cur_room)

class Room:
	def __init__(self,bigobj):
		self.sDesc = bigobj["sDesc"]
		self.lDesc = bigobj["lDesc"]
		self.items = set(bigobj["items"]) if "items" in bigobj else set()
		self.commands = Syntax(bigobj["commands"])
		rawexits = bigobj["exits"]
		self.exits = []
		refexits = {}
		for e in rawexits:
			out = "go "+e
			pretty = e
			if all(d in "nesw" for d in e):
				out = []
				temp = ["{" + letter + "}" for letter in e]
				out = ["".join(temp)]+[" ".join(temp)]
				out = ["go "+di for di in out]+out
				out = [i.format(**Glob.compass[0]) for i in out] + [i.format(**Glob.compass[1]) for i in out]
				pretty = " ".join(temp).format(**Glob.compass[1])
			refexits["|".join(out)] = [{"fltext":"You go {}".format(pretty),"onfail":"can't go {0}","execute":["gotoroom|{}".format(rawexits[e])]}]
			self.exits.append(pretty)
		self._exits = Syntax(refexits)
		
	def __getitem__(self,phrase):
		out = self.commands[phrase]
		if not out or not out.meta:
			snd = self.try_exit(phrase)
			out = snd if snd else out
		return out
	def try_exit(self,phrase):
		return self._exits[phrase]

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
			print(phrase)
			for kw in key.split('|'):
				if phrase.lower().startswith(kw):
					words = self._storage[key]
					for elm in words:
						if elm.meets_requirement(phrase.meta):
							return elm[phrase.replace(kw,'',1).strip()]
		return None
class Word():
	def __init__(self, bigobj):
		self._prereq = [a.split("|") for a in bigobj["prereq"]] if "prereq" in bigobj else []
		self.flave_text = bigobj["fltext"]
		self._words = Syntax(bigobj["commands"] if "commands" in bigobj else [])
		self._cons = [a.split("|") for a in bigobj['execute']] if 'execute' in bigobj else []
		self.onfail = C(bigobj['onfail'] if 'onfail' in bigobj else "{onfaildefault}",False)
		self._forceend = 'forcepass' in bigobj
	def meets_requirement(self, meta):
		if len(self._prereq) is 0:
			return True
		return all(meta.getParse(con[0],con[1]) for con in self._prereq)
	def execute(self, meta):
		for c in self._cons:
			meta.setParse(c[0],c[1])
		
	def __getitem__(self, phrase):
		if len(phrase)>0 and not self._forceend:
			out = self._words[phrase]
			if out:
				return out
			#If it's not found, return fail
			return C(phrase.meta.game.common_format(self.onfail,phrase),False)

		else:
			self.execute(phrase.meta)
			return C(phrase.meta.game.common_format(self.flave_text,phrase),True)
			
			
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
			return
	#only loads when no command was used
	
	if message.channel.type is not discord.enums.ChannelType.private:
		return
	p = Glob.active_players.get(message.author.id)
	if p:
		await p.message(readable(p.do(clean(message.content))))
		await p.update()

#Adventure loading magics
def load_adventure(name,rep="adventures/"):
	path = rep+name
	if not os.path.exists(path):
		return None
	files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
	out = {}
	#room files are read
	out["rooms"] = {}
	for room in [b for b in files if b.endswith(".room")]:
		out["rooms"][room[:room.rfind('.')]] = Room(json.load(open(os.path.join(path, room))))
	#default commands. Note that it would only set the last found file
	out["default_commands"] = Syntax(json.load(open(os.path.join(rep, name+".default_commands"))))
	out["config"] = json.load(open(os.path.join(rep, name+".conf")))
	out["items"] = json.load(open(os.path.join(rep, name+".items")))
	stdget = {}

	getty = {}
	getty["fltext"] = "What do you want to take?"
	getty["onfail"] = "You can't get {left}"
	getty["commands"] = {}
	for i in out["items"]:
		item = {}
		item["fltext"]= "you got "+i["display"]
		item["prereq"]= ["iteminroom|"+i["id"]]
		item["execute"]= ["pickup|"+i["id"]]
		getty["commands"][i["syn"]] = [item]
	stdget["take|get|pickup"]= [getty]
	putty = {}
	putty["fltext"] = "What do you want to drop?"
	putty["onfail"] = "You can't drop {left}"
	putty["commands"] = {}
	for i in out["items"]:
		item = {}
		item["fltext"]= "you dropped "+i["display"]
		item["prereq"]= ["hasitem|"+i["id"]]
		item["execute"]= ["drop|"+i["id"]]
		putty["commands"][i["syn"]] = [item]
	stdget["put down|drop"]= [putty]
	inv = {}
	inv["fltext"]= "{left.meta.inventory}"
	stdget["inventory|inv|i"]= [inv]
	out["stdget"] = Syntax(stdget)
	return out

@command()
async def hi(msg, cont):
	await msg.channel.send("Hello {}".format(msg.author.nick if msg.author.nick else msg.author.name))



@command()
async def start_game(msg, cont):
	dat = list(cont.split(" "))
	name = dat[0]
	if msg.author.id in Glob.active_players:
		await msg.author.send("Already playing")
		return
	key = dat[1] if len(dat)>1 else "session{:06d}".format(Glob.newsession())
	g = load_adventure(name)
	if key in Glob.running_games:
		await msg.author.send("Key already taken")
		return
	Glob.running_games[key]= Game(g,msg.author.id)
	await msg.author.send("Game {} tarted with ID {}".format(name,key))
	await Glob.running_games[key].player_join(msg.author.id)
	print("Test done")



token = open("login.token").readline().strip()
client.run(token)
