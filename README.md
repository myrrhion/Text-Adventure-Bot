# Text-Adventure-Bot

This whole bot is a right mess and hacked together.
And hopefully the 80% done it needs to work.
The other 20% are better features anyway.

# TAM syntax
TAM is just JSON on the outside, but on the inside is a system that allows you to write interactive adventures.
You should look up how JSON works to get more of an insight into how it works.
## Room Syntax
All of the room is between `RiD:{}`
order is irrelevant, capitalisation is **_very important_**.
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
## Command Syntax
Command syntax is highly complex. I tried to make it as versatile as possible while keeping it easy for beginners.
The command syntax is based on nesting simple words and chaining them.
getting a command is done in two steps. First it checks whether the word exists, after that it checks which consequence it should execute each word is written as
`**Word**:[{option a}, {option b}, {option c}]`
options are built according to the instructions written below
### Words
`"prereq":{prerequisit object}` _Optional_
This is to make the game progress. The first option where all prerequisits are met will be chosen.
### Flavour Text
`"fltext":"string"`
flavour text displayed when this is the end of the entry command.
### Further words
`commands:{}` _Optional_
Further commands down the line.
This is, protentially, infintely extendable.
You just add another set of commands built like this in it.
