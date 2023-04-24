class Engine():
    def __init__(self, rooms, items, characters, start):
        self.rooms = rooms
        self.items = items 
        self.characters = characters
        self.inventory = []
        self.start = start

    # Update the current room provided it's a supported direction to navigate to
    # currentRoom (int) : id of the current room 
    # dir (string) : hopefully a NSEW direction, but maybe not
    def navigate(self, currentRoom, dir):
        compass = ["north", "south", "east", "west"]
        if dir in compass:
            checkDir = self.rooms[currentRoom].neighbors[compass.index(dir)]
            if checkDir != None and not self.rooms[currentRoom].blocked:
                currentRoom = checkDir
            else:
                print("You cannot go that way.")
        else:
            print("Sorry, you can only go north, south, east, and west.")

        return currentRoom
    
    # Ask a character about an object, provided the character is in the current room
    # currentRoom (int) : id of the current room 
    # character (string) : character key to be checked against current room's character dict
    # thing (string) : key to be checked within character's dialogue dict, if such a character exists
    def askabout(self, currentRoom, character, thing):
        if character in self.rooms[currentRoom].characters:
            # Pull out relevant character from dict, run askAbout function on it
            self.rooms[currentRoom].characters[character].askAbout(thing)
        else:
            # We didn't get a hit on the character, so print generic confusion text
            print("I don't know who you're trying to talk to.")

    def takeItem(self, currentRoom, item):
        if item in self.rooms[currentRoom].items:
            result = self.rooms[currentRoom].items[item].onTake()
            if type(result) == str:
                self.inventory.append(self.rooms[currentRoom].items[result])
            # remove item from room dict 
            del self.rooms[currentRoom].items[item]
        else:
            print("I don't see that in here.")

    def useOn(self, currentRoom, heldItem, object):
        if heldItem in [c.name for c in self.inventory] and object in self.rooms[currentRoom].items:
            self.inventory[[c.name for c in self.inventory].index(heldItem)].onUse()
            self.inventory.remove(self.inventory[[c.name for c in self.inventory].index(heldItem)])

            contained_items = self.rooms[currentRoom].items[object].onUse()
            for item in contained_items:
                # add to inventory
                self.inventory.append(self.rooms[currentRoom].items[item])
                self.rooms[currentRoom].items[item].onTake()
                # remove from room
                del self.rooms[currentRoom].items[item]


    def lookAt(self, currentRoom, object):
        if object in self.rooms[currentRoom].items:
            self.rooms[currentRoom].items[object].onLook()


    def printInventory(self):
        if len(self.inventory) == 0:
            print("EMPTY")
        else:
            for item in self.inventory:
                print(item.name.upper())

        
    
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
        print("look at X : where X is a character or object")
        print("inventory : returns contents of player inventory")
        print("exit/quit : quit the game")
        print("")


    # Run the core game loop!
    def run(self):
        currentRoom = self.start # Start at the designated start point given in the DSL
        while True:
            # Ask for input, parse it and change state accordingly

            # Print current room's flavor text
            print(self.rooms[currentRoom].text)

            # self.rooms[currentRoom].status 

            user_input = str(input()).split(' ')

            # Supported commands (so far)
            if user_input[0] == "help":
                self.help_user(user_input)
            elif user_input[0]  == "exit" or user_input[0] == "quit":
                break
            elif user_input[0] == "go":
                currentRoom = self.navigate(currentRoom, user_input[1])
            elif user_input[0] == "ask" and user_input[2] == "about":
                self.askabout(currentRoom, user_input[1], user_input[3])
            elif user_input[0] == "take":
                self.takeItem(currentRoom, user_input[1])
            elif user_input[0] == "use" and user_input[2] == "on":
                self.useOn(currentRoom, user_input[1], user_input[3])
            elif user_input[0] == "look" and user_input[1] == "at":
                self.lookAt(currentRoom, user_input[2])
            elif user_input[0] == "inventory":
                self.printInventory()
            else:
                print("I don't understand what you're saying.")



