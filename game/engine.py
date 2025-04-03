from .characters import Orc, Elf, Human
from .commands import examine, attack, help_command
from .world import GameObject, World
import random as rd

class GameEngine:
    """Manages the game loop and user commands."""
    def __init__(self):
        self.running = True
        self.player = None
        self.world = World()
        self.world.populate_world()

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

        print(f"You are {self.player.name}, An {self.player.race} warrior with {self.player.health} HP.")
        print("Type 'help' for commands.")
        self.game_loop()

    def game_loop(self):
        while self.running:
            command = input(": ").strip().lower().split()
            if not command:
                continue
            verb, noun = command[0], command[1] if len(command) > 1 else None

            if verb == "quit":
                print("Goodbye, traveler!")
                self.running = False
            elif verb == "help":
                print(help_command())
            elif verb == "examine":
                if noun:
                    print(examine(noun))
                else:
                    print("Examine what?")
            elif verb == "attack":
                if noun:
                    print(attack(self.player, noun))
                else:
                    print("Attack who?")
            elif verb =="encounter":
                enemy = self.world.encounter_enemy()
                if enemy:
                    print(f"{self.player.name} encounters {enemy.name}!")
                    while enemy.is_alive() and self.player.is_alive():
                        action = input("Do you want to 'attack' or 'flee'? ").strip().lower()
                        if action == "attack":
                            print(attack(self.player, enemy.name))
                        elif action == "flee":
                            if self.attempt_flee(enemy):
                                print(f"{self.player.name} successfully flees from {enemy.name}!")
                                break
                            else:
                                print(
                                    f"{self.player.name} is unable to flee from {enemy.name}! The enemy is too strong!")
                                print(attack(self.player, enemy.name))
                        else:
                            print("Invalid command.")

                    if not enemy.is_alive():
                        print(f"{enemy.name} has been defeated!")
                else:
                    print("No enemies to encounter.")
            else:
                print("Unknown command. Type 'help' for a list of commands.")

    def attempt_flee(self, enemy):
        """
        Determines if the player can flee from the enemy.
        A higher chance of success if the player is stronger or if the enemy is weak.
        :param enemy: The enemy character.
        :return: True if the flee chance is 50% or higher, False otherwise.
        """
        flee_chance = rd.random()
        player_strength = self.player.health # for now, we're using player health as strength
        enemy_strength = enemy.health # same for the enemy

        if player_strength > enemy_strength:
            flee_chance += 0.2

        if player_strength < enemy_strength:
            flee_chance -= 0.2

        flee_chance = max(0.0, min(flee_chance, 1.0))

        return flee_chance >= 0.5