from engine import Engine
from room import Room

startingRoom = Room(0)
startingRoom.neighbors = [1,2,None,None]
startingRoom.text = "You are in a concrete room. An opened door lies to the south, while a dark cave resides to the north."

skullRoom = Room(1)
skullRoom.neighbors = [None,0,None,None]
skullRoom.text = "Whoa, this is a cave! And there's a skull in here... You can go south to return to the concrete room."

treasureRoom = Room(2)
treasureRoom.neighbors = [0,None,None,None]
treasureRoom.text = "There's a locked treasure chest in here! The concrete room resides to the north."


engine = Engine([startingRoom, skullRoom, treasureRoom],[])

engine.run()
