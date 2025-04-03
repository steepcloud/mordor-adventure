from .characters import Orc, Elf, Human
from .commands import process_command, help_command, show_regions, show_enemies, show_inventory, use_item
from .world import World
from .items import create_starting_items


class GameEngine:
    """Manages the game loop and user commands."""

    def __init__(self):
        self.running = True
        self.player = None
        self.world = None

    def start_game(self):
        """Initialize the game and start the main game loop."""
        self._setup_player()
        self._give_starting_items()
        
        print(f"You are {self.player.name}, {self.player.description}")
        print(f"You've been equipped with {len(self.player.inventory)} starter items.")
        print("Type 'help' for commands.")

        self.world = World(self.player)
        self.game_loop()

    def _setup_player(self):
        """Create the player character based on user input."""
        print("Welcome to the Lands of Mordor!")
        name = input("Enter your character name: ")
        race = input("Choose your race (Orc, Elf, Human): ").strip().lower()

        if race == "orc":
            self.player = Orc(name)
        elif race == "elf":
            self.player = Elf(name)
        elif race == "human":
            self.player = Human(name)
        else:
            print("Invalid race. Defaulting to Human.")
            self.player = Human(name)

    def _give_starting_items(self):
        """Give the player their starting inventory items."""
        starting_items = create_starting_items()
        for item in starting_items:
            self.player.add_item(item)

    def game_loop(self):
        """Main game loop that processes player commands."""
        while self.running and self.player.is_alive():
            command = input("\n> ").strip().lower()
            
            # Special case for quit command
            if command == "quit":
                print("Goodbye, traveler!")
                self.running = False
                continue
                
            # Process all other commands through the command processor
            result = process_command(command, self)
            
            # Check if player died during command execution
            if not self.player.is_alive():
                print("Game over! Your character has been defeated.")
                self.running = False