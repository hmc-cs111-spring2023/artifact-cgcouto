
# Engine : Handles running the game, interfacing with all the rooms, items, and characters within it!
class Engine():
    def __init__(self, rooms, items, characters, start):
        self.rooms = rooms # a list of Room objects within the game
        self.items = items # a list of items within the game
        self.characters = characters # a list of characters within the game
        self.inventory = [] # player inventory (stores item names)
        self.start = start # the index of the game's starting room (in self.rooms)

    # Update the current room provided it's a supported direction to navigate to
    # currentRoom (int) : id of the current room 
    # dir (string) : hopefully a NSEW direction, but maybe not
    def navigate(self, currentRoom, input):
        dir = " ".join(input) # Put the direction together
        compass = ["north", "south", "east", "west"]
        if dir in compass:
            checkDir = self.rooms[currentRoom].neighbors[compass.index(dir)]
            if checkDir != None:
                if len(self.rooms[checkDir].opensWith) == 0:
                    currentRoom = checkDir
                else:
                    print("That way is blocked, but you can unblock it somehow!" + "\n")
            else:
                print("You cannot go that way." + "\n")
        else:
            print("Sorry, you can only go north, south, east, and west." + "\n")

        return currentRoom
    
    # Ask a character about an object, provided the character is in the current room
    # currentRoom (int) : id of the current room 
    # character (string) : character key to be checked against current room's character dict
    # thing (string) : key to be checked within character's dialogue dict, if such a character exists
    def askAbout(self, currentRoom, character, input):
        thing = " ".join(input)
        if character in self.rooms[currentRoom].characters:
            # Pull out relevant character from dict, run askAbout function on it
            self.rooms[currentRoom].characters[character].askAbout(thing)
        else:
            # We didn't get a hit on the character, so print generic confusion text
            print("I don't know who you're trying to talk to." + "\n")

    # Determine whether an item can be picked up by the player
    # currentRoom (int) : id of the current room
    # item (string) : name of the item that will be checked
    def takeItem(self, currentRoom, input):
        item = " ".join(input) # Put the object together
        # Only go forth if the item actually lives in our room
        if item in self.rooms[currentRoom].items:
            # Run the take function for that item, see what comes out
            result = self.rooms[currentRoom].items[item].onTake()

            # If it's grabbable, the name gets returned and that goes in our inventory
            if type(result) == str:
                self.inventory.append(self.rooms[currentRoom].items[result])

            # Check whether this item is an end state, exit if it is!
            try:
                if self.rooms[currentRoom].items[result].end:
                    exit(-1)
            finally:
                # Otherwise we just remove it from the room and carry on
                del self.rooms[currentRoom].items[item]

        else:
            print("I don't see that in here." + "\n")

    # Handles using an inventory item on an object/locked door
    # currentRoom (int) : the index of the room the player is currently in
    # input (string) : player input, containing potential objects/doors
    def useOn(self, currentRoom, input):
        heldItem = input[1]
        object = " ".join(input[3:]) # Put the object together
        compass = ["north", "south", "east", "west"]
        doors = ["north door", "south door", "east door", "west door"]

        if heldItem in [c.name for c in self.inventory]: # Use on items
            if object in self.rooms[currentRoom].items:
                # If we get a hit, use the item in inventory and delete it
                self.inventory[[c.name for c in self.inventory].index(heldItem)].onUse()
                self.inventory.remove(self.inventory[[c.name for c in self.inventory].index(heldItem)])

                # Find the items that are contained within the opened item (if any)
                contained_items = self.rooms[currentRoom].items[object].contains
                for item in contained_items:
                    # Add to inventory
                    self.inventory.append(self.rooms[currentRoom].items[item])
                    self.rooms[currentRoom].items[item].onTake()

                    # If it's an end state, end the game
                    if self.rooms[currentRoom].items[item].end:
                        exit(-1)

                    # Remove it from the room
                    del self.rooms[currentRoom].items[item]
            elif object in doors: # Use on locked doors
                # get matching index of NSEW search, pull out room neighbor, try opens
                checkDir = self.rooms[currentRoom].neighbors[doors.index(object)]
                if checkDir != None:
                    result = self.rooms[checkDir].openRoom(heldItem)
                    if result == heldItem:
                        # Print the use text for the used item
                        self.inventory[[c.name for c in self.inventory].index(heldItem)].onUse()

                        # Remove it from inventory
                        self.inventory.remove(self.inventory[[c.name for c in self.inventory].index(heldItem)])

                    else:
                        print("Sorry, you can't use that here."+"\n")
                else:
                    print("That won't work here."+"\n")
            else:
                print("I don't understand what you're trying to use that on."+"\n")
        elif object in self.rooms[currentRoom].items:
            print("I don't understand what you're trying to use."+"\n")
        else:
            print("I don't understand what you're trying to use and what you're trying to use it on!"+"\n")


    # Handles looking at a possible object in the current room
    def lookAt(self, currentRoom, input):
        object = " ".join(input) # Put the object together
        if object in self.rooms[currentRoom].items:
            self.rooms[currentRoom].items[object].onLook()
        else:
            print("I don't see that here." + "\n")

    # Prints out the current inventory for the player
    def printInventory(self):
        items = []
        if len(self.inventory) == 0:
            items.append("EMPTY")
        else:
            for item in self.inventory:
                items.append(item.name.upper())
        print("~"*max([len(item) for item in items]))
        [print(item) for item in items]
        print("~"*max([len(item) for item in items]))
        print("")

        
    
    # Prints out a list of supported commands
    # input (string) : optional, if the user specifies a specific command to get help with
    def help_user(self, input):
        print("")
        print("SUPPORTED COMMANDS")
        print("~~~~~~~~~~~~~~~~~~")
        print("go X : where X is a cardinal direction")
        print("ask X about Y : where X is a character, Y is an character or object")
        print("take X : where X is an object")
        print("use X on Y : where X is an object in your inventory and Y is another object")
        print("use X on Y door : where X is an object in your inventory and Y is a cardinal direction")
        print("look at X : where X is a character or object")
        print("inventory : returns contents of player inventory")
        print("help : prints out a list of supported commands")
        print("exit/quit : quit the game")
        print("")


    # Run the core game loop!
    def run(self):
        currentRoom = self.start # Start at the designated start point given in the DSL
        print("")
        while True:
            # Ask for input, parse it and change state accordingly

            # Print current room's flavor text (plus image if present)
            if self.rooms[currentRoom].image != "":
                print(open(self.rooms[currentRoom].image).read())
                print("")
            print(self.rooms[currentRoom].text + "\n")

            # If we've entered a room that's an end state, end the game
            if self.rooms[currentRoom].end:
                break

            print("> ", end="") 

            raw_input = str(input())
            user_input = [i for i in raw_input.split(' ') if i != '']

            print("")

            # Search for upported commands 
            if raw_input.strip() == "help":
                self.help_user(user_input)
            elif raw_input == "exit" or raw_input == "quit":
                break
            elif user_input[0] == "go":
                currentRoom = self.navigate(currentRoom, user_input[1:])
            elif user_input[0] == "ask" and user_input[2] == "about":
                self.askAbout(currentRoom, user_input[1], user_input[3:])
            elif user_input[0] == "take":
                self.takeItem(currentRoom, user_input[1:])
            elif user_input[0] == "use" and user_input[2] == "on":
                self.useOn(currentRoom, user_input)
            elif user_input[0] == "look" and user_input[1] == "at":
                self.lookAt(currentRoom, user_input[2:])
            elif raw_input.strip() == "inventory":
                self.printInventory()
            else:
                print("I don't understand what you're saying." + "\n")



