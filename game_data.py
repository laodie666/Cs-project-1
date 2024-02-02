"""CSC111 Project 1: Text Adventure Game Classes

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
import typing
from typing import Optional, TextIO

class Quest:

    """
     Instance Attributes:
        - name: name of location
        - progress: int storing the progress of the quest, 0 being not started.

    Representation Invariants:
        - self.name != ''
    """
    def __init__(self, name: str) -> None:
        """
        Initialize a new Quest. with name, and progress starting as 0
        """
        self.name = name
        self.progress = 0


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - # TODO

    Representation Invariants:
        - # TODO
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        # NOTES:
        # This is a suggested starter class for Player.
        # You may change these parameters and the data available for the Player object as you see fit.

        self.x = x
        self.y = y

        # The inverntroy stores the location at which the itemis found rather than the item name to use the dictionary
        # -1 for placeholder quests that doesn't need an item.
        self.inventory = [-1]



class Interaction:
    """Possible interactions in the adventure game world.

    Instance Attributes:
        - Pre_prompt: The prompt that is provided before interacted
        - Post_prompt: The prompt that is provided when interacted
        - Required_quest_name: name of required quest initiate as 'no_quest' without input
        - Required_quest_progress: needed progress number for the interaction, initiate as 0 without input
        - Required_item: position of the item needed, initiate as -1 without input


    Representation Invariants:
        - # TODO
    """
    def __init__(self, Pre_prompt:[str], Post_prompt: [str], required_quest_name = 'no_quest', required_quest_progress = 0, required_item = -1) -> None:
        """
        Initialize a new interaction. with location, required quest name, required quest progress, and required item
        """

        self.required_quest_name = required_quest_name
        self.required_quest_progress: required_quest_progress
        self.required_item = required_item
        self.Post_prompt = Post_prompt
        self.Pre_prompt = Pre_prompt

    def special_action(self):
        raise NotImplementedError

class Quest_progress_Interaction (Interaction):
    """
    inherit Interaction but change speciaal_action to increase quest progress
    """

    def __init__(self, Pre_prompt: [str], Post_prompt: [str], quest: Quest, required_quest_name = 'no_quest', required_quest_progress = 0, required_item = -1) -> None:
        """
        Initialize a new interaction. with location, required quest name, required quest progress, required item, and the quest to update
        """
        super().__init__(Pre_prompt, Post_prompt, required_quest_name, required_quest_progress, required_item)
        self.quest = quest
    def special_action(self):
        self.quest.progress += 1

class Teleport_Interaction (Interaction):
    """
    inherit Interaction but change speciaal_action to increase quest progress
    """
    def __init__(self, Pre_prompt: [str], Post_prompt: [str], player: Player, required_quest_name = 'no_quest', required_quest_progress = 0, required_item = -1) -> None:
        """
        Initialize a new interaction. with location, required quest name, required quest progress, required item, and the quest to update
        """
        super().__init__(Pre_prompt, Post_prompt, required_quest_name, required_quest_progress, required_item)
        self.player = player

    def special_action(self):
        if self.player.x == 3 and self.player.y == 6:
            self.player.y = 4
        elif self.player.x == 3 and self.player.y == 4:
            self.player.y = 6


class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - name: name of location
        - short_description: short description in a string.
        - long_description: long description with each line stored in a list.
        - visited: whether or not a location is visited already
        - index: index of the location on the map

    Representation Invariants:
        - # TODO
    """

    def __init__(self, name: str, short_description: str, long_description: list[str], visited = False, index = -1) -> None:
        """
        Initialize a new location. with name, short description, and long description
        """

        # NOTES:
        # Data that could be associated with each Location object:
        # a position in the world map,
        # a brief description,
        # a long description,
        # a list of available commands/directions to move,
        # items that are available in the location,
        # and whether the location has been visited before.
        # Store these as you see fit, using appropriate data types.
        #
        # This is just a suggested starter class for Location.
        # You may change/add parameters and the data available for each Location object as you see fit.
        #
        # The only thing you must NOT change is the name of this class: Location.
        # All locations in your game MUST be represented as an instance of this class.

        self.name = name
        self.short_description = short_description
        self.long_description = long_description
        self.visited = visited
        self.index = index


class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: name
        - description: description of the item

    Representation Invariants:
        - # TODO
    """

    def __init__(self, name: str, score:int, description: list[str]) -> None:
        """
        Initialize a new item, with name and description.
        """

        # NOTES:
        # This is just a suggested starter class for Item.
        # You may change these parameters and the data available for each Item object as you see fit.
        # (The current parameters correspond to the example in the handout).
        # Consider every method in this Item class as a "suggested method".
        #
        # The only thing you must NOT change is the name of this class: Item.
        # All item objects in your game MUST be represented as an instance of this class.

        self.name = name
        self.score = score
        self.description = description

class Dialogue:
    """ Dialogue stored in recursive Structure

    Instance Attributes:
        - target: who is talking
        - content: content of the dialogue
        - future_dialogue: further dialogue options in a dictionary
        - status: status of dialogue, -1 being not started, 0 being completed, 1 being failed

    Representation Invariants:
        - # TODO

    """

    def __init__(self, target: str, content: str, future_dialogue = None, status = -1) -> None:
        """
        Content cant be empty as dialogue need content
        If there is no future dialogue it is defaulted as None
        name is defaulted as none as not all dialogue are important and require name
        """
        self.target = target
        self.content = content
        self.future_dialogue = future_dialogue
        self.status = status


    def Progress_dialogue(self):
        """
        method to proprogate through an entire dialogue tree
        The status of the dialogue will be dependent on which end of the dialogue tree the player has arrived, which will be passed back up to the top.
        """

        if self.future_dialogue is not None:
            # if there is only one option then the player doesn't have to choose
            if len(self.future_dialogue) == 1:
                # print own content
                print(self.content)
                # pass in status and go into the next iteration
                self.status  = self.future_dialogue[-1].Progress_dialogue()
                return self.status

           # player has to choose
            else:
                # print own content
                print(self.content)

                # print available options
                for choice in self.future_dialogue:
                    type(choice)
                    print(str(choice) + ")" + self.future_dialogue[choice].content)

                #take input then proceed in that direction while passing up the status
                user_choice = input("select option")
                self.status = self.future_dialogue[int(user_choice)].Progress_dialogue()
                return self.status

        else:
            print(self.content)
            print("Dialogue ends")
            return self.status

class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - # TODO add more instance attributes as needed; do NOT remove the map attribute

    Representation Invariants:
        - Two interact can not be in the same location
        - Two items can not be in the same location
    """

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """

        # NOTES:

        # map_data should refer to an open text file containing map data in a grid format, with integers separated by a
        # space, representing each location, as described in the project handout. Each integer represents a different
        # location, and -1 represents an invalid, inaccessible space.

        # You may ADD parameters/attributes/methods to this class as you see fit.
        # BUT DO NOT RENAME OR REMOVE ANY EXISTING METHODS/ATTRIBUTES IN THIS CLASS

        # The map MUST be stored in a nested list as described in the load_map() function's docstring below
        self.map = self.load_map(map_data)

        # NOTE: You may choose how to store location and item data; create your own World methods to handle these
        # accordingly. The only requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.
        self.locations = self.load_locations(location_data)

        self.items = self.load_items(items_data)

        # Entering parent house increase progress by 1: can only knock Jean's door with progress 1
        # Finish talking to Jean increase progress by 1: can only go into Jean's living room with progress 2
        # If the mean dialogue option is picked when talking to Jean, the quest progress go to -1 and the quest ends.
        # Finish talking to Mom to end the quest: obtain T-card
        self.T_card_quest = Quest("T_card_quest")

        # Talking to Eric increase progress by 1: can only go to macdonalds if progress is 1.
        # Picking the "make me cheat sheet" dialogue will result in quest failure
        # Interact at macdonalds to eat increase progress by 1: Can only go back to Eric's house is 2
        # Interact at Eric's house at progress 2 of the house ends the quest, and obtain the cheat sheet.
        self.Cheat_sheet_quest = Quest("Cheat_sheet_quest")


        # Talking to Grandma increase progress by 1: can only go into Grandma living room if progress is 1
        # Failing the dialogue option with Grandma fail the quest. make progress go -1
        # Watering the plant with watering can increase progress by 1
        # Scoop cat poop with cat litter shovel increase progress by 1: Can only talk to Grandma at progress 3
        # Taking to Gradnma at progress three ends the quest, results in you getting the lucky pen.
        self.Lucky_pen_quest = Quest("Lucky_pen_quest")

        # Place holder quest for interactions that doesn't require a quest active.
        self.no_quest = Quest("no_quest")

        # Ending quest, start with 0 and end with 1 being when you return from Markham, and 2 being after player goes to sleep
        self.ending_quest = Quest("ending_quest")

        # store all quests in  dictionary for easy access.
        self.Quests = {"Cheat_sheet_quest": self.Cheat_sheet_quest, "T_card_quest": self.T_card_quest, "Lucky_pen_quest": self.Lucky_pen_quest, "no_quest": self.no_quest, "ending_quest": self.ending_quest}


        # TODO: dialogue

        #Interactions

        self.go_markham = Teleport_Interaction()

        # lists of interactable locations in form of location: interactable
        self.interactables = {}

        # Dialogues

        j7 = Dialogue("Jean", "Of course, did you come back just for my birthday, your mom is here too. Lovely surprise :)!", status = 0)
        j6 = Dialogue("Jean", "Wow, I almost thought you were here for my birthday. Yeah, your mom is right here.", status = 0)
        j5 = Dialogue("Jean", "Where are your manners!? Go back to school!", status = 1)
        j4 = Dialogue("You", "Happy Birthday Aunt Jean! Can I come in?",  {-1: j7})
        j3 = Dialogue("You", "Hi Aunt Jean, have you seen my mom?",  {-1: j6})
        j2 = Dialogue("You", "I don’t have time for you right now, let me in.",  {-1: j5})
        j1 = Dialogue("Jean", "Hel- OH, it's you, aren’t you supposed to be at school right now? What are you doing here?",  {1: j2, 2: j3, 3:j4})


        # TODO: finish rest of dialogue

        # lists of dialogues in form of location: dialogue
        self.dialogues = {5: j1}



    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        """
        lines = [line.strip() for line in map_data]
        return [[int(place) for place in line.split(" ")] for line in lines]

    def load_locations(self, location_data: TextIO) -> dict[int: Location]:
        """
        Store locations from location file into format like this for each location:

        {position: [name, short description, long descriptions]}

        Return this dictionary representation of the location, its index, its short and long description.
        """
        locations = {}
        counter = 0
        lines = [line.strip() for line in location_data]
        name = ''
        position = -1
        short_description = ''
        long_description = []
        for line in lines:
            # next location
            if line == "END":
                locations[position] = Location(name, short_description, long_description, index = position)
                counter = 0
                position = -1
                name = ''
                short_description = ''
                long_description = []
                continue

            # name
            if counter == 0:
                name = line

            # index
            elif counter == 1:
                position = int(line)

            # short description
            elif counter == 2:
                short_description = line

            else:
                long_description.append(line)

            counter += 1

        return locations

    def load_items(self, items_data: TextIO) -> dict[int: list[str]]:
        """
        Store items from item file into format like this for each item:

        {position: [name, description]}

        Return this dictionary representation of the name, its location, and description.
        """

        lines = [line.strip() for line in items_data]
        counter = 0
        description = []
        name = ''
        position = -1
        score = -1
        items = {}
        for line in lines:
            if line == "END":
                counter = 0
                items[position] = Item(name, score, description)
                name = ''
                description = []
                position = -1
                score = -1
                continue

            if counter == 0:
                name = line

            elif counter == 1:
                position = int(line)
            elif counter == 2:
                score = int(line)
            else:
                description.append(line)

            counter += 1

        return items

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """

        if 0 > x  or  x >= len(self.map[0]) or 0 > y or y >= len(self.map) or self.map[y][x] == -1:
            return None
        else:
            return self.locations[self.map[y][x]]

    def available_actions(self, x, y):
        """
        Return the available actions in this location.

        """

        menu = ["map: print out the map and where you currently are"
                "go: to go in one of the four directions, north, south, east, west",
                "look: obtain the long description of the location",
                "inventory: check your own inverntory",
                "score: check your current store based on the items you own",
                "quit: quit the game",
                "save: save the current game state into a save slot",
                "load: load the game state from a save slot",
                ]



        index = self.get_location(x, y)
        if index in self.items:
            menu.append("pick up: pick up the item at the ccurrent location")

        if index in self.interactables:
            menu.append("interact: interact with whatever is in the current location")

        if index in self.dialogues:
            menu.append("talk: talk to whoever is available to talk in the current location")

        return menu


def test_world() -> World:
    map_data = open("map.txt", "r")
    location_data = open("locations.txt", "r")
    items_data = open("items.txt", "r")
    return World(map_data, location_data, items_data)
