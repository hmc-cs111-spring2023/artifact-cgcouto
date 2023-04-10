class Room():
    # A pretty barebones class ngl... probably could be refactored into a better form
    def __init__(self, roomID, neighbors, characters, text):
        self.roomID = roomID
        self.neighbors = neighbors
        self.items = []
        self.characters = characters
        self.text = text
        self.blocked = False