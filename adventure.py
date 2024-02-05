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


def look(player: Player, world: World):
    """
    Print long info about the current player location
    """
    index = world.get_location(player.x, player.y).index

    for description_line in world.get_location(player.x, player.y).long_description:
        print(description_line)

    # check whether there is an interactable or not
    if index in w.interactables:
        # check whether the quest progression needed for this interaction and the needed items are met.
        interactable = w.interactables[index]
        if w.Quests[interactable.required_quest_name].progress == interactable.required_quest_progress \
                and interactable.required_item in p.inventory and index not in w.interacted:
            print()
            print(interactable.Pre_prompt)

    # check whether there is a dialogue here or not and making sure you have not had this dialogue.
    if index in w.dialogues and w.dialogues[index].status == -1:
        print()
        if not (player.x == 5 and player.y == 3) or world.T_card_quest.progress == 2:
            if not (index == 16) or world.Lucky_pen_quest.progress == 3:
                if not (index == 13) or 13 in p.inventory:
                    if not (index == 17) or 17 in p.inventory:
                        print("You can talk to " + w.dialogues[index].target + " here.")

    # check whether there is an item here and print the item name and description here.
    if index in w.items and index not in p.inventory:
        print()
        if world.items[index].name != "T-card" and world.items[index].name != "Lucky Pen" and world.items[
            index].name != "Cheat Sheet":
            print("There is a " + w.items[index].name + " here.")
            if world.items[index].name == "Watering can":
                print("Type <pick up> to pick it up.")
            elif world.items[index].name == "Cat litter shovel":
                print("Type <pick up> to pick it up.")
            elif world.items[index].name == "Happy Meal":
                print("Type <pick up> to pick up your happy meal.")


def go(d: str, player: Player, world: World):
    """
    Move the player in the direct, also take in quest progression into consideration for specific locations
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

    # check validity of destination
    if 0 > current_x or current_x >= len(world.map[0]) or 0 > current_y or current_y >= len(world.map) or \
            world.map[current_y][current_x] == -1:
        print("Invalid direction to go, try again. You can type map to see the map and where you are.")

    # T-card quest location restrictions
    elif current_x == 5 and current_y == 3 and w.T_card_quest.progress < 1:
        print("You don't have a reason to visit Jean, you should probably go to your parent's house for the T-card")
    elif current_x == 6 and current_y == 3 and w.T_card_quest.progress <= 2:
        print("Jean is still at the door, not letting you in.")

    # Cheat sheet quest locaiton restrictions
    elif current_x == 2 and current_y == 1 and w.Cheat_sheet_quest.progress < 1:
        print("You aren't hungry and have no reason to go there.")
    # Can't go to Eric's room before eating at macdonalds.
    elif current_x == 4 and current_y == 0 and w.Cheat_sheet_quest.progress == 0:
        print("You should probably talk to Eric first.")
    elif current_x == 4 and current_y == 0 and w.Cheat_sheet_quest.progress == 1:
        print("Eric is waiting for you at Macdonalds to eat.")
    # failed quest or too early means you cant go to eric room to study
    elif current_x == 4 and current_y == 0 and w.Cheat_sheet_quest.progress == -1:
        print("Eric isn't letting you into his room.")

    # Lucky pen quest location restrictions
    elif current_x == 0 and current_y == 3 and w.Lucky_pen_quest.progress < 1:
        if w.Lucky_pen_quest.progress == -1:
            print("Grandma is not letting you in.")
        else:
            print("Grandma is still waiting for you to explain why you are here. ")

    # valid move
    else:
        p.x = current_x
        p.y = current_y


# return score of all items added up
def score(player: Player, world: World) -> int:
    """
    return score of the player right now
    """
    score = 0
    for item in player.inventory:
        if item in world.items:
            score += world.items[item].score

    return score


# print out the description of the item.
def inspect(world: World, item_position: int):
    """
    inspect the item
    """
    for line in world.items[item_position].description:
        print(line)


def interact(world: World, player: Player):
    """
    interact with the interactable in the current location
    """
    index = world.get_location(player.x, player.y).index
    if index in w.interactables:
        # check whether the quest progression needed for this interaction and the needed items are met.
        interactable = w.interactables[index]
        if w.Quests[interactable.required_quest_name].progress == interactable.required_quest_progress \
                and interactable.required_item in p.inventory and index not in w.interacted:
            interactable.special_action()
            print(interactable.Post_prompt)
            w.interacted.add(index)

            if index == 2:
                print()
                print("You had a long day, time to go rest. ")

            if world.Lucky_pen_quest.progress == 3:
                print()
                print("Good job, now go to the ktichen to talk to Grandma to pick up your lucky pen. ")
        else:
            print("No interactables here")

        if index == 2:
            world.ending_quest.progress += 1

    else:
        print("No interactable here")


def pick_up(world: World, player: Player):
    """
    pick up item in the current location if possible
    """
    index = world.get_location(player.x, player.y).index

    if index in world.items and index not in player.inventory:

        # story quest items can't be picked up, must be obtained by interaction
        if (world.items[index].name != "T-card" and world.items[index].name != "Lucky Pen" and world.items[index].name
                != "Cheat Sheet"):
            player.inventory.append(index)
            if world.items[index].name == "Watering can":
                print("You pick up the *watering can*. It's kind of heavy so good thing your grandma didn't have to do \
                it.")
            elif world.items[index].name == "Cat litter shovel":
                print("You picked up the *litter shovel*.")
            elif world.items[index].name == "Happy Meal":
                print("You picked up your *happy meal*. The toy is some skateboard keychain.")
            return

        print("There is no item to pick up here")


def talk(world: World, player: Player):
    """
    Initiate dialogue at the current position if possible
    """
    index = world.get_location(player.x, player.y).index
    completion = -1
    # check whether there is a dialogue here or not and making sure you have not had this dialogue.
    if index in world.dialogues and world.dialogues[index].status == -1:
        # Jean's dialogue can only be activated when at Jean's door and quest progress is 2
        if index == 5 and world.T_card_quest.progress == 0:
            print("You don't have a reason to visit Jean, you should probably go to your parent's house for the T-card")
            return
        elif index == 5 and world.T_card_quest.progress == 1:
            print("You should probably knock first")
            return

        # Grandma's dialogue at kitchen can only be triggered when quest progress is 3.
        elif index == 16 and world.Lucky_pen_quest.progress < 3:
            print("You should do your grandma's requests first")
            return

        elif index == 13 and 13 not in player.inventory:
            print("You should pick up your happy meal first.")
            return

        elif index == 17 and 17 not in player.inventory:
            print("Finish making your cheat sheet before talking, gotta focus!")

        else:
            # initiate dialogue
            completion = world.dialogues[index].Progress_dialogue()
            if index == 16:
                world.dialogues[index].status = 0
                completion = 0

    # triggers when completing a dialogue REQUIRE HEAVY DEBUGGING
    if completion == 0:
        # Jean talk
        if index == 5:
            world.T_card_quest.progress += 1
        # Eric talk
        if index == 14:
            world.Cheat_sheet_quest.progress += 1
        # Grandma talk
        if index == 8:
            world.Lucky_pen_quest.progress += 1
        # Finish T-card
        if index == 6 and world.T_card_quest.progress == 3:
            world.T_card_quest.progress += 1
            player.inventory.append(6)
        # Finish Lucky pen
        if index == 16 and world.Lucky_pen_quest.progress == 3:
            world.Lucky_pen_quest.progress += 1
            player.inventory.append(16)

    if completion == 1:
        print("Quest failed")

        if index == 5:
            world.T_card_quest.progress = -1
        if index == 8:
            world.Lucky_pen_quest.progress = -1
        if index == 14:
            world.Cheat_sheet_quest.progress = -1

    else:
        print("There is no one to talk to here.")


def debug(p: Player, w: World):
    """
    debug current state of the game returnes relevant info
    """
    print("Player index")
    print(w.get_location(p.x, p.y).index)
    print("Player location")
    print(str(p.x) + " " + str(p.y))
    print("Quests")
    print(w.T_card_quest.name + " " + str(w.T_card_quest.progress))
    print(w.Cheat_sheet_quest.name + " " + str(w.Cheat_sheet_quest.progress))
    print(w.Lucky_pen_quest.name + " " + str(w.Lucky_pen_quest.progress))
    print("Visted")
    print(w.get_location(p.x, p.y).visited)
    print("Inventory")
    print(p.inventory)
    if w.get_location(p.x, p.y).index in w.dialogues:
        print("there is dialogue")
        print("status: " + str(w.dialogues[w.get_location(p.x, p.y).index].status))


def look_up(world: World, index: int):
    """
    look up the location name given the index
    """
    print(world.locations[index].name)


# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":

    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = w.p

    step_counter = 0

    did_quit = False

    print("You're back at your dorm at U of T, your visit back home to Markham to see your grandparents is over. ")
    print("Back to the school mindset. What did you have to do again?")
    print(" OH RIGHT! You have an exam tomorrow, but wait...")
    print("Where is your T-card, you need that to get in.")
    print("And you didn't study so you have no cheat sheet.")
    print("And where is your lucky pen?")
    print("Okay so where to start:")
    print(
        "Your mom took your T-card because her friend wouldn't believe you got into U of T while you were in Markham.")
    print("You can make a cheat sheet with your friend Eric back in Markham.")
    print("And you were studying at your grandparents so your pen must be there.")
    print("Time gather the items!")
    print()

    print(
        "There is a 60 step count limit in this game, moving, talking, picking up items, and interacting all cost 1 \
        step")
    print("If the game is not completed before 60 steps, you get a bad ending.")
    print()

    while not w.ending_quest.progress == 2:
        location = w.get_location(p.x, p.y)

        print()

        if not location.visited:
            look(p, w)

            # Arriving at parent house increase progress by 1
            if p.x == 4 and p.y == 2 and not w.get_location(p.x, p.y).visited:
                w.T_card_quest.progress += 1

            w.get_location(p.x, p.y).visited = True

        # short description, and showing what is there.
        else:
            print(location.short_description)
            index = location.index
            print()
            # check whether there is an interactable or not
            if index in w.interactables:
                # check whether the quest progression needed for this interaction is met.
                interactable = w.interactables[index]
                if w.Quests[
                    interactable.required_quest_name].progress == interactable.required_quest_progress and index not in\
                        w.interacted:

                    print("This location can be interacted, type <interact> to interact.")

            # check whether there is a dialogue here or not and making sure you have not had this dialogue.
            if index in w.dialogues and w.dialogues[index].status == -1:
                if not (p.x == 5 and p.y == 3) or w.T_card_quest.progress == 2:
                    if not (index == 16) or w.Lucky_pen_quest.progress == 3:
                        if not (index == 13) or 13 in p.inventory:
                            if not (index == 17) or 17 in p.inventory:
                                print("You can talk to " + w.dialogues[index].target + " here.")

            # check whether there is an item here to pick up.
            if index in w.items and index not in p.inventory:
                if (w.items[index].name != "T-card" and w.items[index].name != "Lucky Pen" and w.items[index].name !=
                        "Cheat Sheet"):
                    print("There is an item here to be picked up")

        # Depending on whether it's been visited before,
        # print either full description (first time visit) or brief description (every subsequent visit)
        print()
        print("What to do? \n")
        print("type help to see all possible actions")
        print("type actions to see all the available actions at this location again")
        choice = input("\nEnter action: ")
        print()

        if choice == "help":
            menu = ["map: print out the map and where you currently are",
                    "look up: look up the name of the location at an index on the map"
                    "go: to go in one of the four directions, north, south, east, west",
                    "look: obtain the long description of the location",
                    "inventory: check your own inverntory",
                    "inspect: inspect *insert item* to see their description"
                    "score: check your current store based on the items you own",
                    "quit: quit the game",
                    "interact: interact with whatever is in the current location",
                    "talk: talk to whoever is available to talk in the current location",
                    "pick up: pick up the item at the ccurrent location"
                    ]

            for commands in menu:
                print(commands)

        if choice == "actions":
            for action in w.available_actions(p.x, p.y):
                print(action)

        elif choice == "map":
            for line in w.map:
                print(line)

            print("You are at " + w.get_location(p.x, p.y).name + ", index of " + str(w.get_location(p.x, p.y).index))

        elif choice == "look":
            look(p, w)

        elif "go" in choice:
            if len(choice.split(" ")) == 2:
                go(choice.split(" ")[1], p, w)
                step_counter += 1
            else:
                print(
                    "Wrong number of words after go, remember to keep it to only being go north, go south, go east, go\
                     west")

        elif choice == "score":
            print(score(p, w))

        elif choice == "inventory":
            for item in p.inventory:
                if item != -1:
                    print(w.items[item].name)

            if len(p.inventory) == 1:
                print("You have no item right now.")

        elif "inspect" in choice:
            if len(choice.split(" ")) != 1:
                item_name = choice.split(" ")[1]
                item_index = -1
                for index in w.items:
                    if w.items[index].name == item_name:
                        item_index = index
                        break

                if item_index not in p.inventory:
                    print("Item not found in inventory")

                else:
                    inspect(w, item_index)
            else:
                print("Empty string after inspect, remember to put a item name after inspect.")

        elif choice == "quit":

            did_quit = True
            break

        elif choice == "interact":
            interact(w, p)
            step_counter += 1

        elif choice == "pick up":
            pick_up(w, p)
            step_counter += 1

        elif choice == "talk":
            talk(w, p)
            step_counter += 1

        elif "look up" in choice:
            if len(choice.split(" ")) <= 2 or not choice.split(" ")[2].isnumeric():
                print("invalid index, remember to type in a valid index on the map after look up")
            else:
                look_up(w, int(choice.split(" ")[2]))

        elif choice == "debug":
            debug(p, w)

        else:
            print("invalid input, try again")

        if step_counter == 40:
            print("20 steps left")

        if step_counter == 50:
            print("10 steps left")

        if step_counter == 55:
            print("5 steps left")

        if step_counter >= 60:
            print(
                "It is too late outsie and you have yet to go sleep, you are unable to get enough sleep before the \
                exam.")
            print("As you are going back to your dorm, you are so tired you fell onto the road, and lost conciousness")
            print(
                "You woke up again at a hospital, realizing you have missed your exam and there is no retest, it is \
                what it is.")

            print("game over")

    if did_quit:
        print("game quit")

    elif step_counter < 60:
        score = score(p, w)
        if score == 100:
            print(
                "You got everything you need :)! You we're able to get good sleep in the night and complete the exam \
                smoothly.")
            print("Your final mark was 100%!")
        elif score == 83:
            print(
                "Without your lucky pen, you were tossing and turning in your sleep. You overslept your alarm and got \
                to the exam room late.")
            print("Nonetheless, with the cheat sheet and t-card, you got a 83% on the exam. You passed!")
        elif score == 65:
            print("You didn't have your t-card for the exam and so you had a 35% deduction on the exam.")
            print("Even so, you were otherwise fully prepared meaning you earned the other 65%. You passed!")
        elif score == 52:
            print("You didn't have your cheat sheet for the exam. You were in a good mindset but not well studied.")
            print("You barely passed with a 52%.")
        elif score == 48:
            print(
                "You only had a cheat sheet for the exam. You didn't pass but your studying paied off and you got a \
                48%.")
        elif score == 17:
            print(
                "You only had your lucky pen for the exam. You didn't pass but you had passion during the exam and you \
                got a 17%.")
        elif score == 35:
            print(
                "You only had your t card for the exam. You didn't pass but you earned all the marks you could and you \
                got a 35%.")
        elif score == 0:
            print(
                "You went to Markham and came home empty handed. You went to bed hopeful. But on the exam you earned a \
                devistating 0%.")
            print(
                "You took too long, the day is over. You won't make it in time for the exam. At least they drop one \
                mark.")

    print("Game Over, thank you for playing!")

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['hashlib', 'game_data'],
    })
