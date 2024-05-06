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
                sys.exit(f"Duplicate room names found in map file: '{room_name}'")
            room_names.add(room_name)

            exit_rooms = set()
            for exit_direction, exit_room in room['exits'].items():
                exit_room_normalized = self.normalize_room_name(exit_room)
                if exit_room_normalized in exit_rooms:
                    sys.exit(f"Ambiguous exits to '{exit_room}' in room '{room_name}'")
                if exit_room_normalized not in room_names:
                    sys.exit(f"Invalid exit room '{exit_room}' in map file for room '{room_name}'.")
                exit_rooms.add(exit_room_normalized)

        start_room_normalized = self.normalize_room_name(game_map['start'])
        if start_room_normalized not in room_names:
            sys.exit(f"Invalid start room '{game_map['start']}' in map file.")

    def normalize_room_name(self, room_name):
        return ' '.join(room_name.strip().split())

    # Rest of the code remains the same (display_room_info, process_command, etc.)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 adventure.py [map filename]")
    game = TextAdventure(sys.argv[1])
    game.play()
