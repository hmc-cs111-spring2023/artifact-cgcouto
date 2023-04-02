from room import Room
import string

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
                print("You cannot go that way here.")
        else:
            print("Sorry, you can only go north, south, east, and west.")

        return currentRoom


    def run(self):
        currentRoom = 0
        while True:
            # ask for input, parse it and do stuff accordingly
            print(self.rooms[currentRoom].text)

            user_input = str(input())

            if user_input == "help":
                print("Sorry, can't help you right now") # add better command
            elif user_input  == "exit" or user_input == "quit":
                break
            elif user_input[:2] == "go":
                currentRoom = self.navigate(currentRoom, user_input[3:])
            else:
                print("I don't understand what you're saying.")



