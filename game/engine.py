from .characters import Orc, Elf, Human
from .commands import examine, attack, help_command
from .world import World
from .combat import Combat
from .items import create_starting_items


class GameEngine:
    """Manages the game loop and user commands."""

    def __init__(self):
        self.running = True
        self.player = None
        self.world = None

    def start_game(self):
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

        # Give the player some starting items
        starting_items = create_starting_items()
        for item in starting_items:
            self.player.add_item(item)

        print(f"You are {self.player.name}, {self.player.description}")
        print(f"You've been equipped with {len(starting_items)} starter items.")
        print("Type 'help' for commands.")

        self.world = World(self.player)

        self.game_loop()

    def game_loop(self):
        while self.running and self.player.is_alive():
            command = input("\n> ").strip().lower().split()
            if not command:
                continue

            verb = command[0]
            noun = ' '.join(command[1:]) if len(command) > 1 else None

            if verb == "quit":
                print("Goodbye, traveler!")
                self.running = False

            elif verb == "help":
                print(help_command())

            elif verb == "regions":
                self.show_regions()

            elif verb == "travel" and noun:
                self.world.change_region(noun)

            elif verb == "look":
                print(f"You are currently in the {self.world.current_region}.")
                print(f"There are {len(self.world.enemies)} enemies in this area.")

            elif verb == "enemies":
                self.show_enemies()

            elif verb == "examine":
                if noun:
                    print(examine(noun))
                else:
                    print("Examine what?")

            elif verb == "stats":
                print(self.player.show_stats())

            elif verb == "inventory":
                self.show_inventory()

            elif verb == "use" and noun:
                self.use_item(noun)

            elif verb == "attack" and noun:
                enemy = self.world.get_enemy_by_name(noun)
                if enemy:
                    print(f"{self.player.name} initiates combat with {enemy.name}!")
                    combat = Combat(self.player, enemy)
                    combat.start_combat()

                    if self.player.health <= 0:
                        print(f"{self.player.name} has been defeated!")
                        self.running = False 
                else:
                    print(f"No enemy named '{noun}' found.")

            elif verb == "encounter":
                enemy = self.world.encounter_enemy()
                if enemy:
                    print(f"{self.player.name} encounters {enemy.name}!")
                    combat = Combat(self.player, enemy)
                    combat.start_combat()

                    if self.player.health <= 0:
                        print(f"{self.player.name} has been defeated!")
                        self.running = False
                else:
                    print("No enemies to encounter.")

            else:
                print("Unknown command. Type 'help' for a list of commands.")

        if not self.player.is_alive():
            print("Game over! Your character has been defeated.")

    def show_regions(self):
        """Display all available regions."""
        print("Available regions:")
        for region in self.world.regions.keys():
            if region == self.world.current_region:
                print(f"  {region} (current)")
            else:
                print(f"  {region}")

    def show_enemies(self):
        """Display all enemies in the current region."""
        if not self.world.enemies:
            print("There are no enemies in this region.")
            return

        print(f"Enemies in the {self.world.current_region}:")
        for i, enemy in enumerate(self.world.enemies, 1):
            print(f"  {i}. {enemy.name}: {enemy.get_desc()}")

    def show_inventory(self):
        """Display the player's inventory."""
        if not self.player.inventory:
            print("Your inventory is empty.")
            return

        print("Your inventory:")
        for i, item in enumerate(self.player.inventory, 1):
            equipped = ""
            if hasattr(item, 'equipped') and item.equipped:
                equipped = " (equipped)"
            print(f"  {i}. {item.name}{equipped}: {item.description}")

    def use_item(self, noun):
        """Use an item from the player's inventory."""
        if not self.player.inventory:
            print("Your inventory is empty.")
            return

        try:
            # Check if noun is a number
            item_index = int(noun) - 1
            if 0 <= item_index < len(self.player.inventory):
                item = self.player.inventory[item_index]
                result = item.use(self.player)
                print(result)
                if item.consumable:
                    self.player.inventory.pop(item_index)
            else:
                print(f"Invalid item number. You have {len(self.player.inventory)} items.")
        except ValueError:
            # If not a number, search by name
            found = False
            for item in self.player.inventory:
                if item.name.lower() == noun.lower():
                    result = item.use(self.player)
                    print(result)
                    if item.consumable:
                        self.player.inventory.remove(item)
                    found = True
                    break
            if not found:
                print(f"No item named '{noun}' found in your inventory.")