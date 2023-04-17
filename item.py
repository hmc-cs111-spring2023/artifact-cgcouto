
class Item:
    # This will be expanded upon as we get into week 2 of the project!
    def __init__(self, name, look, pickup, use, grabBool, opens, contains):
        self.name = name
        self.lookText = look
        self.grabbable = grabBool
        self.useText = use
        self.takeText = pickup
        self.contains = contains
        self.opens = opens
        self.status = "test"

    def onLook(self):
        print(self.lookText)

    def onInspect(self):
        print(self.lookText)

    def onTake(self):
        if self.grabbable:
            print(self.takeText)
            return self.name
        else:
            print("You cannot pick that up.")

    
    def onUse(self):
        print(self.useText)
        return self.contains

    
