from engine import Engine
from room import Room

# Same as adventure.game, just written in native Python instead of my external DSL

startingRoom = Room(0, [1,2,None,None], "You find yourself in a dark room. A door leads to the north, while a cave opens to the south.")

skullRoom = Room(1, [None,0,None,None], "You've arrived in a dingy cave. You can go north to return to the starting room.")

treasureRoom = Room(2, [0,None,None,None], "Wow, there's a treasure chest in here! You can't open it though (at least not yet). The starting room resides to the south.")

engine = Engine([startingRoom, skullRoom, treasureRoom],[])

engine.run()
