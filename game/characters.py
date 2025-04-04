from .game_object import GameObject
import random as rd


class Character(GameObject):
    """Base class for all characters in the game."""

    def __init__(self, name, race, health, attack_power):
        description = f"{GameObject.get_article(race)} {race} warrior with {health} HP."
        super().__init__(name, description)
        self.race = race
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.defense = 0
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None

    def is_alive(self):
        return self.health > 0

    def attack(self, target):
        if not isinstance(target, Character):
            return f"{target.name} is not a valid target!"

        damage = rd.randint(1, self.attack_power)

        # apply target's defense if they have any
        if hasattr(target, 'defense') and target.defense > 0:
            reduced_damage = max(1, damage - target.defense)  # minimum 1 damage
            damage_blocked = damage - reduced_damage
            damage = reduced_damage
            target.health = max(0, target.health - damage)
            return f"{self.name} attacks {target.name} for {damage} damage! {target.name}'s armor blocks {damage_blocked} damage. {target.name} now has {target.health} HP."
        else:
            target.health = max(0, target.health - damage)
            return f"{self.name} attacks {target.name} for {damage} damage! {target.name} now has {target.health} HP."

    def heal(self, amount):
        """Heal the character by the specified amount, not exceeding max health."""
        original_health = self.health
        self.health = min(self.max_health, self.health + amount)
        actual_heal = self.health - original_health
        return f"{self.name} heals for {actual_heal} HP! Current HP: {self.health}/{self.max_health}"

    def add_item(self, item):
        """Add an item to the character's inventory."""
        self.inventory.append(item)
        return f"{self.name} acquires {item.name}!"

    def remove_item(self, item):
        """Remove an item from the character's inventory."""
        if item in self.inventory:
            self.inventory.remove(item)
            return f"{self.name} no longer has {item.name}."
        return f"{self.name} doesn't have {item.name}."

    def show_stats(self):
        """Display the character's current stats."""
        stats = (
            f"Name: {self.name}\n"
            f"Race: {self.race}\n"
            f"Health: {self.health}/{self.max_health}\n"
            f"Attack: {self.attack_power}\n"
            f"Defense: {self.defense}\n"
        )

        if self.equipped_weapon:
            stats += f"Weapon: {self.equipped_weapon.name}\n"
        if self.equipped_armor:
            stats += f"Armor: {self.equipped_armor.name}\n"

        return stats


class Orc(Character):
    def __init__(self, name):
        super().__init__(name, "Orc", 20, 5)
        # Orcs get a slight defense boost
        self.defense = 1


class Elf(Character):
    def __init__(self, name):
        super().__init__(name, "Elf", 15, 6)
        # Elves have higher attack but lower health


class Human(Character):
    def __init__(self, name):
        super().__init__(name, "Human", 18, 4)
        # Humans are balanced