class Room():
    # A pretty barebones class ngl... probably could be refactored into a better form
    def __init__(self, roomID, neighbors, characters, items, text, image):
        self.roomID = roomID
        self.neighbors = neighbors
        self.items = items
        self.characters = characters
        self.text = text
        self.blocked = False
        self.opensWith = []
        self.image = image