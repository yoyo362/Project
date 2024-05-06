import json
import sys


class TextAdventure:
    def __init__(self, map_file):
        self.map_file = map_file
        self.current_room = None
        self.inventory = []
        self.visited_rooms = set()
        self.load_map()

    def load_map(self):
        with open(self.map_file, 'r') as f:
            try:
                game_map = json.load(f)
                self.validate_map(game_map)
                self.rooms = {room['name']: room for room in game_map['rooms']}
                self.current_room = game_map['start']
            except json.JSONDecodeError:
                sys.exit("Invalid JSON format in map file.")
            except KeyError:
                sys.exit("Map file is missing required keys.")

    def validate_map(self, game_map):
        if 'start' not in game_map or 'rooms' not in game_map:
            sys.exit("Map file is missing required keys.")

        room_names = set()
        for room in game_map['rooms']:
            room_name = room['name']
            if room_name in room_names:
                sys.exit("Duplicate room names found in map file.")
            room_names.add(room_name)

            for exit_room in room['exits'].values():
                if exit_room not in room_names:
                    sys.exit(f"Invalid exit room '{exit_room}' in map file.")

        if game_map['start'] not in room_names:
            sys.exit(f"Invalid start room '{game_map['start']}' in map file.")

    def move(self, direction):
        if direction in self.rooms[self.current_room]['exits']:
            self.current_room = self.rooms[self.current_room]['exits'][direction]
            self.visited_rooms.add(self.current_room)
            self.print_room_description()
        else:
            print("You can't go that way.")

    def print_room_description(self):
        room = self.rooms[self.current_room]
        print(room['desc'])
        if 'items' in room:
            print("You see the following items in the room:")
            for item in room['items']:
                print(f"- {item}")

    def take_item(self, item_name):
        room = self.rooms[self.current_room]
        if 'items' in room and item_name in room['items']:
            self.inventory.append(item_name)
            room['items'].remove(item_name)
            print(f"You took the {item_name}.")
        else:
            print("There is no such item here.")

    def drop_item(self, item_name):
        if item_name in self.inventory:
            self.inventory.remove(item_name)
            self.rooms[self.current_room].setdefault('items', []).append(item_name)
            print(f"You dropped the {item_name}.")
        else:
            print("You don't have that item.")

    def print_inventory(self):
        if self.inventory:
            print("You are carrying the following items:")
            for item in self.inventory:
                print(f"- {item}")
        else:
            print("You are not carrying any items.")

    def quit_game(self):
        print("Goodbye!")
        sys.exit()


if __name__ == "__main__":
    adventure = TextAdventure("json.map")
    adventure.print_room_description()
    while True:
        command = input("What would you like to do? ").strip().lower()
        if command.startswith("go "):
            direction = command[3:]
            adventure.move(direction)
        elif command.startswith("get ") or command.startswith("take "):
            item_name = command[4:]
            adventure.take_item(item_name)
        elif command.startswith("drop "):
            item_name = command[5:]
            adventure.drop_item(item_name)
        elif command == "inventory":
            adventure.print_inventory()
        elif command == "quit":
            adventure.quit_game()
        else:
            print("Invalid command.")
