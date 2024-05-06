import sys
import json

class AdventureGame:
    def __init__(self, map_file):
        self.load_map(map_file)
        self.current_room = self.start_room

    def load_map(self, map_file):
        with open(map_file, 'r') as f:
            game_map = json.load(f)
        
        self.validate_map(game_map)

        self.start_room = game_map['start']
        self.rooms = {room['name']: room for room in game_map['rooms']}

    def validate_map(self, game_map):
        if 'start' not in game_map or 'rooms' not in game_map:
            sys.exit("Map file is missing required keys.")

        room_names = set()
        for room in game_map['rooms']:
            room_name = room['name']
            if room_name in room_names:
                sys.exit("Duplicate room names found in map file.")
            room_names.add(room_name)

        for room in game_map['rooms']:
            for exit_direction, exit_room in room['exits'].items():
                if exit_room not in room_names:
                    sys.exit(f"Invalid exit room '{exit_room}' in map file from room '{room['name']}'.")

        if game_map['start'] not in room_names:
            sys.exit(f"Invalid start room '{game_map['start']}' in map file.")

    def move(self, direction):
        exit_room = self.current_room['exits'].get(direction)
        if exit_room:
            self.current_room = self.rooms[exit_room]
        else:
            print("You can't go that way.")

    def look(self):
        room = self.current_room
        print(room['name'])
        print(room['desc'])
        print("Exits:", ", ".join(room['exits'].keys()))
        print("Items:", ", ".join(room['items']))

    def get_item(self, item):
        if item in self.current_room['items']:
            print(f"You pick up the {item}.")
            self.current_room['items'].remove(item)
        else:
            print(f"There is no {item} in this room.")

    def inventory(self):
        print("Inventory:", ", ".join(self.current_room['items']))

    def play(self):
        while True:
            command = input("What would you like to do? ").strip().lower()
            if command == 'quit':
                print("Goodbye!")
                break
            elif command == 'look':
                self.look()
            elif command.startswith('go '):
                direction = command[3:]
                self.move(direction)
                self.look()
            elif command.startswith('get '):
                item = command[4:]
                self.get_item(item)
            elif command == 'inventory':
                self.inventory()
            else:
                print("Invalid command.")

if __name__ == "__main__":
    game = AdventureGame("json.map")
    game.play()
