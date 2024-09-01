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
        self.rooms = [
            {"name": "Kitchen", "item": ["key"], "description": None},
            {"name": "hallway", "items": ["carpet"], "description": "You are in a grand hallway."},
            {"name": "library", "items": ["scroll"], "description": "This is the castle's library. It contains many ancient tomes and scrolls."},
            {"name": "living room", "items": ["clock"], "description": "This is the living room that's not so living. It's getting late."}
        ]
        self.score = 0
        self.room_connections()

    def room_connections(self):
        for i, room in enumerate(self.rooms):
            if 'exits' not in room:
                room['exits'] = {}
        
        # Connect kitchen with hallway
        if i == 0 and "hallway" in [r["name"] for r in self.rooms]:
            self.rooms[i]["exits"]["north"] = {"room": self.rooms[1]}
            self.rooms[1]["exits"]["south"] = {"room": self.rooms[0]}

        # Connect library to hall and kitchen (since it's a castle)
        elif i == 2:
            for connected_room in [r for r in self.rooms if "hallway" not in r["name"]] + [{"name": "kitchen"}]:
                room_name = connected_room['name']
                direction = 'west' if room_name == "kitchen" else 'east'
                self.rooms[i]["exits"][direction] = {"room": connected_room}

    def randomize_rooms(self):
        for room in self.rooms:
            if 'items' not in room:  # Check if the item is present
                continue

            items = list(room['item'])
            random.shuffle(items)
            room["item"] = items


class Player:
    def __init__(self, game_state):
        self.current_room = None
        self.inventory = []
        self.treasures_found = 0
        self.game_state = game_state
        self.set_current_room(self.game_state.rooms[0])

    def set_current_room(self, room):
        self.current_room = Room(room["name"])
        self.current_room.description = room.get("description", "")
        for direction, connected_room in room['exits'].items():
            self.current_room.add_exit(direction, game_state.rooms[self.game_state.rooms.index(connected_room)])

    def move_to(self, direction):
        if direction in self.current_room.exits:
            next_room_name = list(self.current_room.exits[direction].name)
            for i, room in enumerate(self.game_state.rooms):
                if 'exits' not in room:  # Check if the exit is present
                    continue

                exits = [exit['room'] for exit in room.get('exits', [])]
                if next_room_name == list(exit['room'].name) and direction.lower() in ['north', 'south']:
                    self.set_current_room(room)
                    break
                elif next_room_name == list(self.game_state.rooms[i].get("item", [])[0]):
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
            print(direction + " to the " + game_state.rooms[self.game_state.rooms.index(room)].get('name', ''))


def main():
    while True:
        # Create rooms
        global game_state
        game_state = GameState()
        
        player = Player(game_state)
        
        won_game = False

        while not won_game and True:
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

            if len(player.inventory) >= sum(len(room.get('item', [])) for room in game_state.rooms):
                print(f"Congratulations, you have found all the treasures! You won!")
                won_game = True

        # Randomize rooms
        random.shuffle(game_state.rooms)
        
        global current_room_index  # Make it a global variable so we can access it outside this scope.
        current_room_index = 0
        
        for room in game_state.rooms:
            if 'items' not in room:  
                continue
            
            items = list(room['item'])
            random.shuffle(items)
            room["item"] = items

if __name__ == "__main__":
    main()