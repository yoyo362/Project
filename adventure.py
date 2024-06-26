import json
import sys

class TextAdventure:
    def __init__(self, map_file):
        self.map_file = map_file
        self.current_room = None
        self.inventory = []
        self.visited_rooms = []
        self.load_map()

    def load_map(self):
        with open(self.map_file, 'r') as f:
            try:
                game_map = json.load(f)
                self.validate_map(game_map)
                self.rooms = {self.normalize_room_name(room['name']): room for room in game_map['rooms']}
                self.current_room = self.normalize_room_name(game_map['start'])
            except json.JSONDecodeError:
                sys.exit("Invalid JSON format in map file.")
            except KeyError:
                sys.exit("Map file is missing required keys.")

    def validate_map(self, game_map):
        if 'start' not in game_map or 'rooms' not in game_map:
            sys.exit("Map file is missing required keys.")

        room_names = set()
        for room in game_map['rooms']:
            room_name = self.normalize_room_name(room['name'])
            if room_name in room_names:
                sys.exit("Duplicate room names found in map file.")
            room_names.add(room_name)

            exit_rooms = set()
            for exit_direction, exit_room in room['exits'].items():
                exit_room_normalized = self.normalize_room_name(exit_room)
                if exit_room_normalized in exit_rooms:
                    sys.exit(f"Ambiguous exits to '{exit_room}' in room '{room_name}'")
                if exit_room_normalized not in room_names and exit_room_normalized != '':
                    exit_rooms.add(exit_room_normalized)
                else:
                    sys.exit(f"Invalid exit room '{exit_room}' in map file.")

        start_room_normalized = self.normalize_room_name(game_map['start'])
        if start_room_normalized not in room_names:
            sys.exit(f"Invalid start room '{game_map['start']}' in map file.")

    def normalize_room_name(self, room_name):
        return ' '.join(room_name.strip().split())

    def display_room_info(self):
        room = self.rooms[self.current_room]
        print(f"> {room['name'].strip()}\n\n{room['desc']}\n")
        if 'items' in room:
            print("Items:", ', '.join(room['items']))
        print("\nExits:", ', '.join(room['exits']))
        print("\nWhat would you like to do?")

    def process_command(self, command):
        if command == 'look':
            self.display_room_info()
        elif command.startswith('go '):
            self.go(command.split(' ', 1)[1])
        elif command.startswith('get '):
            self.get(command.split(' ', 1)[1])
        elif command.startswith('drop '):
            self.drop(command.split(' ', 1)[1])
        elif command == 'inventory' or command == 'inv':
            self.show_inventory()
        elif command == 'help':
            self.show_help()
        elif command == 'quit':
            print("Goodbye!")
            sys.exit()
        elif command in self.rooms[self.current_room]['exits']:
            self.go(command)
        else:
            print("Invalid command. Type 'help' for a list of commands.")

    def go(self, direction):
        room = self.rooms[self.current_room]
        if direction in room['exits']:
            next_room = self.normalize_room_name(room['exits'][direction])
            if next_room in self.rooms:
                if next_room != self.current_room:
                    if next_room not in self.visited_rooms:
                        self.visited_rooms.append(self.current_room)
                        self.current_room = next_room
                        self.display_room_info()
                    else:
                        print("You've already been in this room. Try another direction or backtrack.")
                else:
                    if self.visited_rooms:
                        prev_room = self.visited_rooms.pop()
                        self.current_room = prev_room
                        self.display_room_info()
                    else:
                        print("You can't go any further in this direction.")
            else:
                print(f"There's no way to go {direction}.")
        else:
            print(f"There's no way to go {direction}.")

    def get(self, item):
        room = self.rooms[self.current_room]
        if 'items' in room and item in room['items']:
            self.inventory.append(item)
            room['items'].remove(item)
            print(f"You pick up the {item}.")
        else:
            print(f"There's no {item} here.")

    def drop(self, item):
        if item in self.inventory:
            room = self.rooms[self.current_room]
            room['items'].append(item)
            self.inventory.remove(item)
            print(f"You drop the {item}.")
        else:
            print(f"You don't have {item} in your inventory.")

    def show_inventory(self):
        if self.inventory:
            print("Inventory:")
            for item in self.inventory:
                print(f"  {item}")
        else:
            print("You're not carrying anything.")

    def show_help(self):
        print("Commands:")
        print("  look: Look around the current room.")
        print("  go [direction]: Move to the room in the specified direction.")
        print("  get [item]: Pick up an item in the current room.")
        print("  drop [item]: Drop an item from your inventory into the current room.")
        print("  inventory: View your inventory.")
        print("  help: Display this help message.")
        print("  quit: Quit the game.")

    def play(self):
        self.display_room_info()
        while True:
            command = input(">> ").lower()
            self.process_command(command)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 adventure.py [map filename]")
    game = TextAdventure(sys.argv[1])
    game.play()