# Character : Supports characters within the game, which are able to respond to set keywords!
class Character:
    def __init__(self, responseDict):
        self.responseDict = responseDict # Dictionary of keywords and programmed responses
        self.otherResponse = "Sorry, I don't understand." # 

    
    def askAbout(self, thing):
        if thing in self.responseDict:
            print(self.responseDict[thing] + "\n")
        else:
            print(self.otherResponse + "\n")
