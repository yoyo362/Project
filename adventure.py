import json
import sys

class TextAdventure:
    def __init__(self, map_file):
        self.map_file = map_file
        self.current_room = None
        self.inventory = []
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
            if room['name'] in room_names:
                sys.exit("Duplicate room names found in map file.")
            room_names.add(room['name'])

        for room in game_map['rooms']:
            for exit_room in room['exits'].values():
                if exit_room not in room_names:
                    sys.exit(f"Invalid exit room '{exit_room}' in map file.")

    def display_room_info(self):
        room = self.rooms[self.current_room]
        print(f"> {room['name']}\n\n{room['desc']}\n")
        if 'items' in room:
            print("Items:", ', '.join(room['items']))
        print("\nExits:", ', '.join(room['exits']))
        print("\nWhat would you like to do?")

    def process_command(self, command):
        parts = command.split(' ')
        action = parts[0]

        if action == 'start':
            self.play()
        elif action == 'look':
            self.display_room_info()
        elif action == 'go':
            if len(parts) > 1:
                direction = ' '.join(parts[1:])
                self.go(direction)
            else:
                print("Please specify a direction.")
        elif action in ['north', 'south', 'east', 'west']:
            self.go(action)  # Call go method directly with the direction
        elif action == 'get':
            if len(parts) > 1:
                item = ' '.join(parts[1:])
                self.get(item)
            else:
                print("Please specify an item to get.")
        elif action == 'inventory' or action == 'inv':
            self.show_inventory()
        elif action == 'help':
            self.show_help()
        elif action == 'quit':
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid command. Type 'help' for a list of commands.")

    def go(self, direction):
        room = self.rooms[self.current_room]
        if direction in room['exits']:
            self.current_room = room['exits'][direction]
            self.display_room_info()
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
        print("  inventory: View your inventory.")
        print("  help: Display this help message.")
        print("  quit: Quit the game.")

    def play(self):
        self.display_room_info()
        while True:
            command = input(">> ")
            self.process_command(command)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 adventure.py [map filename]")
    game = TextAdventure(sys.argv[1])
    game.play()
