class Room():
    def __init__(self, roomID, neighbors, text):
        self.roomID = roomID
        self.neighbors = neighbors
        self.items = []
        self.text = text