from pyparsing import *
from room import Room
from engine import Engine
from character import Character
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
    text = restOfLine
    character = (Combine('<' + Word(alphanums) + '>') + Suppress(LPAREN) + 'character' + Suppress(RPAREN + LBRACKET) + OneOrMore(phrase) + Suppress(RBRACKET))
    room = Combine('<' + Word(alphanums) + '>') + Suppress(LPAREN) + ZeroOrMore(neighbor) + Suppress(RPAREN + LBRACKET) + SkipTo("\n") + ZeroOrMore(character) + Suppress(RBRACKET)
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

    # Pull out only the directional info (ex. treasure is south)
    room_directions = [room[1:len(room)-1] for room in rooms_data]

    # We'll be returning the print text and the neighbors array to be used in Engine
    text_and_neighbors = [["", [None, None, None, None]] for i in range(len(rooms_data))]

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

            text_and_neighbors[current_room_id][1][current_direction_index] = next_room_id
            text_and_neighbors[next_room_id][1][next_direction_index] = current_room_id

        # Clean the string some more (remove /n and whitespace at end)
        text_and_neighbors[j][0] = rooms_data[j][len(rooms_data[j])-1].replace('\n', '')

    return text_and_neighbors

# Given parsed character info, build dictionaries for dialogue, return that along with room id, character key
def create_character_dict(character_list):
    character_dict = {}

    for i in range(2, len(character_list[1])):
        character_dict[character_list[1][i][0]] = character_list[1][i][1]
        
    return [character_list[0], character_list[1][0].replace("<", "").replace(">",""), character_dict]


# Create room objects, pass into Engine and run the game!
# rooms_text_and_neighbors ([[string, [int]]]) : list from verify_game_map
def run_game(rooms_text_and_neighbors, characters_info):

    characters = [Character(character[2]) for character in characters_info]
    character_dicts = [{} for i in range(len(rooms_text_and_neighbors))]

    print(len(characters_info))

    for i in range(len(characters_info)):
        character_dicts[characters_info[i][0]][characters_info[i][1]] = characters[i]

    print(character_dicts)
    rooms = [Room(i, rooms_text_and_neighbors[i][1], character_dicts[i], rooms_text_and_neighbors[i][0]) for i in range(len(rooms_text_and_neighbors))]

    game = Engine(rooms, [], characters)
    game.run()


def main():

    args = sys.argv[1:]
    if len(args) == 0:
        print("Please provide a file name when you run this function.")
        exit(-1)
    elif len(args) > 1:
        print("Too many arguments! Please only provide a file name when you run this function.")
        exit(-1)

    # TODO: 
    # Add support for passing in multiple .game files to be compiled into a complete game
    parsed_data = parse_data(args[0])

    split_data = split_into_rooms(parsed_data)

    # Pull out the characters in our parsed data
    characters = []
    for i in range(len(split_data)):
        if split_data[i][1] == 'character':
            characters.append([i-1, split_data[i]])
    
    # Leave only the room data in split_data
    for character in characters:
        split_data.remove(character[1])

    # Make sure the room navigation logic makes sense, get final data out
    rooms_text_and_neighbors = verify_game_map(split_data)

    # Build character dialogue dictionaries, get final data out
    character_room_and_dialogue = []
    for character in characters:
        character_room_and_dialogue.append(create_character_dict(character))

    # Run the game!
    run_game(rooms_text_and_neighbors, character_room_and_dialogue)

if __name__ == "__main__":
    main()
