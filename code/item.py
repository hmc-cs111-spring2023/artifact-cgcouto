class Item:

    def __init__(self, name, look, pickup, use, grabBool, opens, contains, image, end):
        self.name = name # The item name as a string (ex. bucket)
        self.lookText = look # Prints out on look
        self.grabbable = grabBool # Boolean that sets whether you can add it to inv or not
        self.useText = use # Prints out on use
        self.takeText = pickup # Prints out on pickup
        self.contains = contains # List of item names that this item contains
        self.opens = opens # Item name that this item interacts with
        self.image = image # filepath to relevant ASCII image
        self.end = end # Boolean that describes whether it's an end state or not

    # Print look text and ASCII if relevant
    def onLook(self):
        if self.image != "":
            print(open("../examples/"+self.image).read())
            print("")
        print(self.lookText + "\n")

    # Print take text and pass back item name for engine to handle
    def onTake(self):
        if self.grabbable:
            print(self.takeText + "\n")
            return self.name
        else:
            print("You cannot pick that up." + "\n")

    # Print use text and pass back contained items for engine to handle
    def onUse(self):
        print(self.useText + "\n")
        return self.contains

    
