from .characters import Orc, Elf, Human
from .commands import examine, attack, help_command
from .world import GameObject, World
from .combat import Combat
#import random as rd

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
                    combat = Combat(self.player, enemy)
                    combat.start_combat()
                else:
                    print("No enemies to encounter.")
            else:
                print("Unknown command. Type 'help' for a list of commands.")
