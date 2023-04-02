from room import Room

class Engine():
    def __init__(self, rooms, items):
        self.rooms = rooms
        self.items = items
        self.inventory = [False]*len(items)

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
    
    def help_user(self, input):
        print("yes")



    def run(self):
        currentRoom = 0
        while True:
            # ask for input, parse it and do stuff accordingly
            print(self.rooms[currentRoom].text)

            user_input = str(input()).split(' ')

            if user_input[0] == "help":
                self.help_user(user_input)
            elif user_input[0]  == "exit" or user_input[0] == "quit":
                break
            elif user_input[0] == "go":
                print("[" + user_input[1] + "]")
                currentRoom = self.navigate(currentRoom, user_input[1])
            else:
                print("I don't understand what you're saying.")



