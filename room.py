class Room():
    def __init__(self, roomID):
        self.roomID = roomID
        self.neighbors = [0, 0, 0, 0]
        self.items = []
        self.text = ""