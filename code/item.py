class Item:

    def __init__(self, name, look, pickup, use, grabBool, opens, contains, image, end):
        self.name = name
        self.lookText = look
        self.grabbable = grabBool
        self.useText = use
        self.takeText = pickup
        self.contains = contains
        self.opens = opens
        self.status = "test"
        self.image = image
        self.end = end

    def onLook(self):
        if self.image != "":
            print(open(self.image).read())
            print("")
        else:
            print("miss")
        print(self.lookText + "\n")


    def onTake(self):
        if self.grabbable:
            print(self.takeText + "\n")
            return self.name
        else:
            print("You cannot pick that up." + "\n")

    
    def onUse(self):
        print(self.useText)
        return self.contains

    
