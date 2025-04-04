import random as rd
from .game_object import GameObject


class Item(GameObject):
    """Base class for all items in the game."""

    def __init__(self, name, description, value=0, consumable=False):
        super().__init__(name, description)
        self.value = value
        self.consumable = consumable
        self.equipped = False

    def use(self, user, target=None):
        """Default use method for items. Should be overridden by subclasses."""
        return f"{user.name} uses {self.name}, but nothing happens."


class Consumable(Item):
    """Base class for consumable items."""
    
    def __init__(self, name, description, value=10):
        super().__init__(name, description, value=value, consumable=True)


class Equipment(Item):
    """Base class for equipment items."""
    
    def __init__(self, name, description, value=30):
        super().__init__(name, description, value=value, consumable=False)
    
    def equip(self, character):
        """Equip this item."""
        self.equipped = True
        return f"{character.name} equips {self.name}."
    
    def unequip(self, character):
        """Unequip this item."""
        self.equipped = False
        return f"{character.name} unequips {self.name}."


class HealingPotion(Consumable):
    """A potion that heals the user."""

    def __init__(self, name="Healing Potion", description="A red potion that restores health.", healing_amount=None):
        if healing_amount is None:
            healing_amount = rd.randint(5, 15)
        
        if description == "A red potion that restores health.":
            description = f"A red potion that restores {healing_amount} HP."
            
        super().__init__(name, description, value=healing_amount*2)
        self.healing_amount = healing_amount

    def use(self, user, target=None):
        """Heal the user by the healing amount."""
        original_health = user.health
        user.health += self.healing_amount
        actual_heal = user.health - original_health
        return f"{user.name} drinks the {self.name} and recovers {actual_heal} HP! Current HP: {user.health}/{user.max_health}"


class DamagePotion(Consumable):
    """A potion that damages the target."""

    def __init__(self, name="Damage Potion", description="A volatile mixture in a glass vial.", damage_amount=None):
        if damage_amount is None:
            damage_amount = rd.randint(8, 12)
            
        if description == "A volatile mixture in a glass vial.":
            description = f"A volatile mixture that deals {damage_amount} damage when thrown."
            
        super().__init__(name, description, value=damage_amount*2)
        self.damage_amount = damage_amount

    def use(self, user, target=None):
        """Deal damage to the target."""
        if target is None:
            return f"{user.name} readies the {self.name} to throw at an enemy."

        original_health = target.health
        target.health -= self.damage_amount
        actual_damage = original_health - target.health
        return f"{user.name} throws the {self.name} at {target.name}, dealing {actual_damage} damage! {target.name}'s HP: {target.health}"


class StrengthElixir(Consumable):
    """Temporarily boosts attack power."""
    
    def __init__(self, name="Strength Elixir", boost_amount=None, duration=3):
        if boost_amount is None:
            boost_amount = rd.randint(2, 4)
            
        description = f"A powerful brew that increases attack by {boost_amount} for {duration} turns."
        super().__init__(name, description, value=boost_amount*10)
        self.boost_amount = boost_amount
        self.duration = duration
    
    def use(self, user, target=None):
        user._attack_power += self.boost_amount
        return f"{user.name} drinks the {self.name}, feeling stronger! Attack +{self.boost_amount}."


class DefensePotion(Consumable):
    """Temporarily boosts defense."""
    
    def __init__(self, name="Defense Potion", boost_amount=None, duration=3):
        if boost_amount is None:
            boost_amount = rd.randint(1, 3)
            
        description = f"A thick, metallic liquid that increases defense by {boost_amount} for {duration} turns."
        super().__init__(name, description, value=boost_amount*10)
        self.boost_amount = boost_amount
        self.duration = duration
    
    def use(self, user, target=None):
        user._defense += self.boost_amount
        return f"{user.name} drinks the {self.name}, feeling more resilient! Defense +{self.boost_amount}."


class Weapon(Equipment):
    """A weapon that can be equipped to increase attack power."""

    def __init__(self, name, description, attack_bonus=2):
        super().__init__(name, description, value=attack_bonus*25)
        self.attack_bonus = attack_bonus
        self.equipped = False

    def use(self, user, target=None):
        """Equip the weapon, increasing the user's attack power."""
        if not hasattr(user, 'equipped_weapon'):
            user.equipped_weapon = None

        if self.equipped:
            # unequip the weapon
            self.equipped = False
            user.equipped_weapon = None
            return f"{user.name} unequips {self.name}."
        else:
            # unequip any currently equipped weapon
            if user.equipped_weapon:
                user.equipped_weapon.equipped = False

            # equip this weapon
            self.equipped = True
            user.equipped_weapon = self
            return f"{user.name} equips {self.name}, gaining +{self.attack_bonus} attack power!"


class Armor(Equipment):
    """Armor that can be equipped to absorb damage."""

    def __init__(self, name, description, defense_bonus=2):
        super().__init__(name, description, value=defense_bonus*20)
        self.defense_bonus = defense_bonus
        self.equipped = False

    def use(self, user, target=None):
        """Equip the armor, reducing incoming damage."""
        if not hasattr(user, 'equipped_armor'):
            user.equipped_armor = None

        if self.equipped:
            # unequip the armor
            self.equipped = False
            user.equipped_armor = None
            return f"{user.name} removes {self.name}."
        else:
            # unequip any currently equipped armor
            if user.equipped_armor:
                user.equipped_armor.equipped = False

            # equip this armor
            self.equipped = True
            user.equipped_armor = self
            return f"{user.name} puts on {self.name}, gaining +{self.defense_bonus} defense!"


class LuckCharm(Equipment):
    """Increases critical hit chance when equipped."""
    
    def __init__(self, name="Lucky Charm", description="A small trinket that seems to bring good fortune."):
        super().__init__(name, description, value=40)
        self.crit_bonus = 0.1  # 10% increase to critical hit chance
        self.equipped = False
    
    def use(self, user, target=None):
        if not hasattr(user, 'equipped_charm'):
            user.equipped_charm = None
            
        if self.equipped:
            self.equipped = False
            user.equipped_charm = None
            return f"{user.name} removes the {self.name}."
        else:
            if user.equipped_charm:
                user.equipped_charm.equipped = False
                
            self.equipped = True
            user.equipped_charm = self
            return f"{user.name} wears the {self.name}, feeling luckier!"


def create_starting_items():
    """Create a set of starting items for a new player."""
    items = [
        HealingPotion(),
        Weapon("Rusty Sword", "An old sword with some rust, but still sharp.", 1),
        Armor("Leather Tunic", "Basic protection made of hardened leather.", 1)
    ]
    
    # add one random bonus item based on chance
    bonus_roll = rd.random()
    
    if bonus_roll < 0.2:  # 20% chance for a good weapon
        items.append(Weapon("Steel Shortsword", "A well-crafted blade of decent quality.", 2))
    elif bonus_roll < 0.4:  # 20% chance for good armor
        items.append(Armor("Studded Leather", "Reinforced leather armor offering better protection.", 2))
    elif bonus_roll < 0.6:  # 20% chance for a strength elixir
        items.append(StrengthElixir())
    elif bonus_roll < 0.8:  # 20% chance for a defense potion
        items.append(DefensePotion())
    else:  # 20% chance for a luck charm
        items.append(LuckCharm())
    
    return items