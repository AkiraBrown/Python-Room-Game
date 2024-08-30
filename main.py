import random
class Room:
    def __init__(self, name):
        self.name = name
        self.description = ""
        self.exits = {}
        self.items = []
        

    def add_exit(self, direction, room):
        self.exits[direction] = room

    def add_item(self, item_name):
        self.items.append(item_name)
   

class GameState:
    def __init__(self):
        self.rooms = []
        self.score = 0
    def randomize_rooms(self):
        self.rooms = random.shuffle(self.rooms)


class Player:
    def __init__(self):
        self.current_room = None
        self.inventory = []
        self.treasures_found = 0

    def move_to(self, direction):
        if direction in self.current_room.exits:
            self.current_room = self.current_room.exits[direction]
            print(f"You have moved to the {self.current_room.name} room.")
        else:
            print("You cannot go that way.")

    def take_item(self, item_name):
        for i in range(len(self.current_room.items)):
            if self.current_room.items[i] == item_name and item_name not in self.inventory:
                self.current_room.items.pop(i)
                self.inventory.append(item_name)
                self.treasures_found += 1
                print(f"You have taken the {item_name}.")
        else:
            print("There is no such item.")

    def look(self):
        if self.current_room.description != "":
            print(self.current_room.description)
        for direction, room in self.current_room.exits.items():
            print(direction + " to the " + room.name)

def main():
    #TODO: Try to make this more random in a function
    # Create rooms
    gameMode = GameState()
    kitchen = Room("Kitchen")
    hall = Room("Hallway")
    library = Room("Library")
    # Kitchen exit and item
    kitchen.add_exit("north", hall)
    kitchen.add_item("key")
    # hall exit and item
    hall.description = "You are in a grand hallway."
    hall.add_exit("south", kitchen)
    hall.add_exit("east", library)

    library.description = "This is the castle's library. It contains many ancient tomes and scrolls."
    library.add_item("scroll")
    #HIGHLIGHT Everything below is fine
    # Create player
    player = Player()
    player.current_room = kitchen

    while True:
        print("\nYou are in the", player.current_room.name, "room.")
        if len(player.inventory) > 0:
            print(f"You have {len(player.inventory)} items in your inventory:")
            for item in player.inventory:
                print(item)
        else:
            print("Your inventory is empty.")

        command = input("\nWhat do you want to do? (type 'look', 'move <direction>', or 'take <item_name>') ")

        if command == "quit":
            break

        elif command.startswith('move'):
            direction = command.split()[1]
            player.move_to(direction)

        elif command.startswith("take"):
            item_name = command[5:]
            player.take_item(item_name)

        elif command.lower() == 'look':
            player.look()

if __name__ == "__main__":
    main()