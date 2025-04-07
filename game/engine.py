from .characters import Orc, Elf, Human
from .commands import process_command, help_command, show_regions, show_enemies, show_inventory, use_item
from .world import World
from .items import create_starting_items
from .combat import Combat


class GameEngine:
    """Manages the game loop and user commands."""

    def __init__(self):
        self.running = True
        self.player = None
        self.world = None
        self.in_combat = False
        self.active_combat = None

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

        while True:
            name = input("Enter your character name: ").strip()
            if len(name) > 256:
                print("Name is too long. Please keep your name under 256 characters.")
            elif not name:
                print("You must enter a name.")
            else:
                break

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

            # special case for quit command
            if command == "quit":
                print("Goodbye, traveler!")
                self.running = False
                continue

            # process all other commands through the command processor
            result = process_command(command, self)
            if result:
                print(result)

            # check if player died during command execution
            if not self.player.is_alive():
                print("Game over! Your character has been defeated.")
                self.running = False

    def start_combat(self, enemy_name=None):
        """Start combat with an enemy, either random or specified by name."""
        if enemy_name:
            # find enemy by name
            enemy = self.world.get_enemy_by_name(enemy_name)
            if not enemy:
                return {"error": "No enemy found", "log": [f"No enemy named '{enemy_name}' found."]}
        else:
            # random encounter
            enemy = self.world.encounter_enemy()
            if not enemy:
                return {"error": "No enemy found", "log": ["No enemies to encounter in this region."]}

        # create combat instance
        self.active_combat = Combat(self.player, enemy)
        self.in_combat = True

        # start the combat and return initial state
        return self.active_combat.start_combat()

    def process_combat_action(self, action, item_param=None):
        """Process a player action during combat."""
        if not self.in_combat or not self.active_combat:
            return {"error": "Not in combat", "log": ["You are not in combat."]}

        if action == "use item":
            if isinstance(item_param, int):
                # it's an index
                result = self.active_combat.process_action(action, item_index=item_param)
            else:
                # it's a name (string) or None
                result = self.active_combat.process_action(action, item_name=item_param)
        else:
            result = self.active_combat.process_action(action)

        # check if combat is over
        if not result["active"]:
            self.in_combat = False
            self.active_combat = None

            # handle rewards if player won
            if result.get("victory"):
                reward_msg = self.world.give_reward(self.player)
                if reward_msg:
                    result["log"].append(reward_msg)

        return result

    def get_current_combat_state(self):
        """Get the current state of combat if in combat."""
        if not self.in_combat or not self.active_combat:
            return None
        return self.active_combat.get_combat_state()