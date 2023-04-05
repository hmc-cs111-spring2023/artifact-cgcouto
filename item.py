
class Item:
    # This will be expanded upon as we get into week 2 of the project!
    def __init__(self):
        self.name = ""
        self.lookText = ""
        self.grabbable = False
        self.useText = ""
        self.takeText = ""
        self.contains = False

    def onLook(self):
        print(self.lookText)

    def onInspect(self):
        print(self.lookText)

    def onTake(self):
        if self.grabbable:
            print(self.takeText)
        else:
            print("You cannot pick that up.")

    
    def onUse(self):

        if self.contains:
            # Add contained object(s) to inventory, print takeText
            print('yes')

    
