"""CSC111 Project 1: Text Adventure Game

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""

# Note: You may add in other import statements here as needed
from game_data import World, Item, Location, Player

# Note: You may add helper functions, classes, etc. here as needed

# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(3, 7)  # set starting location of player; you may change the x, y coordinates here as appropriate



    while not p.victory:
        location = w.get_location(p.x, p.y)

        # TODO: ENTER CODE HERE TO PRINT LOCATION DESCRIPTION
        # Depending on whether or not it's been visited before,
        # print either full description (first time visit) or brief description (every subsequent visit)
        print()
        print("What to do? \n")
        print("Available actions:")
        for action in w.available_actions(p.x, p.y):
            print(action)
        print("type help to see all possible actions")
        print("type actions to see all the available actions at this location again")
        choice = input("\nEnter action: ")

        if choice == "help":
            menu = ["map: print out the map and where you currently are"
                    "go: to go in one of the four directions, north, south, east, west",
                    "look: obtain the long description of the location",
                    "inventory: check your own inverntory",
                    "score: check your current store based on the items you own",
                    "quit: quit the game",
                    "save: save the current game state into a save slot",
                    "load: load the game state from a save slot",
                    "interact: interact with whatever is in the current location",
                    "talk: talk to whoever is available to talk in the current location",
                    "pick up: pick up the item at the ccurrent location"
                    ]

            for commands in menu:
                print(commands)

            continue

        if choice == "actions":
            for action in w.available_actions(p.x, p.y):
                print(action)

            continue

        if choice == "map":
            for line in w.map:
                print(line)

            print("You are at " + w.get_location(p.x, p.y).name + ", index of " + str(w.get_location(p.x, p.y).index))

            continue

    def look(player: Player, world: World):
        for line in world.get_location(player.x, player.y).long_description:
            print(line)

    def go(d: str, player: Player, world: World) -> bool:
        """
        Move the player in the direct, returning True if the move is valid and False if it is not
        """
        current_x = player.x
        current_y = player.y

        # Check direction to go
        if d == 'north':
            current_y -= 1
        elif d == 'south':
            current_y += 1
        elif d == 'east':
            current_x += 1
        elif d == 'west':
            current_x -= 1
        else:
            print("Invalid direction input, either type in north, south, east, or west")
            return False

        # check validity of destination
        if 0 > current_x or current_x >= len(world.map[0]) or 0 > current_y or current_y >= len(world.map) or world.map[current_x][current_y] == -1:
            print("Invalid direction to go, try again")
            return True
        return False


        # TODO: CALL A FUNCTION HERE TO HANDLE WHAT HAPPENS UPON THE PLAYER'S CHOICE
        #  REMEMBER: the location = w.get_location(p.x, p.y) at the top of this loop will update the location if
        #  the choice the player made was just a movement, so only updating player's position is enough to change the
        #  location to the next appropriate location
        #  Possibilities:
        #  A helper function such as do_action(w, p, location, choice)
        #  OR A method in World class w.do_action(p, location, choice)
        #  OR Check what type of action it is, then modify only player or location accordingly
        #  OR Method in Player class for move or updating inventory
        #  OR Method in Location class for updating location item info, or other location data etc....
