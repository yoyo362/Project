Yogesh Kumar Palanivelu                ypalaniv@stevens.edu

## GitHub Repository
Repository URL: https://github.com/yoyo362/Project.git

## Project Description
This project implements a text-based adventure game where players navigate through a textual world using text commands. The game engine allows players to interact with the game world by reading input commands, parsing them, and executing actions accordingly.


### Extensions Implemented
1. **Abbreviations for Verbs, Directions, and Items:**
   - Abbreviated forms of commands are accepted, making gameplay more user-friendly.
   - Abbreviations only work when they are unambiguous.
   - Prefix-based matching is implemented for exits and commands.

2. **A Help Verb:**
   - Implemented a "help" verb to provide players with a list of valid verbs.
   - Help text is dynamically generated from the defined verbs.

3. **Directions Become Verbs:**
   - Implemented the feature where players can use exits as verbs (e.g., typing "east" instead of "go east").
   - Supports abbreviations for unusual exits.



## Testing Approach
To ensure the correctness of the game engine, the following testing approach was adopted:

 **Manual Testing:**
   - Manually tested the game engine with various input commands and scenarios (like providing commands like the directions that are not present and the verbs 
    and abbrevations that are not provided in the code which it should produce an error) to find the bugs and issues. 



## Bugs or Issues
-  While writing the json.load file , I missed to include (f) which produced TypeError for me while running the code. Then I changed it.
   Many Indentation errors were produced in the code while I wrote , which I cleared it after.



## Example of Difficult Issue and Resolution
   In the game, players could use the "go" command to move between rooms, with the command structured as"go[direction]", for example. "go north" would move the player character to the romm in the north direction. Problem arose when players enters commands with incorrect syntax, such as "go" without specifying the direction as said earlier. Due to this the game would crash with index out of range errors or errors produce confusing error messages.

   To change this I modified the process_command method to parse the "go" command and validate its syntax. I checked if the command started with "go" and if it contained a valid direction, as well as without the "go" command valid direction,  as its argument orelse it produced invalid command. Type "help" for a list of commands.



## Hours Spent

Total Hours Spent on the project : Around 36 hours.


## Map File Example
 {
  "start": "start_room",
  "rooms": [
    {
      "name": "start_room",
      "desc": "You are at the beginning of the adventure.",
      "exits": {
        "north": "next_room",
        "east": "drop_room"
      },
      "items": ["key"]
    },
    {
      "name": "next_room",
      "desc": "You've moved to the next area.",
      "exits": {
        "south": "start_room"
      },
      "items": ["torch"]
    },
    {
      "name": "drop_room",
      "desc": "You are in a room with a table.",
      "exits": {
        "west": "start_room"
      },
      "items": ["book"]
    }
  ]
}
The "start_room" includes the "north" exit leading to the "next_room" for the Help Verb extension.
The "start_room" also includes the "east" exit leading to the "drop_room" for the Drop Item extension.
The "next_room" includes the "south" exit leading back to the "start_room" for connectivity.
The "drop_room" includes the "west" exit leading back to the "start_room" for connectivity.
This map file incorporates elements from all three extensions into a single cohesive game world.



## How to Run
1. Clone the repository to your local machine.
2. Navigate to the directory containing the `adventure.py` file.
3. Run the game using the following command:
    python3 adventure.py [map_filename]

