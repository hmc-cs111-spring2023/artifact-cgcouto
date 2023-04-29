# PyQuest: A DSL for creating text-based adventure games

Hi there! This is my project for CS 121 : Domain Specific Languages at Harvey Mudd College.


<u>Required Python package: pyparsing (pip install should do the trick)</u>

## Motivation and audience

When I looked at other languages within this space, I found some simple DSLs, many of which are visually-oriented and designed to run in your browser. These are really cool, but to me a truly authentic text-based adventure game must be delivered on the command line! For DSLs that run locally in this space, they were a lot tougher to use, with all the ones I looked at requiring stringing together function calls and handling some/all of the state management yourself. This would not be a great fit for many people who are interested in this domain! 


The core audience for this project is people with little to no coding experience who are interested in text-based adventure games as a medium. One good example is writers: these people want to focus on the quality of the text they're writing and not control flow and state management. I also think that this language would be a good fit for first-time programmers, especially younger ones. When I first learned HTML in eighth grade, I found it super boring. A language like this could fill the same need that HTML did when I was younger - teaching basic nesting, structure, and the importance of syntax.

## DSL overview

My DSL is heavily inspired by HTML with its nesting and options. The most important thing to understand about my DSL is that it is comprised of a set of rooms, where items and characters can live within a room. I used nesting with curly braces to describe this containment behavior. 

Like HTML, rooms, items, and characters are all started with a keyword wrapped in angle brackets <>. This is the term used to reference that thing within the DSL syntax and within the game once it's running (ex. \<shovel> will be an object you use/look/pickup by referring to shovel).

Each core item within the DSL has a number of options that can go with it. These options are wrapped in parentheses (), separated by commas, and can be encoded in any order. All of these options are described below! One important thing to note is that the first option for items and characters must be `item` and `character`, respectively. I thought a lot about whether this was necessary, but I decided in its favor because it makes the code much more readable at a glance.

For rooms, characters, and items, relevant text that gets printed to the terminal goes within curly braces {}. These curly braces also signify nesting, so for a room you'll have the room text followed by any characters and items residing within that room.

You can also attach ASCII images (saved as txt files) to rooms and items! These images print out when a room is entered and when an item is looked at. It's important to keep all your game and txt files within the same folder so my parser can find them all!

My language has basic error-handling on the DSL syntax (more on that in the limitations section) and much more robust error-handling on game logic. For example, my parser can determine when room direction logic is faulty (ex. two rooms definitions have conflicting information on how they neighbor each other, or two rooms both being north of another room). It can also provide custom error messages warning about duplicate definitions and where things that aren't defined are referenced.

Finally, you can pass in multiple files at once to my parser, and it will parse them all and stitch the game together. This is a useful feature, especially for larger games.



### Rooms

OPTIONS


`start` : This is a keyword that signifies which room the player begins Obviously there can only be one room with this option (and the parser will tell you if you messed this up). 

` X is north/south/east/west` : where X is the tag for another room, this encodes which other rooms are neighbors to the current room being encoded. To give an example, let's say that alley is to the east of shop. In my language, you only have to give one direction for the connection to work (alley is east in shop or shop is west in alley), but you can do both if you want.

`end` : This keyword should be used when a room is an end state. End state rooms terminate the game once they are entered. Unlike start, there can be multiple end states within a game.

`image is X` : where X is a txt file (including the extension), this should lead to an ASCII image that prints out when a room is entered and stayed in.

`blocked until X` : where X is an item in your inventory, it signifies that a room cannot be entered from any direction until that item has been used on a door that connects to that room (with the syntax 'use key on west door' in-game, for example).

LINES

Rooms support a single static line of text that prints every time you enter a room or do an action within in. Compared to items and characters, no keyword and colon pair is required here, just the raw text!

### Items
OPTIONS

`item` : Must start the list of options for all items within the language.

`grabbable` : Sets whether an item can be picked up by the player (going into their inventory) or not.

`contains X` : where X is an item in the room, 

`opens X` : where X is an item in the game (not necesarily in the same room), this option encodes how items in your inventory interact positively with items that aren't grabbable (and are fixed to the room they reside in).

`end` : This keyword should be used when an item is an end state. End state items terminate the game once they are picked up (after their pickup message is printed).

`image is X` : where X is a txt file (including the extension), this should lead to an ASCII image that prints out when an item is looked at.

LINES

Items can have up to three lines of text, each corresponding to a different capability of that item. The syntax is structured as keyword : text .

`look` : Defines text that prints out when you look at the item

`pickup` : Defines text that prints out when you pick up at the item (only relevant if the item in question is grabbable)

`use` : Defines text that prints out when you look at the item (only relevant if the item in question opens something)

### Characters

`character` : Must start the list of options for a character within the language.

Characters have no options otherwise!

LINES

To create dialogue options for a character, you provide the keyword and the character's response separated by a colon. 


## Running your game

Once you've followed the rules outlined above and written a game, you can run `parser.py` and pass in your files on the command line. This will automatically parse the game and launch it in the terminal automatically!

Once again, all game files (.game and .txt) need to be stored within the same folder so my parsing and backend can find everything properly.

## How to play

Once you're in the game, there's a whole nother set of commands for interacting with the game space that you've encoded. I've come to realize that the commands within the game are like a mini-DSL. These should be self-explanatory: 

`help` : prints out a list of supported commands

`go X` : where X is a cardinal direction

`ask X about Y` : where X is a character and Y is an character or object

`take X` : where X is an item

`use X on Y` : where X is an object in your inventory and Y is another object

`use X on Y door` : where X is an object in your inventory and Y is a cardinal direction

`look at X` : where X is a character or object

`inventory` : returns contents of player inventory

`exit/quit` : quit the game

## Some examples

With these examples, I want to not only demonstrate the features present in my project, but also the kinds of games and experiences you can create using it!

My first example is a maze game that demonstrates how you can navigate between rooms.

Within the `code` folder, you can run 

```
python parser.py ../examples/maze/maze.game
```

to play this game!

My second example explores how different items and characters work within a single room. 

To run that, start from the `code` folder again and type 

```
python parser.py ../examples/prison/alcatraz.game
```

Finally, my third example flexes all the features of my DSL and game engine in a classic text-based adventure format. Once again, return to the `code` folder and run

```
python parser.py ../examples/dugeon/adventurepart1.game ../examples/dugeon/adventurepart2.game
```
to try it out!

I hope these examples are interesting and helpful!

## Limitations and areas for improvement

Without a doubt, the biggest limitation (and the biggest disappointment in my eyes) relates to my parsing strategy. At the start of the project, I decided to use pyparsing because it was a prominent and well-documented Python parsing library that was intuitive to use. My plan was to use the `setFailAction` function within pyparsing to kick back custom error messages when particular sections didn't pattern-match. However, when it came time to execute this plan (which was the Monday before this project was due) I learned that `setFailAction` wasn't going to work for interior patterns, but only the top-level one being fed into pyparsing's `parse_file` function. When pyparsing can't grasp your syntax, the error looks like this:
```
pyparsing.exceptions.ParseException: Expected '}', found '<'  (at char 479), (line:4, col:5)
```

And this could be worse, because it gives you a line and column number which lets you deduce the section that isn't being parsed properly. But with my audience in mind, this is not a great outcome. If I had another week to work on this project, addressing this would be my first priority, where I would choose another parsing library and follow a more traditional approach for parsing (with more technical grammars and tokens and all that).

In doing this project, I learned that managing control flow and state for these kinds of games is surprisingly hard! There's a lot of things you need to maintain even for simple games in this space. So it shouldn't come as a surprise that there are things that could be expanded/improved about this language. Here's a short list of features that could be added:

* Expanding characters so that they can give and receive items (that gets triggered on certain keywords), also so that they can be looked at with corresponding ASCII images if you wish
* Being able to use multiple items in your inventory on items and doors
* Support for rebinding commands within the game through the DSL (ex. rebinding 'look at' to 'observe')
* An interactive debugging mode that visualizes the room structure and what items/characters live in each room


