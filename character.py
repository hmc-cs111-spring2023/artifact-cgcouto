class Character:
    def __init__(self, responseDict):
        self.responseDict = responseDict
        self.otherResponse = "Sorry, I don't understand."
        self.hasItems = []
        self.ASCII = ""

    def askAbout(self, thing):
        if thing in self.responseDict:
            print(self.responseDict[thing])
        else:
            print(self.otherResponse)
            
    def giveItem(self, thing):
        print("yes")
