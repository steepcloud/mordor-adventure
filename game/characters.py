from .game_object import GameObject
import random as rd


class Character(GameObject):
    """Base class for all characters in the game."""

    def __init__(self, name, race, health, attack_power):
        description = f"{GameObject.get_article(race)} {race} warrior with {health} HP."
        super().__init__(name, description)
        self.race = race
        self._health = health
        self._max_health = health  # store max health for healing purposes
        self._attack_power = attack_power
        self._defense = 0 
        self.inventory = [] 
        self.equipped_weapon = None
        self.equipped_armor = None
        self.equipped_charm = None

    @property
    def health(self):
        """Get the character's current health."""
        return self._health

    @health.setter
    def health(self, value):
        """Set the character's health, ensuring it stays withing bounds."""
        self._health = max(0, min(value, self.max_health))
    
    @property
    def max_health(self):
        """Get the character's maximum health."""
        return self._max_health

    @max_health.setter
    def max_health(self, value):
        """Set the character's maximum health."""
        self._max_health = max(1, value)
        if self._health > self._max_health:
            self._health = self.max_health
    
    @property
    def attack_power(self):
        """Get the character's attack power including weapon bonus."""
        base_power = self._attack_power
        # weapons adds to base attack if equipped
        weapon_bonus = self.equipped_weapon.attack_bonus if self.equipped_weapon else 0
        return base_power + weapon_bonus
    
    @attack_power.setter
    def attack_power(self, value):
        """Set the character's base attack power."""
        self._attack_power = max(1, value)
    
    @property
    def defense(self):
        """Get the character's defense including armor bonus."""
        base_defense = self._defense
        armor_bonus = self.equipped_armor.defense_bonus if self.equipped_armor else 0
        return base_defense + armor_bonus

    @defense.setter
    def defense(self, value):
        """Set the character's base defense."""
        self._defense = max(0, value)

    def is_alive(self):
        return self.health > 0

    def attack(self, target):
        if not isinstance(target, Character):
            return f"{target.name} is not a valid target!"

        damage = rd.randint(1, self.attack_power)

        # armor reduces incoming damage but never below 1
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
        """Add an item to the character's inventory if there's space."""
        if len(self.inventory) >= 10:  # limit inventory to 10 items
            return f"{self.name}'s inventory is full! Drop something first."
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
    
    def special_ability(self, target):
        """Orcs have Berserker Rage: deal high damage but take recoil damage."""
        damage = rd.randint(self.attack_power, self.attack_power * 2)
        target.health -= damage

        recoil = max(1, damage // 4) # recoil scales with damage dealt
        self.health -= recoil

        return (f"{self.name} goes into a berserker rage and deals {damage} damage to {target.name}! "
                f"The rage costs {self.name} {recoil} health points.")



class Elf(Character):
    def __init__(self, name):
        super().__init__(name, "Elf", 15, 6)
        # Elves have higher attack but lower health
    
    def special_ability(self, target):
        """Elves have Precision Strike: guaranteed hit with critical chance."""
        # elves have higher crit chance representing their accuracy
        critical = rd.random() < 0.4  # 40% chance for critical hit
        damage = self.attack_power * (2 if critical else 1)
        target.health -= damage
        
        if critical:
            return f"{self.name} fires a critical precision shot at {target.name} for {damage} damage!"
        else:
            return f"{self.name} fires a precision shot at {target.name} for {damage} damage!"


class Human(Character):
    def __init__(self, name):
        super().__init__(name, "Human", 18, 4)
        # Humans are balanced

    def special_ability(self, target=None):
        """Humans have Resilience: restore health and gain temporary defense."""
        # defensive ability that represents human adaptability 
        heal_amount = rd.randint(2, 5)
        original_health = self.health
        self.health += heal_amount
        actual_heal = self.health - original_health
        
        # temporary defense boost only lasts for the next attack
        self._defense += 2 
        
        return f"{self.name} shows resilience, healing for {actual_heal} HP and gaining +2 defense for the next attack!"