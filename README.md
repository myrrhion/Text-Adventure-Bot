# Text-Adventure-Bot

This whole bot is a right mess and hacked together.
And hopefully the 80% done it needs to work.
The other 20% are better features anyway.

# TAM syntax
TAM is just JSON on the outside, but on the inside is a system that allows you to write interactive adventures.
## Room Syntax
All of the room is between `{}`
order is irrelevant, capitalisation is **_very important_**.
A lot of the making it easier tools can be emulated using the syntax for the effects of commands.

`"rid":"string"`
Room Id, used for traversel. 
Has to be unique or there will be errors.
`"sDesc": "string"`
The short description of the room when entering it the second+ time,
`"lDesc": "string"`
Long description of the room when entering it for the first time.
**Important**: You are responsible for having the long description show when using the "look" command.
`"items":["valid itemId","valid itemId",]` _Optional_
list of items that just lie around in the room. 
This is a beginner friendly mechanic that allows the player to take and drop items in rooms.
Each element in the list is the itemId of an item defined in the items section of the game.
`"exits":{"string":"valid rid","string":"valid rid"...}` _(technically) Optional_
list of room transitions.
Another beginner adventure designer help tool.
The first element of the key|value pair is a direction. Available directions are the cardinal directions (up to the thrid degree) in their shortened form, e.g. `n`, `w`, `s`, `e`, `ne`, `ssw`, `ene` and so on.
The second is the rid of a room that exists.
players navigate these by typing, as an example for traversing north east: "go north east", "nort east", "northeast", "go ne" or "ne"
**Important**: local definitions of these keywords will overwrite them.
`commands:{}`
The valid commands.
Setting these up is a story onto itself, it is completely covered in the section **Syntax**.
