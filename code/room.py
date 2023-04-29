# Room : Stores all the details about a room in the game
class Room():

    def __init__(self, roomID, neighbors, characters, items, text, image, opensWith, end):
        self.roomID = roomID # The index of this room 
        self.neighbors = neighbors # The indices of neighboring rooms (as stored in the list in Engine) in N S E W order
        self.items = items # List of items within this room
        self.characters = characters # List of characters within this room
        self.text = text # Text that prints when this room is entered/stayed in
        self.opensWith = opensWith # Item names that will make this room unblocked (allowing entry)
        self.image = image # filename for relevant ASCII image
        self.end = end # boolean as to whether this room is an end state or not

    # Determines whether a given object unblocks a room!
    # object (string) : the name of the object the player is using on the door
    def openRoom(self, object):
        if object in self.opensWith:
            self.opensWith.remove(object)
            return object