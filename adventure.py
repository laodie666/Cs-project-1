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

    menu = ["look", "inventory", "score", "quit", "back"]

    while not p.victory:
        location = w.get_location(p.x, p.y)

        # TODO: ENTER CODE HERE TO PRINT LOCATION DESCRIPTION
        # Depending on whether or not it's been visited before,
        # print either full description (first time visit) or brief description (every subsequent visit)

        print("What to do? \n")
        print("[menu]")
        for action in location.available_actions():
            print(action)
        choice = input("\nEnter action: ")

        if choice == "[menu]":
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ")




    def look(p: Player, w: World):
        for line in w.get_location(p.x, p.y).long_description:
            print(line)

    def go(d:str, p: Player, w: World) -> bool:
        """
        Move the player in the direct, returning True if the move is valid and False if it is not
        """
        current_x = p.x
        current_y = p.y

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
        if 0 > current_x or current_x >= len(w.map[0]) or 0 > current_y or current_y >= len(w.map) or w.map[current_x][current_y] == -1:
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
