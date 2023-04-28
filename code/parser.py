from pyparsing import *
from room import Room
from engine import Engine
from character import Character
from item import Item
import sys

# Parse the file into an array with the most important elements!
# filename (string) : the absolute or relative path to the file where you've written in my external DSL
def parse_data(filename):
    # Use shorthand for parsing parentheses and brackets
    LBRACKET, RBRACKET = map(Literal, "{}")
    LPAREN, RPAREN = map(Literal, "()")

    # The various pieces that go into my DSL
    neighbor = Combine(Word(alphas) + ' is ' + one_of(['north', 'south', 'east', 'west'])) + Suppress(ZeroOrMore(','))
    phrase = Group(Word(alphas) + Suppress(":") + restOfLine)
    look = Group("look" + Suppress(":") + restOfLine)
    pickup = Group("pickup" + Suppress(":") + restOfLine)
    use = Group("use" + Suppress(":") + restOfLine)
    image = Group('image' + Suppress('is') + Combine(Word(alphanums) + '.' + Word(alphanums)) + Optional(Suppress(',')))
    character = (Combine('<' + Word(alphanums) + '>') + Suppress(LPAREN) + 'character' + Suppress(RPAREN + LBRACKET) + OneOrMore(phrase) + Suppress(RBRACKET))
    blocked = Group('blocked' + Suppress('until') + Word(alphanums) + Optional(Suppress(',')))
    contains = Group('contains' + Word(alphas) + Optional(Suppress(',')))
    opens = Group('opens' + Word(alphas) + Optional(Suppress(',')))
    item = Combine('<' + Word(alphanums) + '>') + Suppress(LPAREN) + 'item' + Optional(Suppress(',')) + Optional('end' + Suppress(',')) + Optional('grabbable' + Optional(Suppress(','))) + Optional(contains) + Optional(opens) + Optional(image) + Suppress(RPAREN + LBRACKET) + Optional(look) + Optional(pickup) + Optional(use) + Suppress(RBRACKET)
    room = (Combine('<' + Word(alphanums) + '>') + Suppress(LPAREN) + Optional("start" + Suppress(",")) + Optional("end" + Suppress(",")) + ZeroOrMore(neighbor) + Optional(blocked) + Optional(image) + Suppress(RPAREN + LBRACKET) + SkipTo("\n") + ZeroOrMore(character) + ZeroOrMore(item) + Suppress(RBRACKET))

    # Combining the pieces together
    game = OneOrMore(room)

    # Should be ordered [room_name, direction(s), room_text, ...]
    parsed_data = game.parse_file(filename)
    return parsed_data

# Clean up and pull out the parsed data into relevant sections
# data ([string]) : raw parser data ordered [room_name, direction(s), room_text, ...]
def split_into_rooms(data): 
    room_tags = []
    for i in range(len(data)):
        # Tell room tags based on whether it's surrounded by angled brackets
        # There's probably a better way to do this...
        if data[i][0] == "<" and data[i][len(data[i])-1] == ">":
            room_tags.append(i)

    # Add the end of the data so we can stop in the for loop below
    room_tags.append(len(data))

    # Pull out the relevant intervals of data for each parsed room tag
    split_data = []
    for j in range(len(room_tags)-1):
        split_data.append(data[room_tags[j]:room_tags[j+1]])   
    return split_data


# Take in parser data split by room tag, verify that the specified game map makes sense, and pull out 
# room text and neighbor info in a way that the implementation can use it
# rooms_data ([[string]]) : parser data organized as [[room_tag, neighbors, room_text], ...]
def verify_game_map(rooms_data):

    # Build dictionary that maps room names (strings) to their int ID's
    room_names_to_ids = {}
    for i in range(len(rooms_data)):
        room_names_to_ids[rooms_data[i][0][1:len(rooms_data[i][0])-1]] = i

    # Find image data if it exists and pull it out of rooms_data
    images_list = [""]*len(rooms_data)

    blocked_list = [[] for i in range(len(rooms_data))]

    for n in range(len(rooms_data)):
        for m in range(len(rooms_data[n])-1):
            if type(rooms_data[n][m]) == list:
                if rooms_data[n][m][0] == 'image':
                    images_list[n] = rooms_data[n][m][1]
                    del rooms_data[n][m]
                elif rooms_data[n][m][0] == 'blocked':
                    blocked_list[n].append(rooms_data[n][m][1])
                    del rooms_data[n][m]


    # Pull out only the directional info (ex. treasure is south)
    room_directions = [room[1:len(room)-1] for room in rooms_data]

    # We'll be returning the print text and the neighbors array to be used in Engine
    text_and_neighbors = [["", [None, None, None, None], "", []] for i in range(len(rooms_data))]

    compass = ['north', 'south', 'east', 'west'] # Different directions
    pairedInds = [1, 0, 3, 2] # Indices of the opposite direction in compass (ex. 1 at index 0 signifies opposite of north is south)
    for j in range(len(rooms_data)):
        for k in range(len(room_directions[j])):
            parsed_direction = room_directions[j][k].split(' ')

            # Obtain the details of the room we're in and the room we're looking to move to
            current_room_id = j
            next_room_id = room_names_to_ids[parsed_direction[0]]
            current_direction_index = compass.index(parsed_direction[2]) 
            next_direction_index = pairedInds[compass.index(parsed_direction[2])] 

            # TODO:
            # Need to check that we're either overwriting a None or the number we're adding
            # is the same as what's already there (otherwise something is wrong with the room logic)
            # Also need to check that we're not adding directions to rooms that don't exist

            text_and_neighbors[current_room_id][1][current_direction_index] = next_room_id
            text_and_neighbors[next_room_id][1][next_direction_index] = current_room_id

        # Clean the string some more (remove /n and whitespace at end)
        text_and_neighbors[j][0] = rooms_data[j][len(rooms_data[j])-1].replace('\n', '').lstrip()
        text_and_neighbors[j][2] = images_list[j]
        text_and_neighbors[j][3] = blocked_list[j]

    return text_and_neighbors


def find_start(rooms_data):
    start = None
    roomNum = 0
    elem = 0
    for i in range(len(rooms_data)):
        for j in range(len(rooms_data[i])):
            if rooms_data[i][j] == 'start':
                if start == None:
                    start = i
                    roomNum = i
                    elem = j
                else:
                    print("ERROR: Cannot have two or more starting rooms!")
                    exit(-1)

    if start != None:
        del rooms_data[roomNum][elem]
    else:
        start = 0
    return start

def find_end(rooms_data, items_data):
    endRooms = [False for i in range(len(rooms_data))]
    endItems = [False for i in range(len(items_data))]
    for i in range(len(rooms_data)):
        for j in range(len(rooms_data[i])):
            if rooms_data[i][j] == 'end':
                endRooms[i] = True
        try:
            rooms_data[i].remove('end')
        finally:
            continue

    for i in range(len(items_data)):
        for j in range(len(items_data[i][1])):
            if items_data[i][1][j] == 'end':
                endItems[i] = True
        try:
            items_data[i][1].remove('end')
        finally:
            continue

    return [endRooms, endItems]


# Given parsed character info, build dictionaries for dialogue, return that along with room id, character key
def create_character_dict(character_list):
    character_dict = {}

    for i in range(2, len(character_list[1])):
        character_dict[character_list[1][i][0]] = character_list[1][i][1].lstrip()
        
    return [character_list[0], character_list[1][0].replace("<", "").replace(">",""), character_dict]

def preprocess_item_info(item_list):
    item = item_list[1]

    # Go through each item and pull out room ID, grabbable or not, contains item or not, look/pickup/use text
        
    grabBool = bool('grabbable' in item)

    inner_lists = [p for p in item if type(p) == list]

    opens_list = []
    contains_list = []
    text_list = ["", "", ""]
    image = ""

    for lst in inner_lists:
        if lst[0] == "opens":
            opens_list.append(lst[1])
        elif lst[0] == "contains":
            contains_list.append(lst[1])
        elif lst[0] == "look":
            text_list[0] = lst[1].lstrip()
        elif lst[0] == "pickup":
            text_list[1] = lst[1].lstrip()
        elif lst[0] == "use":
            text_list[2] = lst[1].lstrip()
        elif lst[0] == "image":
            image = lst[1]

    item_details = [item_list[0], item[0].replace("<", "").replace(">",""),  text_list, grabBool, opens_list, contains_list, image]  # start with room id and item name

    return item_details


# Create room objects, pass into Engine and run the game!
# rooms_text_and_neighbors ([[string, [int]]]) : list from verify_game_map
def run_game(rooms_text_and_neighbors, characters_info, items_info, starting_room, ending_rooms_and_items):

    characters = [Character(character[2]) for character in characters_info]
    character_dicts = [{} for i in range(len(rooms_text_and_neighbors))]

    for i in range(len(characters_info)):
        character_dicts[characters_info[i][0]][characters_info[i][1]] = characters[i]


    items = [Item(items_info[i][1], items_info[i][2][0], items_info[i][2][1], items_info[i][2][2], items_info[i][3], items_info[i][4], items_info[i][5], items_info[i][6], ending_rooms_and_items[1][i]) for i in range(len(items_info))]
    item_dicts = [{} for i in range(len(rooms_text_and_neighbors))]

    for j in range(len(items_info)):
        item_dicts[items_info[j][0]][items_info[j][1]] = items[j]

    # Need to find which items are contained within another item and augment their status accordingly
    # Also need to update status of rooms to blocked/unblocked

    # If no start is provided, default to room 0

    rooms = [Room(i, rooms_text_and_neighbors[i][1], character_dicts[i], item_dicts[i], rooms_text_and_neighbors[i][0], rooms_text_and_neighbors[i][2], rooms_text_and_neighbors[i][3], ending_rooms_and_items[0][i]) for i in range(len(rooms_text_and_neighbors))]

    game = Engine(rooms, items, characters, starting_room)
    game.run()


def main():

    args = sys.argv[1:]
    if len(args) == 0:
        print("Please provide at least one file name when you run this function.")
        exit(-1)

    parsed_data = []
    for file in args:
        parsed_data.append(parse_data(file).asList())

    # If we have multiple files that we've pulled from, need to flatten our data list 
    parsed_data = [data for sublist in parsed_data for data in sublist]

    split_data = split_into_rooms(parsed_data)


    # Pull out the characters and items in our parsed data
    characters = []
    items = []
    lastRoom = -1
    for i in range(len(split_data)):
        if split_data[i][1] == 'character':
            characters.append([lastRoom, split_data[i]])
        elif split_data[i][1] == 'item':
            items.append([lastRoom, split_data[i]])
        else:
            lastRoom += 1
    
    # Leave only the room data in split_data
    for character in characters:
        split_data.remove(character[1])
    for item in items:
        split_data.remove(item[1])

    print(items)

    starting_room = find_start(split_data)

    ending_rooms_and_items = find_end(split_data, items)

    # Make sure the room navigation logic makes sense, get final data out
    rooms_text_and_neighbors = verify_game_map(split_data)

    # Build character dialogue dictionaries, get final data out
    character_room_and_dialogue = []
    for character in characters:
        character_room_and_dialogue.append(create_character_dict(character))

    # Build item name dictionaries for each room, get final data out
    item_room_and_info = []
    for item in items:
        item_room_and_info.append(preprocess_item_info(item))

    print(ending_rooms_and_items)

    # Run the game!
    run_game(rooms_text_and_neighbors, character_room_and_dialogue, item_room_and_info, starting_room, ending_rooms_and_items)

if __name__ == "__main__":
    main()
