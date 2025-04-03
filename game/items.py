from .game_object import GameObject


class Item(GameObject):
    """Base class for all items in the game."""

    def __init__(self, name, description, value=0, consumable=False):
        super().__init__(name, description)
        self.value = value
        self.consumable = consumable

    def use(self, user, target=None):
        """Default use method for items. Should be overridden by subclasses."""
        return f"{user.name} uses {self.name}, but nothing happens."


class HealingPotion(Item):
    """A potion that heals the user."""

    def __init__(self, name="Healing Potion", healing_amount=10):
        description = f"A potion that restores {healing_amount} HP."
        super().__init__(name, description, value=20, consumable=True)
        self.healing_amount = healing_amount

    def use(self, user, target=None):
        """Heal the user by the healing amount."""
        user.health += self.healing_amount
        return f"{user.name} drinks the {self.name} and recovers {self.healing_amount} HP! Current HP: {user.health}"


class DamagePotion(Item):
    """A potion that damages the target."""

    def __init__(self, name="Damage Potion", damage_amount=8):
        description = f"A potion that deals {damage_amount} damage to an enemy."
        super().__init__(name, description, value=15, consumable=True)
        self.damage_amount = damage_amount

    def use(self, user, target=None):
        """Deal damage to the target."""
        if target is None:
            return f"{user.name} has no target to use {self.name} on!"

        target.health -= self.damage_amount
        return f"{user.name} throws the {self.name} at {target.name}, dealing {self.damage_amount} damage! {target.name}'s HP: {target.health}"


class Weapon(Item):
    """A weapon that can be equipped to increase attack power."""

    def __init__(self, name, description, attack_bonus=2):
        super().__init__(name, description, value=50, consumable=False)
        self.attack_bonus = attack_bonus
        self.equipped = False

    def use(self, user, target=None):
        """Equip the weapon, increasing the user's attack power."""
        if not hasattr(user, 'equipped_weapon'):
            user.equipped_weapon = None

        if self.equipped:
            # Unequip the weapon
            user.attack_power -= self.attack_bonus
            self.equipped = False
            return f"{user.name} unequips {self.name}."
        else:
            # Unequip any currently equipped weapon
            if user.equipped_weapon:
                user.equipped_weapon.use(user)  # Unequip the current weapon

            # Equip this weapon
            user.attack_power += self.attack_bonus
            self.equipped = True
            user.equipped_weapon = self
            return f"{user.name} equips {self.name}, gaining +{self.attack_bonus} attack power!"


class Armor(Item):
    """Armor that can be equipped to absorb damage."""

    def __init__(self, name, description, defense_bonus=2):
        super().__init__(name, description, value=40, consumable=False)
        self.defense_bonus = defense_bonus
        self.equipped = False

    def use(self, user, target=None):
        """Equip the armor, reducing incoming damage."""
        if not hasattr(user, 'equipped_armor'):
            user.equipped_armor = None
            user.defense = 0  # Base defense

        if self.equipped:
            # Unequip the armor
            user.defense -= self.defense_bonus
            self.equipped = False
            return f"{user.name} removes {self.name}."
        else:
            # Unequip any currently equipped armor
            if user.equipped_armor:
                user.equipped_armor.use(user)  # Unequip the current armor

            # Equip this armor
            user.defense += self.defense_bonus
            self.equipped = True
            user.equipped_armor = self
            return f"{user.name} puts on {self.name}, gaining +{self.defense_bonus} defense!"


def create_starting_items():
    """Create a set of starting items for a new player."""
    return [
        HealingPotion(),
        DamagePotion(),
        Weapon("Rusty Sword", "An old sword with some rust, but still sharp.", 1),
        Armor("Leather Tunic", "Basic protection made of hardened leather.", 1)
    ]