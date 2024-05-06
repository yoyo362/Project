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
                if exit_room_normalized not in room_names:
                    if exit_room_normalized != '':
                        exit_rooms.add(exit_room_normalized)
                    else:
                        sys.exit(f"Invalid exit room '{exit_room}' in map file.")

        start_room_normalized = self.normalize_room_name(game_map['start'])
        if start_room_normalized not in room_names:
            sys.exit(f"Invalid start room '{game_map['start']}' in map file.")

    def normalize_room_name(self, room_name):
        if len(room_name.strip()) == 1:
            return room_name.strip()
        else:
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

    # ... (the rest of the code remains the same)