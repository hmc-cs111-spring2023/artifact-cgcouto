class Room():
    # A pretty barebones class ngl... probably could be refactored into a better form
    def __init__(self, roomID, neighbors, text):
        self.roomID = roomID
        self.neighbors = neighbors
        self.items = []
        self.text = text