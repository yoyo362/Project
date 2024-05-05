import json
import sys

class TextAdventure:
    def __init__(self, map_file):
        self.map_file = map_file
        self.current_room = None
        self.inventory = []
        self.load_map()

    def load_map(self):
        try:
            with open(self.map_file, 'r') as f:
                game_map = json.load(f)
            self.validate_map(game_map)
            self.rooms = {room['name']: room for room in game_map['rooms']}
            self.current_room = game_map['start']
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error loading map file: {e}")
            sys.exit(1)

    def validate_map(self, game_map):
        if 'start' not in game_map or 'rooms' not in game_map:
            raise ValueError("Map file is missing required keys.")

        room_names = set()
        for room in game_map['rooms']:
            if room['name'] in room_names:
                raise ValueError("Duplicate room names found in map file.")
            room_names.add(room['name'])

            for exit_room in room['exits'].values():
                if exit_room not in room_names:
                    raise ValueError(f"Invalid exit room '{exit_room}' in map file.")

            # Check for ambiguous exits
            exit_counts = {}
            for exit_name, exit_room in room['exits'].items():
                exit_counts[exit_room] = exit_counts.get(exit_room, 0) + 1
                if exit_counts[exit_room] > 1:
                    raise ValueError(f"Ambiguous exits to '{exit_room}' in room '{room['name']}'")

    def display_room_info(self):
        room = self.rooms[self.current_room]
        print(f"> {room['name']}\n\n{room['desc']}\n")
        if 'items' in room:
            print("Items:", ', '.join(room['items']))
        print("\nExits:", ', '.join(room['exits']))
        print("\nWhat would you like to do?")

    def process_command(self, command):
        parts = command.lower().split(' ')
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
            self.go(action)
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
            sys.exit(0)
        else:
            print("Invalid command. Type 'help' for a list of commands.")

    def go(self, direction):
        room = self.rooms[self.current_room]
        if 'exits' in room and direction in room['exits']:
            next_room = room['exits'][direction]
            if next_room == self.current_room:
                print("You can't go that way, it leads back to the same room.")
            else:
                self.current_room = next_room
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
            command = input(">> ").strip()
            if command:
                self.process_command(command)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        sys.exit(1)
    game = TextAdventure(sys.argv[1])
    game.play()