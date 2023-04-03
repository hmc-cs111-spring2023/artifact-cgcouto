class Engine():
    def __init__(self, rooms, items):
        self.rooms = rooms # Currently works
        self.items = items # To-do for week 2!
        self.inventory = [False]*len(items)

    # Update the current room provided it's a supported direction to navigate to
    # currentRoom (int) : id of the current room 
    # dir (string) : hopefully a NSEW direction, but maybe not
    def navigate(self, currentRoom, dir):
        compass = ["north", "south", "east", "west"]
        if dir in compass:
            checkDir = self.rooms[currentRoom].neighbors[compass.index(dir)]
            if checkDir != None:
                currentRoom = checkDir
            else:
                print("You cannot go that way.")
        else:
            print("Sorry, you can only go north, south, east, and west.")

        return currentRoom
    
    # Prints out a list of supported commands
    # input (string) : optional, if the user specifies a specific command to get help with
    def help_user(self, input):
        print("yes") # Need to do this still


    # Run the core game loop!
    def run(self):
        currentRoom = 0 # Start in the first room in the array
        while True:
            # Ask for input, parse it and change state accordingly

            # Print current room's flavor text
            print(self.rooms[currentRoom].text)

            user_input = str(input()).split(' ')

            # Supported commands (so far)
            if user_input[0] == "help":
                self.help_user(user_input)
            elif user_input[0]  == "exit" or user_input[0] == "quit":
                break
            elif user_input[0] == "go":
                print("[" + user_input[1] + "]")
                currentRoom = self.navigate(currentRoom, user_input[1])
            else:
                print("I don't understand what you're saying.")



