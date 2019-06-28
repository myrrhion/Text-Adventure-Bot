```
DISCLAIMER
This whole bot is a right mess and hacked together.
And hopefully the 80% done it needs to work.
The other 20% are better features anyway.

disregard Anything pushed after PDT 23:59:59 for the competition.
I will continue working on this since I like it.
```

# Text-Adventure-Bot

A bot that isn't just *one* text adventure, but rather a bot that can be used to make *more text adventures*.
Sadly, due to having a toddler, and living in europe, I couldn't make all the feauters I wanted.
A short list of planned features:
  * Multiplayer
  * ... that is pretty much it.

this whole thing is, as of now, capable of playing adventures that have been prepared.
Sadly, aside from a few room adventure as a proof of concept, most energy went into writing the parser system.
Writing a single game might have been faster in the short term, but isn't this whole hackathon about trying to share with the community?


# TAM syntax
TAM is just JSON on the outside, but on the inside is a system that allows you to write interactive adventures.
You should look up how JSON works to get more of an insight into how it works.

You can find working samples in the adventure folder.
## Room Syntax
each room is saved as `{roomid}.room` in the subfolder with the same name as
A lot of the making it easier tools can be emulated using the syntax for the effects of commands.
In front of the room there has to be the Room Id, used for traversel. 
Has to be unique or there will be errors.
### Short Description
`"sDesc": "string"`
The short description of the room when entering it the second+ time,
### Long Description
`"lDesc": "string"`
Long description of the room when entering it for the first time.
**Important**: You are responsible for having the long description show when using the "look" command.
### Items
`"items":["valid itemId","valid itemId",]` _Optional_
list of items that just lie around in the room. 
This is a beginner friendly mechanic that allows the player to take and drop items in rooms.
Each element in the list is the itemId of an item defined in the items section of the game.
### Exits
`"exits":{"string":"valid rid","string":"valid rid"...}` _(technically) Optional_
list of room transitions.
Another beginner adventure designer help tool.
The first element of the key|value pair is a direction. Available directions are the cardinal directions (up to the thrid degree) in their shortened form, e.g. `n`, `w`, `s`, `e`, `ne`, `ssw`, `ene` and so on.
The second is the rid of a room that exists.
players navigate these by typing, as an example for traversing north east: "go north east", "nort east", "northeast", "go ne" or "ne"
**Important**: local definitions of these keywords will overwrite them.
### Valid Commands
`commands:{}`
The valid commands.
Setting these up is a story onto itself, it is completely covered in the section **Command Syntax**.

## Item Syntax
Items are saved in `{gamename}.items`
they are, each a {} object in a [] list
### ID
`"id":"string"`
this is the ID that is used by the engine internally. Doesn't have to look good, just has to be unique.
### Short Description
`sdesc":"string"`
a short description of the item that is diplayed when looking at the inventory of if the item is on the ground/in the room.
### Synonyms
`"syn":"string1|string2|knife`
a list of synonyms for the item. Is used by the engine for the drop and get mechanic.
As of now, the engine doesn't deal with overloading terms (e.g. if you call both a dull knife and a sharp knife a knife)

`"display":"yon dagger"`


## Command Syntax
Command syntax is highly complex. I tried to make it as versatile as possible while keeping it easy for beginners.
The command syntax is based on nesting simple words and chaining them.
But, you can also go for complete sentences, if that is more your thing, chaining is advanced and mostly for internal usage anyway.
getting a command is done in two steps. First it checks whether the word exists, after that it checks which consequence it should execute each word is written as
`**Word**:[{option a}, {option b}, {option c}]`
options are built according to the instructions written below
### Options
the actual words are in here:
#### Conditionals
`"prereq":{["getter|value"]}` _Optional_
This is to make the game progress. 
for a list of commands, see below
The first option where all prerequisits are met will be chosen.
if this is not given, it will be considered True
#### Flavour Text
`"fltext":"string"`
flavour text displayed when this is the end of the entry command.
a few keywords that can be dynamically replaced are: 
  * **{left}**: this is replaced with all not matched words
  * **{#}**: with # being a number, it will replace itself with the non-read word at the appropriate position, starting with 0
  * **{ondefaultfail}** default fail message will be inserted.
### Further words
`commands:{}` _Optional_
Further commands down the line.
This is, protentially, infintely extendable.
You just add another set of commands built like this in it.
