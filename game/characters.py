from .game_object import GameObject
import random as rd

class Character(GameObject):
    """Base class for all characters in the game."""
    def __init__(self, name, race, health, attack_power):
        description = f"{GameObject.get_article(race)} {race} warrior with {health} HP."
        super().__init__(name, description)
        self.race = race
        self.health = health
        self.attack_power = attack_power

    def is_alive(self):
        return self.health > 0

    def attack(self, target):
        if not isinstance(target, Character):
            return f"{target.name} is not a valid target!"
        damage = rd.randint(1, self.attack_power)
        target.health -= damage
        return f"{self.name} attacks {target.name} for {damage} damage! {target.name} now has {target.health} HP."

class Orc(Character):
    def __init__(self, name):
        super().__init__(name, "Orc", 20, 5)

class Elf(Character):
    def __init__(self, name):
        super().__init__(name, "Elf", 15, 6)

class Human(Character):
    def __init__(self, name):
        super().__init__(name, "Human", 18, 4)